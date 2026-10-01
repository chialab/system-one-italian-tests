import argparse
import importlib
import json
import time
import urllib.request
from pathlib import Path

LABELS = {
	'it': {'request': "Richiesta", 'context': "Contesto", 'conversation': "Conversazione", 'user': "Utente", 'bot': "Bot"},
	'en': {'request': "Request", 'context': "Context", 'conversation': "Conversation", 'user': "User", 'bot': "Bot"}
}


def post(url, body):
	req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
	t0 = time.perf_counter()
	with urllib.request.urlopen(req, timeout=600) as r:
		out = json.load(r)
	return out['answers'], (time.perf_counter() - t0) * 1000


def top(probs):
	k = max(probs, key=probs.get)
	return k, probs[k]


def run_routing(url, model, domains, langs):
	rows = []
	for dname, d in domains.items():
		for lang in langs:
			codes = list(d['agents'])
			key_to_code = {d['agents'][c][lang][0]: c for c in codes}
			crit = {d['agents'][c][lang][0]: d['agents'][c][lang][1] for c in codes}
			crit_rev = {d['agents'][c][lang][0]: d['agents'][c][lang][1] for c in reversed(codes)}
			for i, case in enumerate(d['cases']):
				text, accepted = case[0 if lang == 'it' else 1], case[2]
				if text is None:
					continue
				answers, ms = post(url, {'model': model, 'state': {LABELS[lang]['request']: text}, 'questions': {
					'route': {'type': 'choice', 'instructions': d['question'][lang], 'criteria': crit},
					'route_rev': {'type': 'choice', 'instructions': d['question'][lang], 'criteria': crit_rev}
				}})
				k, p = top(answers['route']['probabilities'])
				kr, pr = top(answers['route_rev']['probabilities'])
				row = {'domain': dname, 'lang': lang, 'i': i + 1, 'text': text, 'accepted': accepted,
					'pred': key_to_code[k], 'p': round(p, 3), 'ok': key_to_code[k] in accepted,
					'pred_rev': key_to_code[kr], 'p_rev': round(pr, 3), 'ok_rev': key_to_code[kr] in accepted, 'ms': round(ms)}
				rows.append(row)
				print(f"route {dname} {lang} {i + 1:>2} {row['pred']:<5} {row['p']:.2f} {'ok' if row['ok'] else 'KO'} | rev {row['pred_rev']:<5} {'ok' if row['ok_rev'] else 'KO'} {ms:.0f}ms", flush=True)
	return rows


def render(turns, lang):
	lab = LABELS[lang]
	return '\n'.join(f"{lab['user'] if j % 2 == 0 else lab['bot']}: {t}" for j, t in enumerate(turns))


def run_escalation(url, model, e, langs):
	rows = []
	for lang in langs:
		lab = LABELS[lang]
		esc_key = 'passa_a_umano' if lang == 'it' else 'escalate_to_human'
		for i, case in enumerate(e['cases']):
			it_turns, en_turns, escalate, urgency = case[:4]
			risk = case[4] if len(case) > 4 else urgency == 2
			turns = it_turns if lang == 'it' else en_turns
			if turns is None:
				continue
			state = {lab['context']: e['context'][lang], lab['conversation']: render(turns, lang)}
			answers, ms = post(url, {'model': model, 'state': state, 'questions': {
				'noul': {'type': 'noul', 'instructions': e['noul'][lang]},
				'choice': {'type': 'choice', 'instructions': e['choice_q'][lang], 'criteria': e['choice'][lang]},
				'urgency': {'type': 'score', 'instructions': e['score_q'][lang], 'criteria': e['levels'][lang]},
				'risk': {'type': 'noul', 'instructions': e['risk_q'][lang]}
			}})
			p_noul = answers['noul']['noul']
			p_choice = answers['choice']['probabilities'][esc_key]
			p_risk = answers['risk']['noul']
			row = {'lang': lang, 'i': i + 1, 'first': turns[0], 'escalate': escalate, 'urgency': urgency, 'risk': risk,
				'p_noul': round(p_noul, 3), 'ok_noul': None if escalate is None else (p_noul >= 0.5) == escalate,
				'p_choice': round(p_choice, 3), 'ok_choice': None if escalate is None else (p_choice >= 0.5) == escalate,
				'p_risk': round(p_risk, 3), 'ok_risk': None if risk is None else (p_risk >= 0.5) == risk,
				'score': round(answers['urgency']['score'], 2), 'ms': round(ms)}
			rows.append(row)
			exp = '?' if escalate is None else 'Y' if escalate else 'N'
			print(f"esc {lang} {i + 1:>2} exp={exp} noul {p_noul:.2f} | choice {p_choice:.2f} | risk {p_risk:.2f} (exp {risk}) | urg {row['score']:.2f} (exp {urgency}) {ms:.0f}ms", flush=True)
	return rows


