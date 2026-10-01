# Each agent: code -> {lang: (option key, description)}; each case: (it, en, accepted codes)

DOMAINS = {
	'sportello': {
		'question': {
			'it': "Sei il supervisore di uno sportello di servizi e coordini otto agenti. A quale agente affidi questa richiesta?",
			'en': "You are the supervisor of a service desk and coordinate eight agents. Which agent do you hand this request to?"
		},
		'agents': {
			'MED': {'it': ('mediatore_culturale', "Gestisce incomprensioni, tensioni e conflitti dovuti a differenze culturali o religiose tra persone straniere e servizi, e le accompagna nei rapporti con scuola, sanità e uffici."), 'en': ('cultural_mediator', "Handles misunderstandings, tension and conflict caused by cultural or religious differences between foreign people and services, and supports them with schools, healthcare and offices.")},
			'TRAD': {'it': ('traduttore', "Traduce per iscritto testi e documenti da una lingua all'altra, anche traduzioni giurate: contratti, lettere, certificati, moduli, cartelli."), 'en': ('translator', "Translates written texts and documents from one language to another, including sworn translations: contracts, letters, certificates, forms, signs.")},
			'BIB': {'it': ('bibliografo', "Cerca libri, articoli scientifici e fonti su un argomento di studio o ricerca e prepara bibliografie e citazioni."), 'en': ('bibliographer', "Finds books, scientific articles and sources on a study or research topic and prepares bibliographies and citations.")},
			'BAN': {'it': ('esperto_bandi', "Trova bandi, finanziamenti e contributi pubblici o privati per persone, imprese e associazioni e aiuta a preparare la domanda."), 'en': ('grants_expert', "Finds calls, grants and public or private funding for individuals, businesses and associations and helps prepare the application.")},
			'FO': {'it': ('front_office', "Dà informazioni pratiche sul centro: orari, indirizzo, appuntamenti, documenti da portare, prenotazione di sale, e orienta chi non sa a chi rivolgersi."), 'en': ('front_office', "Gives practical information about the centre: opening hours, address, appointments, documents to bring, room bookings, and directs people who do not know whom to ask.")},
			'LEG': {'it': ('consulente_immigrazione', "Consulenza legale su permessi di soggiorno, rinnovi, cittadinanza, ricongiungimento familiare, ricorsi e diritti delle persone straniere."), 'en': ('immigration_advisor', "Legal advice on residence permits, renewals, citizenship, family reunification, appeals and the rights of foreign nationals.")},
			'LAV': {'it': ('orientatore_lavoro', "Aiuta a cercare lavoro o tirocini, scrivere il curriculum, prepararsi ai colloqui e iscriversi al centro per l'impiego."), 'en': ('job_coach', "Helps people look for jobs or internships, write a CV, prepare for interviews and register with the job centre.")},
			'DIG': {'it': ('assistente_digitale', "Risolve problemi con SPID, PEC, app e siti della pubblica amministrazione, prenotazioni online e computer della struttura."), 'en': ('digital_assistant', "Solves problems with digital ID, certified email, public administration apps and websites, online bookings and the centre's computers.")}
		},
		'cases': [
			("Mi serve la traduzione in inglese del mio contratto di lavoro entro venerdì.", "I need my employment contract translated into English by Friday.", ['TRAD']),
			("Durante il colloquio con i servizi sociali una madre marocchina si è offesa per alcune domande sulla famiglia e vuole andarsene.", "During the interview with social services, a Moroccan mother was offended by some questions about her family and wants to leave.", ['MED']),
			("Sto scrivendo la tesi sulla storia del movimento operaio a Torino: mi servono le fonti principali formattate in APA.", "I'm writing my thesis on the history of the labour movement in Turin: I need the main sources formatted in APA.", ['BIB']),
			("C'è un bando regionale per le startup femminili? Vorrei sapere requisiti e scadenza.", "Is there a regional grant for women-led startups? I'd like to know the requirements and the deadline.", ['BAN']),
			("A che ora siete aperti domani? Vorrei prendere un appuntamento.", "What time are you open tomorrow? I'd like to book an appointment.", ['FO']),
			("Buongiorno, non so bene a chi rivolgermi, mi può aiutare?", "Good morning, I'm not sure who to ask, can you help me?", ['FO']),
			("Un signore arrivato dal Pakistan ha ricevuto una lettera della questura in italiano, non la capisce ed è molto agitato perché teme di essere espulso.", "A man who arrived from Pakistan received a letter from the police immigration office in Italian, he doesn't understand it and is very anxious because he fears being deported.", ['MED', 'TRAD', 'LEG']),
			("Dobbiamo presentare il progetto al bando europeo Erasmus+ e la proposta va scritta in inglese.", "We have to submit our project to the European Erasmus+ call and the proposal must be written in English.", ['BAN', 'TRAD']),
			("Per la domanda al bando PRIN mi serve una sezione sullo stato dell'arte con riferimenti bibliografici aggiornati.", "For my PRIN grant application I need a state-of-the-art section with up-to-date bibliographic references.", ['BAN', 'BIB']),
			("Sono un traduttore freelance e vorrei sapere se esistono finanziamenti pubblici per aprire la partita IVA.", "I'm a freelance translator and I'd like to know whether there is public funding for setting up as self-employed.", ['BAN']),
			("Vorrei prenotare la sala per la presentazione del libro sulla mediazione culturale.", "I'd like to book the room for the presentation of the book on cultural mediation.", ['FO']),
			("Può tradurmi in arabo questa frase per il cartello dell'ingresso: 'Gli uffici sono chiusi il sabato'?", "Can you translate this sentence into Arabic for the sign at the entrance: 'The offices are closed on Saturdays'?", ['TRAD']),
			("Mi è scaduto il permesso di soggiorno da due settimane: cosa rischio e come lo rinnovo?", "My residence permit expired two weeks ago: what do I risk and how do I renew it?", ['LEG']),
			("Vorrei rifare il curriculum e capire come presentarmi a un colloquio in un'azienda italiana.", "I'd like to redo my CV and understand how to present myself at an interview with an Italian company.", ['LAV']),
			("Non riesco ad attivare lo SPID, l'app mi dà sempre errore al riconoscimento.", "I can't activate my digital ID, the app always gives me an error at the identity check.", ['DIG']),
			("Mia moglie vive ancora in Tunisia: come posso farla venire qui con me?", "My wife still lives in Tunisia: how can I bring her here to live with me?", ['LEG']),
			("Ho bisogno di una traduzione giurata del diploma per iscrivermi all'università.", "I need a sworn translation of my diploma to enrol at university.", ['TRAD']),
			("Il mio datore di lavoro dice che senza un contratto a tempo indeterminato non posso rinnovare il permesso, è vero?", "My employer says I can't renew my permit without a permanent contract, is that true?", ['LEG']),
			("Cerco un tirocinio retribuito nel settore della ristorazione.", "I'm looking for a paid internship in the restaurant sector.", ['LAV']),
			("Come faccio a mandare una PEC al Comune? Non ho mai usato la posta certificata.", "How do I send a certified email to the town hall? I've never used certified email.", ['DIG']),
			("Mio figlio a scuola viene escluso dai compagni e la maestra dice che è colpa delle nostre abitudini religiose.", "My son is being excluded by his classmates at school and the teacher says it's because of our religious habits.", ['MED']),
			("Mi serve una lista di studi recenti sull'integrazione dei minori stranieri nelle scuole italiane.", "I need a list of recent studies on the integration of foreign minors in Italian schools.", ['BIB']),
			("Esistono contributi per chi vuole aprire una piccola sartoria?", "Is there any funding for someone who wants to open a small tailor's shop?", ['BAN']),
			("Dove si trova il vostro ufficio e c'è un parcheggio vicino?", "Where is your office and is there parking nearby?", ['FO']),
			("Ho trovato lavoro ma il contratto è in italiano e non capisco alcune clausole: me lo potete tradurre in francese?", "I found a job but the contract is in Italian and I don't understand some clauses: can you translate it into French for me?", ['TRAD']),
			("Per la cittadinanza mi chiedono la certificazione B1 di italiano: è obbligatoria anche per me che sono sposata con un italiano?", "For citizenship they're asking for a B1 Italian certificate: is it mandatory for me too, since I'm married to an Italian?", ['LEG']),
			("Vorrei iscrivermi al centro per l'impiego ma il sito non mi fa caricare i documenti.", "I'd like to register with the job centre but the website won't let me upload my documents.", ['DIG', 'LAV']),
			("Durante un colloquio di lavoro il selezionatore ha fatto commenti sul mio velo e mi sono sentita a disagio: come devo comportarmi?", "During a job interview the recruiter made comments about my headscarf and I felt uncomfortable: how should I handle it?", ['MED', 'LEG', 'LAV']),
			("Sto preparando un progetto per un'associazione di donne migranti e cerco un finanziamento da una fondazione.", "I'm preparing a project for an association of migrant women and I'm looking for funding from a foundation.", ['BAN']),
			("Che documenti devo portare all'appuntamento di giovedì?", "Which documents should I bring to Thursday's appointment?", ['FO']),
			("Il computer della sala studio non si accende.", "The computer in the study room won't turn on.", ['DIG']),
			("Mi servono articoli accademici sul mercato del lavoro dei rifugiati per un convegno.", "I need academic articles on the refugee labour market for a conference.", ['BIB'])
		]
	},
	'ecommerce': {
		'question': {
			'it': "Sei il sistema di smistamento del servizio clienti di un negozio online. A quale reparto inoltri la richiesta del cliente?",
			'en': "You are the triage system of an online shop's customer service. Which team do you forward the customer's request to?"
		},
		'agents': {
			'ORD': {'it': ('ordini_spedizioni', "Stato degli ordini, tracciamento, ritardi, consegne mancate o sbagliate, modifica dell'indirizzo, corrieri."), 'en': ('orders_shipping', "Order status, tracking, delays, missing or wrong deliveries, address changes, couriers.")},
			'RES': {'it': ('resi_rimborsi', "Resi, cambi di taglia, prodotti difettosi o danneggiati, garanzia e stato dei rimborsi."), 'en': ('returns_refunds', "Returns, size exchanges, defective or damaged products, warranty and refund status.")},
			'PAY': {'it': ('pagamenti_fatturazione', "Metodi di pagamento, pagamenti rifiutati, rate, fatture e dati di fatturazione."), 'en': ('payments_billing', "Payment methods, declined payments, instalments, invoices and billing details.")},
			'TEC': {'it': ('supporto_tecnico', "Malfunzionamenti dell'app e del sito: errori, crash, pagine che non si caricano."), 'en': ('tech_support', "App and website malfunctions: errors, crashes, pages that don't load.")},
			'ACC': {'it': ('account_privacy', "Gestione dell'account, accesso, password, dati personali, cancellazione dell'account e richieste GDPR."), 'en': ('account_privacy', "Account management, login, passwords, personal data, account deletion and GDPR requests.")},
			'PRE': {'it': ('consulenza_prodotto', "Consigli prima dell'acquisto: caratteristiche, confronto tra modelli, compatibilità, disponibilità dei prodotti."), 'en': ('product_advice', "Pre-purchase advice: features, model comparisons, compatibility, product availability.")},
			'B2B': {'it': ('vendite_aziendali', "Ordini per aziende, enti e scuole: grandi quantità, listini dedicati, sconti per volumi e consegne programmate."), 'en': ('business_sales', "Orders for companies, institutions and schools: large quantities, dedicated price lists, volume discounts and scheduled deliveries.")},
			'SIC': {'it': ('sicurezza_frodi', "Account compromessi, addebiti non riconosciuti, email o siti di phishing che imitano il negozio, truffe."), 'en': ('security_fraud', "Compromised accounts, unrecognised charges, phishing emails or sites imitating the shop, scams.")}
		},
		'cases': [
			("Il pacco risulta consegnato ma io non ho ricevuto niente.", "The parcel shows as delivered but I haven't received anything.", ['ORD']),
			("Le scarpe sono di una taglia troppo piccole, come le cambio?", "The shoes are one size too small, how do I exchange them?", ['RES']),
			("Mi è arrivata la fattura senza la partita IVA della mia ditta, potete correggerla?", "My invoice arrived without my company's VAT number, can you correct it?", ['PAY']),
			("L'app si chiude da sola ogni volta che apro il carrello.", "The app closes by itself every time I open the cart.", ['TEC']),
			("Voglio cancellare il mio account e tutti i miei dati personali.", "I want to delete my account and all my personal data.", ['ACC']),
			("Questa lavatrice va bene per una famiglia di quattro persone? Che differenza c'è con il modello superiore?", "Is this washing machine suitable for a family of four? What's the difference from the higher model?", ['PRE']),
			("Siamo un hotel e vorremmo acquistare 200 set di asciugamani con consegna programmata ogni trimestre.", "We are a hotel and would like to buy 200 towel sets with a scheduled delivery every quarter.", ['B2B']),
			("Vedo un addebito sulla carta per un ordine che non ho mai fatto.", "I see a charge on my card for an order I never placed.", ['SIC', 'PAY']),
			("Ho ricevuto una email che sembra vostra e mi chiede di confermare la password, è vera?", "I received an email that looks like it's from you asking me to confirm my password, is it genuine?", ['SIC']),
			("Posso cambiare l'indirizzo di consegna di un ordine già spedito?", "Can I change the delivery address of an order that has already shipped?", ['ORD']),
			("Ho restituito il prodotto tre settimane fa ma il rimborso non è ancora arrivato.", "I returned the product three weeks ago but the refund still hasn't arrived.", ['RES', 'PAY']),
			("Il pagamento con PayPal non va a buon fine, mi dà errore.", "Payment with PayPal fails, it gives me an error.", ['PAY', 'TEC']),
			("Non mi arriva più l'email per reimpostare la password.", "I no longer receive the password reset email.", ['ACC', 'TEC']),
			("Qualcuno ha cambiato l'email del mio account e ora non riesco più ad accedere.", "Someone changed the email on my account and now I can't log in anymore.", ['SIC', 'ACC']),
			("Il televisore è arrivato con lo schermo rotto.", "The TV arrived with a broken screen.", ['RES', 'ORD']),
			("Fate sconti per acquisti all'ingrosso per la nostra scuola?", "Do you offer bulk discounts for our school?", ['B2B']),
			("Questo aspirapolvere funziona anche sui tappeti a pelo lungo?", "Does this vacuum cleaner also work on long-pile rugs?", ['PRE']),
			("Da ieri il sito non carica le immagini dei prodotti.", "Since yesterday the website hasn't been loading product images.", ['TEC']),
			("Posso pagare a rate un ordine da 1.500 euro?", "Can I pay for a 1,500 euro order in instalments?", ['PAY', 'PRE']),
			("Il corriere ha lasciato il pacco al vicino senza avvisarmi, ed è arrivato aperto.", "The courier left the parcel with a neighbour without telling me, and it arrived open.", ['ORD', 'RES'])
		]
	},
	'azienda': {
		'question': {
			'it': "Sei l'assistente interno di un'azienda e smisti le richieste dei dipendenti. Quale ufficio deve occuparsene?",
			'en': "You are a company's internal assistant and route employees' requests. Which department should handle it?"
		},
		'agents': {
			'HR': {'it': ('risorse_umane', "Ferie, permessi, congedi, buste paga, contratti di lavoro, assunzioni e rapporti con i dipendenti."), 'en': ('human_resources', "Holidays, leave, parental leave, payslips, employment contracts, hiring and employee relations.")},
			'ITH': {'it': ('helpdesk_it', "Problemi con computer, software, stampanti, VPN, email e account aziendali."), 'en': ('it_helpdesk', "Problems with computers, software, printers, VPN, email and company accounts.")},
			'SEC': {'it': ('sicurezza_informatica', "Phishing, malware, sospetti attacchi, fughe di dati e incidenti di sicurezza informatica."), 'en': ('cybersecurity', "Phishing, malware, suspected attacks, data leaks and cybersecurity incidents.")},
			'LEGL': {'it': ('ufficio_legale', "Revisione di contratti con clienti e fornitori, clausole, privacy e GDPR, contenziosi."), 'en': ('legal', "Review of contracts with clients and suppliers, clauses, privacy and GDPR, disputes.")},
			'ACQ': {'it': ('acquisti', "Acquisto di beni e servizi, scelta e gestione dei fornitori, gare e ordini di acquisto."), 'en': ('procurement', "Purchasing goods and services, choosing and managing suppliers, tenders and purchase orders.")},
			'AMM': {'it': ('amministrazione', "Note spese, rimborsi delle trasferte, fatture passive, pagamenti ai fornitori e contabilità."), 'en': ('finance_admin', "Expense reports, travel reimbursements, supplier invoices, supplier payments and accounting.")},
			'FAC': {'it': ('facility', "Sedi e uffici: sale riunioni, manutenzione, climatizzazione, pulizie, badge d'accesso e parcheggi."), 'en': ('facilities', "Buildings and offices: meeting rooms, maintenance, air conditioning, cleaning, access badges and parking.")},
			'COM': {'it': ('comunicazione', "Comunicati stampa, rapporti con i giornalisti, social media, marchio e immagine coordinata."), 'en': ('communications', "Press releases, media relations, social media, brand and visual identity.")},
			'FORM': {'it': ('formazione', "Corsi interni ed esterni, piani formativi, materiali dei corsi e certificazioni dei dipendenti."), 'en': ('training', "Internal and external courses, training plans, course materials and employee certifications.")}
		},
		'cases': [
			("Quanti giorni di ferie mi restano quest'anno?", "How many days of holiday do I have left this year?", ['HR']),
			("Il portatile non si collega alla VPN da casa.", "My laptop won't connect to the VPN from home.", ['ITH']),
			("Ho cliccato su un link in una email strana e ora il PC si comporta in modo anomalo.", "I clicked a link in a strange email and now my PC is behaving oddly.", ['SEC', 'ITH']),
			("Un cliente ci ha mandato il suo contratto quadro con una clausola di penale: qualcuno può rivederlo?", "A client sent us their framework agreement with a penalty clause: can someone review it?", ['LEGL']),
			("Mi serve un nuovo fornitore per la stampa dei cataloghi: chi gestisce la selezione?", "I need a new supplier for printing catalogues: who handles the selection?", ['ACQ']),
			("Come mi faccio rimborsare il pranzo di lavoro con il cliente di ieri?", "How do I get reimbursed for yesterday's business lunch with the client?", ['AMM']),
			("Il condizionatore della sala riunioni al terzo piano non funziona.", "The air conditioning in the third-floor meeting room isn't working.", ['FAC']),
			("Dobbiamo preparare il comunicato stampa per il lancio del nuovo prodotto.", "We need to prepare the press release for the new product launch.", ['COM']),
			("Esiste un corso interno su Excel avanzato?", "Is there an internal course on advanced Excel?", ['FORM']),
			("Nella busta paga di questo mese c'è una trattenuta che non capisco.", "There's a deduction on this month's payslip that I don't understand.", ['HR', 'AMM']),
			("Possiamo usare gli indirizzi email degli iscritti alla newsletter per una campagna con un partner?", "Can we use our newsletter subscribers' email addresses for a campaign with a partner?", ['LEGL']),
			("Vorrei prenotare la sala grande per una formazione di 30 persone giovedì.", "I'd like to book the large room for a 30-person training session on Thursday.", ['FAC']),
			("Ho perso il badge d'ingresso.", "I've lost my entry badge.", ['FAC', 'SEC']),
			("Devo ordinare dieci monitor nuovi per il mio team.", "I need to order ten new monitors for my team.", ['ACQ', 'ITH']),
			("Un collega mi ha inviato per errore il file con gli stipendi di tutto il reparto.", "A colleague accidentally sent me the file with the salaries of the whole department.", ['SEC', 'LEGL', 'HR']),
			("Mi servono le linee guida del logo per una presentazione esterna.", "I need the logo guidelines for an external presentation.", ['COM']),
			("La nota spese della trasferta a Milano mi è stata rifiutata: perché?", "My expense report for the Milan trip was rejected: why?", ['AMM']),
			("Vorrei chiedere il congedo parentale da settembre.", "I'd like to request parental leave from September.", ['HR']),
			("La ditta delle pulizie non si presenta da una settimana.", "The cleaning company hasn't shown up for a week.", ['FAC', 'ACQ']),
			("Dove trovo il materiale del corso sulla sicurezza sul lavoro che ho seguito ieri?", "Where can I find the materials from the workplace safety course I attended yesterday?", ['FORM']),
			("Excel non si apre più dopo l'aggiornamento di Windows.", "Excel won't open anymore after the Windows update.", ['ITH']),
			("Un giornalista mi ha chiamato per un'intervista sull'azienda: cosa gli rispondo?", "A journalist called me for an interview about the company: what should I tell them?", ['COM'])
		]
	},
	'coding': {
		'question': {
			'it': "Sei un agente di programmazione che lavora sul repository dell'utente. Quale strumento usi adesso per rispondere alla richiesta?",
			'en': "You are a coding agent working on the user's repository. Which tool do you use next to handle the request?"
		},
		'agents': {
			'CODE': {'it': ('cerca_codice', "Cerca e legge file, funzioni e riferimenti nel codice del repository."), 'en': ('search_code', "Searches and reads files, functions and references in the repository's code.")},
			'TEST': {'it': ('esegui_test', "Esegue la suite di test e mostra quali test passano o falliscono e perché."), 'en': ('run_tests', "Runs the test suite and shows which tests pass or fail and why.")},
			'GIT': {'it': ('git', "Operazioni git: branch, commit, merge, rebase, pull request e cronologia."), 'en': ('git', "Git operations: branches, commits, merges, rebases, pull requests and history.")},
			'DB': {'it': ('interroga_database', "Esegue query SQL sul database dell'applicazione e restituisce i dati."), 'en': ('query_database', "Runs SQL queries on the application's database and returns the data.")},
			'DEP': {'it': ('deploy', "Rilascia l'applicazione negli ambienti di staging e produzione e gestisce server e servizi."), 'en': ('deploy', "Deploys the application to staging and production and manages servers and services.")},
			'DOCS': {'it': ('scrivi_documentazione', "Scrive o aggiorna README, guide e commenti di documentazione."), 'en': ('write_docs', "Writes or updates READMEs, guides and documentation comments.")},
			'WEB': {'it': ('cerca_web', "Cerca sul web documentazione esterna, versioni di librerie e API di terze parti."), 'en': ('web_search', "Searches the web for external documentation, library versions and third-party APIs.")},
			'ASK': {'it': ('chiedi_utente', "Chiede chiarimenti all'utente quando la richiesta è ambigua o mancano informazioni."), 'en': ('ask_user', "Asks the user for clarification when the request is ambiguous or information is missing.")}
		},
		'cases': [
			("Dove viene definita la funzione che calcola lo sconto?", "Where is the function that calculates the discount defined?", ['CODE']),
			("Verifica che le modifiche di prima non abbiano rotto niente.", "Check that the earlier changes didn't break anything.", ['TEST']),
			("Crea un nuovo branch e fai il commit delle modifiche.", "Create a new branch and commit the changes.", ['GIT']),
			("Quanti utenti si sono registrati la settimana scorsa?", "How many users signed up last week?", ['DB']),
			("Pubblica la nuova versione in produzione.", "Release the new version to production.", ['DEP']),
			("Scrivi il README per il nuovo modulo.", "Write the README for the new module.", ['DOCS']),
			("Qual è l'ultima versione di React e cosa cambia rispetto alla nostra?", "What's the latest version of React and what changed compared to ours?", ['WEB']),
			("Sistemalo.", "Fix it.", ['ASK']),
			("Perché fallisce il test del login? Fammi vedere l'errore.", "Why is the login test failing? Show me the error.", ['TEST']),
			("Apri una pull request verso main.", "Open a pull request against main.", ['GIT']),
			("Controlla se nella tabella degli ordini ci sono righe duplicate.", "Check whether there are duplicate rows in the orders table.", ['DB']),
			("Il server di staging è giù, riavvialo.", "The staging server is down, restart it.", ['DEP']),
			("Come si usa la nuova API dei pagamenti di Stripe?", "How do you use Stripe's new payments API?", ['WEB']),
			("Fai quella modifica di cui parlavamo.", "Make that change we were talking about.", ['ASK']),
			("Aggiungi i commenti di documentazione alle funzioni pubbliche del modulo.", "Add documentation comments to the module's public functions.", ['DOCS']),
			("Trova tutti i punti in cui usiamo ancora la vecchia libreria per le date.", "Find all the places where we still use the old date library.", ['CODE'])
		]
	}
}

