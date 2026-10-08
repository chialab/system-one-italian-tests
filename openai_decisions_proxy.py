import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

OPENAI_URL = 'https://api.openai.com/v1/decisions'


def render_state(state):
	return '\n\n'.join(f"{k}:\n{v}" if '\n' in v else f"{k}: {v}" for k, v in state.items())


def to_question(name, q):
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


def from_answer(a, q):
	# A refusal maps to probability 0 everywhere, so it counts as "not flagged" / first option; it is logged to stderr
	if a['type'] == 'refusal':
		print(f"REFUSAL {a.get('name')}", file=sys.stderr, flush=True)
		if q['type'] == 'noul':
			return {'noul': 0.0, 'refusal': True}
		if q['type'] == 'choice':
			return {'probabilities': {k: 0.0 for k in q['criteria']}, 'refusal': True}
		return {'score': 0.0, 'refusal': True}
	if a['type'] == 'predicate':
		return {'noul': a['probability']}
	if a['type'] == 'choice':
		return {'probabilities': {p['value']: p['probability'] for p in a['probabilities']}, 'confidence': a.get('confidence')}
	return {'score': a['score'], 'probabilities': a.get('probabilities'), 'confidence': a.get('confidence')}


def call_openai(body, key, retries=6):
	data = json.dumps(body).encode()
	for attempt in range(retries):
		req = urllib.request.Request(OPENAI_URL, data=data, headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {key}'})
		try:
			with urllib.request.urlopen(req, timeout=300) as r:
				return json.load(r)
		except urllib.error.HTTPError as e:
			if e.code not in (429, 500, 502, 503, 504) or attempt == retries - 1:
				raise
			print(f"RETRY {e.code} attempt {attempt + 1}", file=sys.stderr, flush=True)
			time.sleep(2 ** attempt)


class Handler(BaseHTTPRequestHandler):
	def do_POST(self):
		body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
		qs = body['questions']
		req = {'model': self.server.model, 'input': render_state(body['state']), 'questions': [to_question(n, q) for n, q in qs.items()]}
		try:
			res = call_openai(req, self.server.key)
		except urllib.error.HTTPError as e:
			err = e.read()
			print(f"ERROR {e.code} {err[:500]!r}", file=sys.stderr, flush=True)
			self.send_response(e.code)
			self.end_headers()
			self.wfile.write(err)
			return
		answers = {a['name']: from_answer(a, qs[a['name']]) for a in res['answers']}
		out = json.dumps({'answers': answers, 'usage': res.get('usage')}).encode()
		self.send_response(200)
		self.send_header('Content-Type', 'application/json')
		self.send_header('Content-Length', str(len(out)))
		self.end_headers()
		self.wfile.write(out)

	def log_message(self, *args):
		pass


def main():
	ap = argparse.ArgumentParser(description="Serves the TypeSafe /v1/systemone format on top of the OpenAI Decisions API")
	ap.add_argument('--port', type=int, default=8092)
	ap.add_argument('--model', default='gpt-6-luna', help="OpenAI model, overrides the one sent by the client")
	a = ap.parse_args()
	server = HTTPServer(('127.0.0.1', a.port), Handler)
	server.key = os.environ['OPENAI_API_KEY']
	server.model = a.model
	print(f"listening on http://127.0.0.1:{a.port}/v1/systemone -> {OPENAI_URL} ({a.model})", file=sys.stderr, flush=True)
	server.serve_forever()


if __name__ == '__main__':
	main()
