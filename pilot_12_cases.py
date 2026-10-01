import json
import sys
import time
import urllib.request

URL = sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8091/v1/systemone'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'routing_results.json'

AG = ['MED', 'TRAD', 'BIB', 'BAN', 'FO']
EXP = [['TRAD'], ['MED'], ['BIB'], ['BAN'], ['FO'], ['FO'], ['MED', 'TRAD'], ['BAN', 'TRAD'], ['BAN', 'BIB'], ['BAN'], ['FO'], ['TRAD']]
EXP_SCORE = [1, 1, 1, 1, 0, 0, 2, 2, 2, 1, 0, 1]

L = {
	'it': {
		'keys': {'MED': 'mediatore_culturale', 'TRAD': 'traduttore', 'BIB': 'bibliografo', 'BAN': 'esperto_bandi', 'FO': 'front_office'},
		'route_q': "Sei il supervisore di uno sportello di servizi e coordini cinque agenti. A quale agente affidi questa richiesta?",
		'desc': {
			'MED': "Mediatore culturale. Interviene quando una persona straniera e un servizio non si capiscono per differenze culturali, religiose o di abitudini: tensioni, offese, diffidenza o conflitti durante un colloquio o allo sportello. Spiega a entrambe le parti il punto di vista dell'altra, accompagna la persona nei rapporti con scuola, servizi sociali, sanità e uffici pubblici e riporta la calma nelle situazioni delicate.",
			'TRAD': "Traduttore. Traduce per iscritto testi e documenti da una lingua a un'altra: contratti, lettere, certificati, moduli, avvisi, cartelli, email e frasi brevi. Riceve il testo e la lingua di destinazione, per esempio inglese, arabo, francese o cinese, e restituisce una traduzione fedele del contenuto.",
			'BIB': "Bibliografo. Cerca libri, articoli scientifici, archivi e altre fonti su un argomento di studio o di ricerca, seleziona quelle più rilevanti e aggiornate e prepara la bibliografia con le citazioni nello stile richiesto, per esempio APA, Chicago o MLA. Aiuta chi scrive tesi, articoli, relazioni e rassegne della letteratura.",
			'BAN': "Esperto di bandi. Cerca bandi, finanziamenti, contributi e agevolazioni pubbliche o private per persone, professionisti, imprese, associazioni ed enti di ricerca, come fondi regionali, nazionali, europei o di fondazioni. Verifica chi può partecipare, spiega il regolamento del bando e guida nella preparazione e nella presentazione della domanda.",
			'FO': "Front-office. Accoglie le persone allo sportello, al telefono e via email e dà le informazioni pratiche sul centro: orari di apertura, indirizzi, contatti, appuntamenti, prenotazione di sale e spazi ed eventi in programma. Orienta chi non sa a chi rivolgersi e risponde alle domande generali."
		},
		'noul_q': {
			'MED': "La richiesta va affidata al mediatore culturale?",
			'TRAD': "La richiesta va affidata al traduttore?",
			'BIB': "La richiesta va affidata al bibliografo?",
			'BAN': "La richiesta va affidata all'esperto di bandi?",
			'FO': "La richiesta va affidata al front-office?"
		},
		'score_q': "Quanti agenti servono per gestire la richiesta?",
		'levels': ["Basta il front-office", "Serve un solo specialista", "Servono più specialisti insieme"],
		'state_key': "Richiesta dell'utente",
		'req': [
			"Mi serve la traduzione in inglese del mio contratto di lavoro entro venerdì.",
			"Durante il colloquio con i servizi sociali una madre marocchina si è offesa per alcune domande sulla famiglia e vuole andarsene.",
			"Sto scrivendo la tesi sulla storia del movimento operaio a Torino: mi servono le fonti principali formattate in APA.",
			"C'è un bando regionale per le startup femminili? Vorrei sapere requisiti e scadenza.",
			"A che ora siete aperti domani? Vorrei prendere un appuntamento.",
			"Buongiorno, non so bene a chi rivolgermi, mi può aiutare?",
			"Un signore arrivato dal Pakistan ha ricevuto una lettera della questura in italiano, non la capisce ed è molto agitato perché teme di essere espulso.",
			"Dobbiamo presentare il progetto al bando europeo Erasmus+ e la proposta va scritta in inglese.",
			"Per la domanda al bando PRIN mi serve una sezione sullo stato dell'arte con riferimenti bibliografici aggiornati.",
			"Sono un traduttore freelance e vorrei sapere se esistono finanziamenti pubblici per aprire la partita IVA.",
			"Vorrei prenotare la sala per la presentazione del libro sulla mediazione culturale.",
			"Può tradurmi in arabo questa frase per il cartello dell'ingresso: 'Gli uffici sono chiusi il sabato'?"
		]
	},
	'en': {
		'keys': {'MED': 'cultural_mediator', 'TRAD': 'translator', 'BIB': 'bibliographer', 'BAN': 'grants_expert', 'FO': 'front_office'},
		'route_q': "You are the supervisor of a service desk and coordinate five agents. Which agent do you hand this request to?",
		'desc': {
			'MED': "Cultural mediator. Steps in when a foreign person and a service do not understand each other because of cultural, religious or everyday differences: tension, offence, mistrust or conflict during an interview or at the desk. Explains each side's point of view to the other, accompanies the person in dealing with schools, social services, healthcare and public offices, and calms down delicate situations.",
			'TRAD': "Translator. Translates written texts and documents from one language to another: contracts, letters, certificates, forms, notices, signs, emails and short sentences. Receives the text and the target language, for example English, Arabic, French or Chinese, and returns a faithful translation of the content.",
			'BIB': "Bibliographer. Searches for books, scientific articles, archives and other sources on a study or research topic, selects the most relevant and up-to-date ones and prepares the bibliography with citations in the requested style, for example APA, Chicago or MLA. Helps people writing theses, papers, reports and literature reviews.",
			'BAN': "Grants expert. Searches for calls for proposals, grants, funding and public or private incentives for individuals, freelancers, businesses, associations and research bodies, such as regional, national, European or foundation funds. Checks who is eligible, explains the rules of the call and guides the preparation and submission of the application.",
			'FO': "Front office. Welcomes people at the desk, by phone and by email and gives practical information about the centre: opening hours, addresses, contacts, appointments, bookings of rooms and spaces and upcoming events. Directs people who do not know whom to ask and answers general questions."
		},
		'noul_q': {
			'MED': "Should the request be handed to the cultural mediator?",
			'TRAD': "Should the request be handed to the translator?",
			'BIB': "Should the request be handed to the bibliographer?",
			'BAN': "Should the request be handed to the grants expert?",
			'FO': "Should the request be handed to the front office?"
		},
		'score_q': "How many agents are needed to handle the request?",
		'levels': ["The front office is enough", "One specialist is needed", "Several specialists are needed together"],
		'state_key': "User request",
		'req': [
			"I need my employment contract translated into English by Friday.",
			"During the interview with social services, a Moroccan mother was offended by some questions about her family and wants to leave.",
			"I'm writing my thesis on the history of the labour movement in Turin: I need the main sources formatted in APA.",
			"Is there a regional grant for women-led startups? I'd like to know the requirements and the deadline.",
			"What time are you open tomorrow? I'd like to book an appointment.",
			"Good morning, I'm not sure who to ask, can you help me?",
			"A man who arrived from Pakistan received a letter from the police immigration office in Italian, he doesn't understand it and is very anxious because he fears being deported.",
			"We have to submit our project to the European Erasmus+ call and the proposal must be written in English.",
			"For my PRIN grant application I need a state-of-the-art section with up-to-date bibliographic references.",
			"I'm a freelance translator and I'd like to know whether there is public funding for setting up as self-employed.",
			"I'd like to book the room for the presentation of the book on cultural mediation.",
			"Can you translate this sentence into Arabic for the sign at the entrance: 'The offices are closed on Saturdays'?"
		]
	}
}


