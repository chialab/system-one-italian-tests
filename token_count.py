import json
import sys
import urllib.request

from suite_data import DOMAINS, ESCALATION

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8091/tokenize'


def ntok(text):
	req = urllib.request.Request(URL, data=json.dumps({'content': text}).encode(), headers={'Content-Type': 'application/json'})
	return len(json.load(urllib.request.urlopen(req))['tokens'])


for lang in ('it', 'en'):
	req_tok = q_tok = opt_tok = opt_chars = n = 0
	for d in DOMAINS.values():
		options = [f"{d['agents'][c][lang][0]}: {d['agents'][c][lang][1]}" for c in d['agents']]
		per_case_opt = sum(ntok(o) for o in options)
		per_case_chars = sum(len(o) for o in options)
		q = ntok(d['question'][lang])
		for case in d['cases']:
			req_tok += ntok(case[0 if lang == 'it' else 1])
			q_tok += q
			opt_tok += per_case_opt
			opt_chars += per_case_chars
			n += 1
	conv = sum(ntok('\n'.join(c[0 if lang == 'it' else 1])) for c in ESCALATION['cases']) / len(ESCALATION['cases'])
	print(f"{lang}: routing request {req_tok / n:.0f} tok, question {q_tok / n:.0f} tok, options {opt_tok / n:.0f} tok ({opt_chars / n:.0f} chars) | escalation conversation {conv:.0f} tok")
