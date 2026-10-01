import json
import time
import urllib.request

import pilot_12_cases as s

c = s.L['it']
crit = {c['keys'][a]: c['desc'][a] for a in s.AG}
short = {c['keys'][a]: None for a in s.AG}
for label, criteria in (('long', crit), ('short', short)):
	times = []
	for text in c['req'][:6]:
		body = {'model': s.MODEL, 'state': {c['state_key']: text}, 'questions': {'route': {'type': 'choice', 'instructions': c['route_q'], 'criteria': criteria}}}
		req = urllib.request.Request(s.URL, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
		t0 = time.perf_counter()
		urllib.request.urlopen(req, timeout=600).read()
		times.append(round((time.perf_counter() - t0) * 1000))
	print(label, times)