def post(body):
	req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
	t0 = time.perf_counter()
	with urllib.request.urlopen(req, timeout=600) as r:
		out = json.load(r)
	return out, (time.perf_counter() - t0) * 1000


def top_agent(probs, key_to_ag):
	k = max(probs, key=probs.get)
	return key_to_ag[k], probs[k]


def run_lang(lang):
	c = L[lang]
	key_to_ag = {v: k for k, v in c['keys'].items()}
	rows = []
	for i, text in enumerate(c['req']):
		state = {c['state_key']: text}
		long_crit = {c['keys'][a]: c['desc'][a] for a in AG}
		questions = {
			'route_long': {'type': 'choice', 'instructions': c['route_q'], 'criteria': long_crit},
			'route_long_rev': {'type': 'choice', 'instructions': c['route_q'], 'criteria': {c['keys'][a]: c['desc'][a] for a in reversed(AG)}},
			'route_short': {'type': 'choice', 'instructions': c['route_q'], 'criteria': {c['keys'][a]: None for a in AG}},
			'n_agents': {'type': 'score', 'instructions': c['score_q'], 'criteria': c['levels']}
		}
		for a in AG:
			questions['noul_' + a] = {'type': 'noul', 'instructions': c['noul_q'][a]}
		res, ms = post({'model': 'Winnow-12B', 'state': state, 'questions': questions})
		A = res['answers']
		row = {'i': i + 1, 'exp': EXP[i], 'ms': round(ms)}
		for q in ('route_long', 'route_long_rev', 'route_short'):
			ag, p = top_agent(A[q]['probabilities'], key_to_ag)
			row[q] = {'top': ag, 'p': round(p, 3), 'ok': ag in EXP[i]}
		nouls = {a: round(A['noul_' + a]['noul'], 3) for a in AG}
		best = max(nouls, key=nouls.get)
		row['noul'] = nouls
		row['noul_top'] = {'top': best, 'ok': best in EXP[i]}
		row['noul_yes'] = [a for a in AG if nouls[a] >= 0.5]
		row['score'] = round(A['n_agents']['score'], 2)
		row['score_exp'] = EXP_SCORE[i]
		rows.append(row)
		print(lang, row['i'], row['route_long']['top'], row['route_long']['p'], 'ok' if row['route_long']['ok'] else 'KO', f"{ms:.0f}ms", flush=True)
	return rows


if __name__ == '__main__':
	results = {lang: run_lang(lang) for lang in ('it', 'en')}
	summary = {}
	for lang, rows in results.items():
		summary[lang] = {
			'route_long': sum(r['route_long']['ok'] for r in rows),
			'route_long_rev': sum(r['route_long_rev']['ok'] for r in rows),
			'order_flips': sum(r['route_long']['top'] != r['route_long_rev']['top'] for r in rows),
			'route_short': sum(r['route_short']['ok'] for r in rows),
			'noul_top': sum(r['noul_top']['ok'] for r in rows),
			'score_round_ok': sum(round(r['score']) == r['score_exp'] for r in rows),
			'median_ms': sorted(r['ms'] for r in rows)[len(rows) // 2]
		}
	json.dump({'summary': summary, 'results': results}, open(OUT, 'w'), indent=1, ensure_ascii=False)
	print(json.dumps(summary, indent=1))