def auroc(pos, neg):
	if not pos or not neg:
		return None
	wins = sum(1.0 if p > n else 0.5 if p == n else 0.0 for p in pos for n in neg)
	return round(wins / (len(pos) * len(neg)), 3)


def summarise(route, esc, domains, langs):
	s = {'routing': {}, 'escalation': {}}
	for dname in domains:
		for lang in langs:
			rs = [r for r in route if r['domain'] == dname and r['lang'] == lang]
			if not rs:
				continue
			s['routing'][f'{dname}/{lang}'] = {
				'n': len(rs), 'ok': sum(r['ok'] for r in rs), 'ok_rev': sum(r['ok_rev'] for r in rs),
				'flips': sum(r['pred'] != r['pred_rev'] for r in rs),
				'median_ms': sorted(r['ms'] for r in rs)[len(rs) // 2]
			}
	for lang in langs:
		rs = [r for r in route if r['lang'] == lang]
		wrong = [r['p'] for r in rs if not r['ok']]
		right = [r['p'] for r in rs if r['ok']]
		s['routing'][f'ALL/{lang}'] = {
			'n': len(rs), 'ok': sum(r['ok'] for r in rs), 'ok_rev': sum(r['ok_rev'] for r in rs),
			'flips': sum(r['pred'] != r['pred_rev'] for r in rs),
			'mean_p_right': round(sum(right) / len(right), 3) if right else None,
			'mean_p_wrong': round(sum(wrong) / len(wrong), 3) if wrong else None
		}
		es = [r for r in esc if r['lang'] == lang and r['escalate'] is not None]
		if not es:
			continue
		pos = [r for r in es if r['escalate']]
		neg = [r for r in es if not r['escalate']]
		rk = [r for r in esc if r['lang'] == lang and r['risk'] is not None]
		s['escalation'][lang] = {
			'n_scored': len(es), 'n_borderline': sum(1 for r in esc if r['lang'] == lang and r['escalate'] is None),
			'noul_ok': sum(r['ok_noul'] for r in es), 'noul_missed': sum(not r['ok_noul'] for r in pos), 'noul_false_alarm': sum(not r['ok_noul'] for r in neg),
			'noul_auroc': auroc([r['p_noul'] for r in pos], [r['p_noul'] for r in neg]),
			'choice_ok': sum(r['ok_choice'] for r in es), 'choice_missed': sum(not r['ok_choice'] for r in pos), 'choice_false_alarm': sum(not r['ok_choice'] for r in neg),
			'choice_auroc': auroc([r['p_choice'] for r in pos], [r['p_choice'] for r in neg]),
			'risk_ok': sum(r['ok_risk'] for r in rk), 'risk_n': len(rk),
			'risk_missed': sum(not r['ok_risk'] for r in rk if r['risk']), 'risk_false_alarm': sum(not r['ok_risk'] for r in rk if not r['risk']),
			'urgency_exact': sum(round(r['score']) == r['urgency'] for r in es),
			'median_ms': sorted(r['ms'] for r in es)[len(es) // 2]
		}
	return s


def main():
	ap = argparse.ArgumentParser(description="Routing and escalation suite against a TypeSafe-compatible /v1/systemone endpoint")
	ap.add_argument('--url', default='http://127.0.0.1:8091/v1/systemone')
	ap.add_argument('--data', default='suite_data', help="data module: suite_data or suite_data_hard")
	ap.add_argument('--langs', default='it,en')
	ap.add_argument('--model', default='Winnow-12B', help="model name sent in the request body")
	ap.add_argument('--tag', default=None, help="results folder name, default: lowercased --model")
	ap.add_argument('--out', default=None, help="default: results/<tag>/<data>_<langs>.json")
	a = ap.parse_args()
	langs = tuple(a.langs.split(','))
	data = importlib.import_module(a.data)
	tag = a.tag or a.model.lower()
	out = Path(a.out or Path(__file__).parent / 'results' / tag / f"{a.data}_{'-'.join(langs)}.json")
	route = run_routing(a.url, a.model, data.DOMAINS, langs)
	esc = run_escalation(a.url, a.model, data.ESCALATION, langs)
	summary = summarise(route, esc, data.DOMAINS, langs)
	out.parent.mkdir(parents=True, exist_ok=True)
	out.write_text(json.dumps({'summary': summary, 'routing': route, 'escalation': esc}, indent=1, ensure_ascii=False))
	print('SUMMARY')
	print(json.dumps(summary, indent=1, ensure_ascii=False))


if __name__ == '__main__':
	main()