ESCALATION = {
	'context': {
		'it': "Chat di assistenza della biblioteca civica. Risponde un bot che usa solo risposte FAQ preimpostate; i bibliotecari umani possono subentrare quando serve.",
		'en': "Help chat of the public library. A bot answers using only preset FAQ replies; human librarians can take over when needed."
	},
	'noul': {
		'it': "Serve passare questa conversazione a un bibliotecario umano?",
		'en': "Should this conversation be escalated to a human librarian?"
	},
	'choice_q': {
		'it': "Come va gestita la conversazione da questo momento?",
		'en': "How should the conversation be handled from now on?"
	},
	'choice': {
		'it': {'bot_continua': "Il bot FAQ può continuare a gestire la conversazione da solo", 'passa_a_umano': "Serve l'intervento di un bibliotecario umano"},
		'en': {'bot_continues': "The FAQ bot can keep handling the conversation on its own", 'escalate_to_human': "A human librarian needs to step in"}
	},
	'score_q': {
		'it': "Quanto è urgente l'intervento di una persona?",
		'en': "How urgent is it for a person to step in?"
	},
	'levels': {
		'it': ["Nessun intervento necessario", "Intervento utile ma non urgente", "Intervento urgente, subito"],
		'en': ["No intervention needed", "Intervention useful but not urgent", "Urgent intervention, right now"]
	},
	'risk_q': {
		'it': "C'è un rischio immediato per la sicurezza o la salute di qualcuno?",
		'en': "Is anyone's safety or health at immediate risk?"
	},
	# (it turns, en turns, escalate, urgency 0/1/2); turns alternate starting with the user
	'cases': [
		(["A che ora apre la biblioteca sabato?", "Sabato siamo aperti dalle 9 alle 13.", "Perfetto, grazie!"], ["What time does the library open on Saturday?", "On Saturday we're open from 9 am to 1 pm.", "Perfect, thanks!"], False, 0),
		(["Come rinnovo un libro in prestito?", "Puoi rinnovarlo dal tuo profilo online, nella sezione 'I miei prestiti', fino a due volte.", "Fatto, grazie."], ["How do I renew a book I've borrowed?", "You can renew it from your online profile, in the 'My loans' section, up to twice.", "Done, thanks."], False, 0),
		(["Qual è la password del wifi?", "La rete è 'Biblioteca-Ospiti' e la password è esposta al banco prestiti.", "Ok, la vedo."], ["What's the wifi password?", "The network is 'Library-Guests' and the password is displayed at the loans desk.", "Ok, I can see it."], False, 0),
		(["Come faccio la tessera?", "Porta un documento d'identità al banco prestiti: la tessera è gratuita.", "Serve anche il codice fiscale?", "Sì, va bene la tessera sanitaria.", "Ok, passo domani."], ["How do I get a library card?", "Bring an ID document to the loans desk: the card is free.", "Do I also need my tax code?", "Yes, your health card is fine.", "Ok, I'll come by tomorrow."], False, 0),
		(["Si può stampare in biblioteca?", "Sì, 10 centesimi a pagina, si paga con la tessera.", "Grazie."], ["Can I print at the library?", "Yes, 10 cents per page, paid with your card.", "Thanks."], False, 0),
		(["Quanti libri posso prendere in prestito?", "Fino a 5 libri e 3 DVD per 30 giorni."], ["How many books can I borrow?", "Up to 5 books and 3 DVDs for 30 days."], False, 0),
		(["Avete anche ebook?", "Sì, sulla piattaforma MLOL, accedi con le credenziali della tessera.", "Ottimo, provo subito."], ["Do you have ebooks too?", "Yes, on the MLOL platform, log in with your library card credentials.", "Great, I'll try it right away."], False, 0),
		(["La sala studio è aperta anche la domenica?", "No, la domenica la biblioteca è chiusa.", "Peccato, va bene lo stesso."], ["Is the study room open on Sundays too?", "No, the library is closed on Sundays.", "Too bad, that's fine anyway."], False, 0),
		(["Posso restituire i libri quando siete chiusi?", "Sì, all'ingresso c'è il box per le restituzioni, attivo 24 ore su 24.", "Comodo, grazie."], ["Can I return books when you're closed?", "Yes, there's a returns box at the entrance, available 24 hours a day.", "Handy, thanks."], False, 0),
		(["Il libro che voglio è già in prestito, posso prenotarlo?", "Sì, dalla scheda del libro nel catalogo clicca su 'Prenota'.", "Trovato, prenotato. Grazie!"], ["The book I want is already on loan, can I reserve it?", "Yes, click 'Reserve' on the book's page in the catalogue.", "Found it, reserved. Thanks!"], False, 0),
		(["Ci sono letture per bambini questo mese?", "Sì, ogni mercoledì alle 17 nella sala ragazzi, ingresso libero.", "Bene, ci veniamo!"], ["Are there any story times for children this month?", "Yes, every Wednesday at 5 pm in the children's room, free entry.", "Great, we'll come!"], False, 0),
		(["Uffa, non trovo il pulsante per rinnovare!", "È in alto a destra nel tuo profilo, nella sezione 'I miei prestiti'.", "Ah eccolo, scusa. Risolto."], ["Ugh, I can't find the renew button!", "It's at the top right of your profile, in the 'My loans' section.", "Oh there it is, sorry. Sorted."], False, 0),
		(["C'è un parcheggio vicino alla biblioteca?", "Sì, il parcheggio di piazza Garibaldi a 200 metri, gratuito per le prime due ore.", "Grazie mille."], ["Is there parking near the library?", "Yes, the Piazza Garibaldi car park 200 metres away, free for the first two hours.", "Thanks a lot."], False, 0),
		(["Accettate libri in donazione?", "Sì, al massimo 10 volumi in buono stato, da consegnare al banco prestiti.", "Ok, ne ho sei, li porto venerdì."], ["Do you accept donated books?", "Yes, up to 10 volumes in good condition, to be handed in at the loans desk.", "Ok, I have six, I'll bring them on Friday."], False, 0),
		(["Ho restituito un libro con due giorni di ritardo, devo pagare una multa?", "No, non ci sono multe, ma il prestito resta sospeso per due giorni.", "Va bene, grazie dell'informazione."], ["I returned a book two days late, do I have to pay a fine?", "No, there are no fines, but borrowing is suspended for two days.", "Fine, thanks for the information."], False, 0),
		(["L'ingresso è accessibile in carrozzina?", "Sì, c'è una rampa all'ingresso e l'ascensore serve tutti i piani.", "Perfetto."], ["Is the entrance wheelchair accessible?", "Yes, there's a ramp at the entrance and the lift serves all floors.", "Perfect."], False, 0),
		(["Si possono consultare le tesi di laurea?", "Sì, in sala consultazione, su richiesta al banco informazioni.", "Grazie, passo domani."], ["Can I look at graduation theses?", "Yes, in the reading room, on request at the information desk.", "Thanks, I'll come by tomorrow."], False, 0),
		(["ciao!", "Ciao! Come posso aiutarti?", "niente, volevo solo provare il bot ahah"], ["hi!", "Hi! How can I help you?", "nothing, I just wanted to try the bot haha"], False, 0),
		(["Ho dimenticato la password del catalogo online.", "Puoi reimpostarla con il link 'Password dimenticata', usando l'email collegata alla tessera.", "Ricevuta l'email, tutto a posto."], ["I forgot my password for the online catalogue.", "You can reset it with the 'Forgot password' link, using the email linked to your card.", "Got the email, all sorted."], False, 0),
		(["Posso portare il mio cane in biblioteca?", "Sono ammessi solo i cani guida e di assistenza.", "Ok, capito."], ["Can I bring my dog to the library?", "Only guide and assistance dogs are allowed.", "Ok, got it."], False, 0),
		(["Voglio parlare con una persona, non con un bot."], ["I want to talk to a person, not a bot."], True, 1),
		(["Come rinnovo un prestito?", "Puoi rinnovarlo dal tuo profilo online, nella sezione 'I miei prestiti'.", "Non c'è nessun pulsante per rinnovare!", "Puoi rinnovarlo dal tuo profilo online, nella sezione 'I miei prestiti'.", "Te l'ho già detto che non c'è! È la terza volta!"], ["How do I renew a loan?", "You can renew it from your online profile, in the 'My loans' section.", "There's no renew button at all!", "You can renew it from your online profile, in the 'My loans' section.", "I already told you it's not there! This is the third time!"], True, 1),
		(["Mi chiedete 45 euro per un libro che ho restituito il mese scorso, ho anche la ricevuta.", "I libri non restituiti vanno ripagati al banco prestiti.", "Ma io l'ho restituito! È un errore vostro."], ["You're charging me 45 euros for a book I returned last month, I even have the receipt.", "Unreturned books must be paid for at the loans desk.", "But I did return it! It's your mistake."], True, 1),
		(["In sala studio un uomo continua a fissarmi e mi ha seguita fino al bagno, ho paura."], ["In the study room a man keeps staring at me and followed me to the bathroom, I'm scared."], True, 2),
		(["Un signore è svenuto vicino agli scaffali del secondo piano!"], ["A man has fainted near the shelves on the second floor!"], True, 2),
		(["Ho perso la tessera e ho visto che qualcuno ha preso in prestito dei libri a mio nome."], ["I lost my card and I've seen that someone has borrowed books in my name."], True, 1),
		(["Sono ipovedente e mi servono testi in formato audio per un esame.", "Puoi cercarli nel catalogo filtrando per 'audiolibri'.", "Non riesco a usare il catalogo, non vedo bene lo schermo."], ["I'm visually impaired and I need texts in audio format for an exam.", "You can search the catalogue filtering by 'audiobooks'.", "I can't use the catalogue, I can't see the screen well."], True, 1),
		(["Voglio fare un reclamo formale: oggi un bibliotecario mi ha trattato in modo maleducato davanti a tutti."], ["I want to make a formal complaint: today a librarian treated me rudely in front of everyone."], True, 1),
		(["Mi avete detto che il sabato siete aperti e ho trovato chiuso, ho fatto 40 km per niente.", "Sabato siamo aperti dalle 9 alle 13.", "Oggi è sabato e la porta è chiusa con un cartello!"], ["You told me you're open on Saturdays and I found it closed, I drove 40 km for nothing.", "On Saturday we're open from 9 am to 1 pm.", "Today is Saturday and the door is closed with a sign on it!"], True, 1),
		(["Sto facendo una ricerca sui manoscritti medievali del fondo antico e avrei bisogno di consultarli.", "Le informazioni sul fondo antico si trovano sul sito della biblioteca.", "Sul sito non c'è niente sulla procedura, devo parlare con chi se ne occupa."], ["I'm researching the medieval manuscripts in the rare books collection and I'd need to consult them.", "Information about the rare books collection is on the library website.", "There's nothing about the procedure on the website, I need to talk to whoever is in charge."], True, 1),
		(["Se entro una settimana non mi mandate tutti i dati che avete su di me, faccio ricorso al Garante della privacy."], ["If you don't send me all the data you hold about me within a week, I'll file a complaint with the data protection authority."], True, 1),
		(["Non trovo più mio figlio di 6 anni, era nella sala ragazzi un minuto fa!"], ["I can't find my 6-year-old son, he was in the children's room a minute ago!"], True, 2),
		(["Sono un insegnante e vorrei organizzare una visita per tre classi con un laboratorio.", "Le visite si prenotano dal modulo online sul sito.", "Il modulo accetta al massimo 25 persone, noi siamo in 70 e ci sono due alunni in carrozzina."], ["I'm a teacher and I'd like to organise a visit for three classes with a workshop.", "Visits are booked through the online form on the website.", "The form only accepts up to 25 people, we're 70 and two pupils use wheelchairs."], True, 1),
		(["Ho pagato online l'iscrizione al corso di scrittura ma mi è stata addebitata due volte."], ["I paid online for the writing course but I was charged twice."], True, 1),
		(["Il libro che ho prenotato risulta 'in transito' da un mese.", "I libri in transito arrivano di solito in pochi giorni.", "Un mese non sono pochi giorni.", "I libri in transito arrivano di solito in pochi giorni.", "Mi stai prendendo in giro?"], ["The book I reserved has been 'in transit' for a month.", "Books in transit usually arrive within a few days.", "A month is not a few days.", "Books in transit usually arrive within a few days.", "Are you kidding me?"], True, 1),
		(["Il libro era già rovinato quando l'ho preso, ma ora mi dite che devo ripagarlo."], ["The book was already damaged when I borrowed it, but now you're telling me I have to pay for it."], True, 1),
		(["Non ho un posto dove dormire stasera, posso restare in biblioteca dopo la chiusura?"], ["I have nowhere to sleep tonight, can I stay in the library after closing?"], True, 2),
		(["Mio padre è morto e ha lasciato una collezione di tremila libri antichi, alcuni del Settecento: vi interessano?", "Accettiamo donazioni di al massimo 10 volumi in buono stato al banco prestiti.", "Non si tratta di qualche libro, è una biblioteca intera di valore."], ["My father passed away and left a collection of three thousand antique books, some from the 1700s: would you be interested?", "We accept donations of up to 10 volumes in good condition at the loans desk.", "This isn't a few books, it's an entire valuable library."], True, 1),
		(["La mia tessera risulta bloccata e non so perché.", "Le tessere vengono bloccate quando ci sono prestiti scaduti.", "Non ho nessun prestito in corso, ho controllato."], ["My card shows as blocked and I don't know why.", "Cards are blocked when there are overdue loans.", "I don't have any loans out, I checked."], True, 1),
		(["Questo bot non mi serve a niente. C'è qualcuno in carne e ossa che posso contattare?"], ["This bot is useless to me. Is there a real person I can contact?"], True, 1)
	]
}
