import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

# Gemini blocks the whole request with HTTP 400 and one of these error codes instead of refusing per question
GEMINI_SAFETY_CODES = {'safety', 'prohibited_content', 'blocklist', 'image_safety', 'content_blocked'}


def render_state(state):
	return '\n\n'.join(f"{k}:\n{v}" if '\n' in v else f"{k}: {v}" for k, v in state.items())


def refusal(q):
	# A refusal maps to probability 0 everywhere, so it counts as "not flagged" / first option
	if q['type'] == 'noul':
		return {'noul': 0.0, 'refusal': True}
	if q['type'] == 'choice':
		return {'probabilities': {k: 0.0 for k in q['criteria']}, 'refusal': True}
	return {'score': 0.0, 'refusal': True}


def openai_question(name, q):
	out = {'name': name, 'instructions': q['instructions']}
	if q['type'] == 'noul':
		out['type'] = 'predicate'
	elif q['type'] == 'choice':
		out['type'] = 'choice'
		out['choices'] = [{'value': k} if d is None else {'value': k, 'description': d} for k, d in q['criteria'].items()]
	elif q['type'] == 'score':
		out['type'] = 'score'
		out['levels'] = [{'label': c} if isinstance(c, str) else c for c in q['criteria']]
	else:
		raise ValueError(f"unsupported question type {q['type']}")
	return out


def openai_answer(a, q):
	if a['type'] == 'refusal':
		print(f"REFUSAL {a.get('name')}", file=sys.stderr, flush=True)
		return refusal(q)
	if a['type'] == 'predicate':
		return {'noul': a['probability']}
	if a['type'] == 'choice':
		return {'probabilities': {p['value']: p['probability'] for p in a['probabilities']}, 'confidence': a.get('confidence')}
	return {'score': a['score'], 'probabilities': a.get('probabilities'), 'confidence': a.get('confidence')}


def openai_request(model, body):
	qs = [openai_question(n, q) for n, q in body['questions'].items()]
	return {'model': model, 'input': render_state(body['state']), 'questions': qs}


def openai_response(res, qs):
	return {a['name']: openai_answer(a, qs[a['name']]) for a in res['answers']}


def gemini_question(q):
	out = {'type': q['type'], 'instructions': q['instructions']}
	if q['type'] == 'choice':
		out['criteria'] = {k: d or '' for k, d in q['criteria'].items()}
	elif q['type'] == 'score':
		out['criteria'] = q['criteria']
	elif q['type'] != 'noul':
		raise ValueError(f"unsupported question type {q['type']}")
	return out


def gemini_request(model, body):
	return {'model': model, 'input': render_state(body['state']), 'questions': {n: gemini_question(q) for n, q in body['questions'].items()}}


def gemini_response(res, qs):
	return {n: {k: v for k, v in a.items() if k in ('noul', 'score', 'probabilities', 'confidence')} for n, a in res['answers'].items()}


def gemini_blocked(code, err):
	if code != 400:
		return False
	try:
		e = json.loads(err)['error']
	except (ValueError, KeyError, TypeError):
		return False
	return e.get('code') in GEMINI_SAFETY_CODES or e.get('status') in GEMINI_SAFETY_CODES


PROVIDERS = {
	'openai': {
		'url': 'https://api.openai.com/v1/decisions', 'key_env': 'OPENAI_API_KEY', 'model': 'gpt-6-luna',
		'auth': lambda key: {'Authorization': f'Bearer {key}'},
		'request': openai_request, 'response': openai_response, 'blocked': lambda code, err: False,
		'retry': {429, 500, 502, 503, 504},
	},
	'gemini': {
		'url': 'https://generativelanguage.googleapis.com/v1beta/decisions', 'key_env': 'GEMINI_API_KEY', 'model': 'gemini-decision-1',
		'auth': lambda key: {'x-goog-api-key': key},
		'request': gemini_request, 'response': gemini_response, 'blocked': gemini_blocked,
		# The v1beta endpoint returns sporadic 403 permission_denied that succeed on retry (2026-11-13)
		'retry': {403, 429, 500, 502, 503, 504},
	},
}


def call_upstream(url, headers, body, retry_codes, retries=6):
	data = json.dumps(body).encode()
	for attempt in range(retries):
		req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'} | headers)
		try:
			with urllib.request.urlopen(req, timeout=300) as r:
				return json.load(r)
		except urllib.error.HTTPError as e:
			if e.code not in retry_codes or attempt == retries - 1:
				raise
			print(f"RETRY {e.code} attempt {attempt + 1}", file=sys.stderr, flush=True)
			time.sleep(2 ** attempt)


class Handler(BaseHTTPRequestHandler):
	def do_POST(self):
		p = self.server.provider
		body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
		qs = body['questions']
		try:
			res = call_upstream(self.server.url, p['auth'](self.server.key), p['request'](self.server.model, body), p['retry'])
			out = {'answers': p['response'](res, qs), 'usage': res.get('usage')}
		except urllib.error.HTTPError as e:
			err = e.read()
			if not p['blocked'](e.code, err):
				print(f"ERROR {e.code} {err[:500]!r}", file=sys.stderr, flush=True)
				self.send_response(e.code)
				self.end_headers()
				self.wfile.write(err)
				return
			print(f"REFUSAL request {err[:300]!r}", file=sys.stderr, flush=True)
			out = {'answers': {n: refusal(q) for n, q in qs.items()}, 'usage': None}
		data = json.dumps(out).encode()
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.send_header('Content-Length', str(len(data)))
		self.end_headers()
		self.wfile.write(data)

	def log_message(self, *args):
		pass


def main():
	ap = argparse.ArgumentParser(description="Serves the TypeSafe /v1/systemone format on top of the OpenAI or Gemini Decisions API")
	ap.add_argument('--provider', choices=PROVIDERS, default='openai')
	ap.add_argument('--port', type=int, default=8092)
	ap.add_argument('--model', help="Upstream model, overrides the one sent by the client (default: the provider's model)")
	ap.add_argument('--url', help="Upstream endpoint (default: the provider's public endpoint)")
	a = ap.parse_args()
	p = PROVIDERS[a.provider]
	server = HTTPServer(('127.0.0.1', a.port), Handler)
	server.provider = p
	server.key = os.environ[p['key_env']]
	server.model = a.model or p['model']
	server.url = a.url or p['url']
	print(f"listening on http://127.0.0.1:{a.port}/v1/systemone -> {server.url} ({server.model})", file=sys.stderr, flush=True)
	server.serve_forever()


if __name__ == '__main__':
	main()
