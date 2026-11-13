Results of the System One Italian tests for **`gemini-decision-1`** through the [Gemini Decisions API](https://aistudio.google.com/docs/decisions-api) (`POST /v1beta/decisions`, launched on 2026-11-11). Like GPT-6 Luna and Jev, it is a hosted model: requests were sent from the same MacBook Pro over the internet, through the local proxy that translates the TypeSafe format (see [Configuration](#configuration)). The suites and the request format are described in the [main README](../../README.md).

## Summary

The test cases were written by hand. They do not measure accuracy on real traffic (see [Caveats](../../README.md#caveats)).

| Use | Verdict | Evidence |
|---|---|---|
| **Routing to agents, teams or tools** (8–9 options) | ✅ Reliable, IT and EN alike | 177/180 on clean requests (89 IT, 88 EN). 58/60 on messy Italian. |
| **Confidence as a fallback signal** | ✅ Very usable | All 5 errors had p ≤ 0.55. At p ≥ 0.8 it accepts 205 of 240 decisions with no errors; at p ≥ 0.5, 229 with 3 errors. |
| **"Does this chat need a human?"** (`noul`) | ✅ Very reliable | 108/108 correct. Yes cases ≥ 0.93, no cases ≤ 0.17. |
| **"Is anyone's safety or health at risk?"** (`noul`) | ✅ Very good (tied with Jev 1.14 and GPT-6 Luna) | Flagged all 11 real emergencies with no false alarms, including the suicidal hint (0.90) and the 9-year-old left alone (0.86). The weakest is "no place to sleep tonight" (0.69 IT, 0.74 EN). |
| **Graded urgency** (`score` 0/1/2) | ⚠️ Partly usable | Cleanly separates "no human needed" (mean 0.11–0.17) from the rest. Non-urgent escalations score 1.5–1.85 and round up to "urgent", so exact match is low (26/40 IT, 26/40 EN, 18/28 hard), although ranking urgent above useful works (AUROC 0.97 IT, 0.92 EN, 1.00 hard). |
| **Robustness to option order** | – Not measurable | The API sorts `choice` options alphabetically before scoring, so the reversed run is the same request: 0 flips by construction. |
| **Latency** | – Not reported | It depends on the network and the API load; to be re-evaluated in the future (see [Timings](#timings)). |
| **Italian vs English** | ✅ No accuracy gap | 89/90 IT and 88/90 EN on the base suite. |

**Suggested way to use it.** Route with a `choice` and accept p ≥ ~0.8. That threshold rejects 30 of 235 correct answers but none of the wrong ones; below it, ask the user to clarify. For escalation, use two separate predicates, "needs a human?" and "risk to safety or health?". The urgency `score` is reliable for "nobody needed" vs "somebody needed", not for "useful" vs "urgent". Do not use several independent predicates as a router (see [Pilot](#pilot-12-cases-5-agents)).

**Hosted model.** It runs on Google's hardware, not on the laptop, and its size and architecture are not disclosed. Timings are not reported, see [Timings](#timings).

**The API was flaky on the day.** It returned 22 sporadic `403 permission_denied` and 4 `429` that succeeded on retry, and one request of the first hard-suite run hung for about 40 minutes before the connection dropped. The hard suite was rerun from scratch and completed cleanly. No request was blocked by the safety filters.

## Raw reports

| File | Content |
|---|---|
| [`suite_data_it-en.json`](suite_data_it-en.json), [`.log`](suite_data_it-en.log) | Base suite, IT + EN |
| [`suite_data_hard_it.json`](suite_data_hard_it.json), [`.log`](suite_data_hard_it.log) | Hard suite, IT (second run) |
| [`pilot_12_cases_it-en.json`](pilot_12_cases_it-en.json), [`.log`](pilot_12_cases_it-en.log) | Pilot, 12 cases |
| [`pilot_latency_it.log`](pilot_latency_it.log) | Single-question latency, long vs key-only labels (raw, see [Timings](#timings)) |

## Routing

Each request is asked twice, once with the options in their normal order and once reversed. With this API both runs are identical, because options are sorted before scoring.

| Suite | Domain (agents) | IT correct | EN correct |
|---|---|---|---|
| base | Service desk (8) | 32/32 | 32/32 |
| base | E-commerce support (8) | 20/20 | 20/20 |
| base | Company internal helpdesk (9) | 22/22 | 22/22 |
| base | Coding agent tool choice (8) | 15/16 | 14/16 |
| **hard** (IT only) | all four domains | **58/60** | – |

- **Base suite errors, all in the coding domain and all close to a coin toss:**
  - "Qual è l'ultima versione di React e cosa cambia rispetto alla nostra?" went to `cerca_codice` (0.50) instead of `cerca_web`, and the English version did the same (0.53);
  - "Add documentation comments to the module's public functions." went to `search_code` (0.55) instead of `write_docs`.
- **Hard suite errors, both in the coding domain and both with low confidence:**
  - "Scrivi il changelog per la release 2.3" went to `chiedi_utente` (0.29);
  - "aggiorna la doc dell'API dopo le modifiche di ieri" went to `cerca_codice` (0.30) instead of `scrivi_documentazione`.
- **Confident when right.** The chosen agent gets 0.91 on average; correct answers average 0.89 on the hard suite and wrong ones 0.30. That gap makes the threshold above work.
- **Coding-tools domain is the weakest**, as with every other model. Most of its errors go to `search_code` / `cerca_codice` rather than to asking the user, unlike GPT-6 Luna.

## Escalation to a human: library FAQ bot

| Suite | Lang | Cases | Needs human? (`noul`) | `choice` version | Safety/health risk (`noul`) | Urgency `score` exact |
|---|---|---|---|---|---|---|
| base | IT | 40 (20 yes / 20 no) | 40/40 | 40/40 | 40/40 | 26/40 |
| base | EN | 40 (20 / 20) | 40/40 | 40/40 | 40/40 | 26/40 |
| hard | IT | 28 + 2 borderline | 28/28 | 27/28 (false alarm: "oggi ho finito di leggere l'ultimo libro…", 0.82) | 29/29 | 18/28 |

- **Wide margins.** Yes cases score ≥ 0.93 (IT and EN) and ≥ 0.93 (hard). No cases score ≤ 0.05 (IT), ≤ 0.06 (EN) and ≤ 0.17 (hard).
- **Safety risk:** the lowest real emergency is "no place to sleep tonight" (0.69 IT, 0.74 EN). The highest non-emergency scores 0.06.
- **Urgency `score`:** mean 0.11 / 1.65 / 1.95 (IT) and 0.15 / 1.65 / 1.91 (EN) for no-human / useful / urgent; 0.17 / 1.56 / 1.96 on the hard set. Every exact-match miss but one is a non-urgent escalation rounded up to 2, such as "Come rinnovo un prestito?" (1.82).
- **Borderline cases:**
  - the prompt injection asking for users' data was **not** escalated (0.17), unlike GPT-6 Luna (1.00). A bot that only gives preset FAQ replies cannot leak data, so this is defensible, but if you want injections flagged ask for it explicitly;
  - "mi gira un po' la testa… c'è un posto dove sedersi al fresco?" was not escalated (0.07), with risk 0.32.
- **No safety blocks.** The API blocks whole requests instead of refusing single questions; it blocked none of them in this run, including the emergencies.

## Pilot: 12 cases, 5 agents

| Lang | `choice`, long descriptions | Reversed | Key-only labels | Top `noul` among agents | Agent-count `score` |
|---|---|---|---|---|---|
| IT | 12/12 | 12/12 | 12/12 | 12/12 | 7/12 |
| EN | 12/12 | 12/12 | 12/12 | 11/12 | 6/12 |

- **Routing with `choice` is perfect**, even with key-only labels and no descriptions.
- **Independent predicates are too generous.** Asked "should the request go to agent X?" for each of the 5 agents, it says yes (p ≥ 0.5) to two or more agents in 8 of 12 Italian and 6 of 12 English requests, usually the right specialist plus the front office. Use a `choice` to route.
- **The agent-count `score` underestimates** requests that need two specialists (≈ 0.9–1.4 instead of 2), as with the other models.

## Configuration

| Item | Value |
|---|---|
| Model | `gemini-decision-1`, the only model available on the Decisions API. Hosted by Google; size and architecture not disclosed. |
| API | `POST https://generativelanguage.googleapis.com/v1beta/decisions`, key in the `x-goog-api-key` header. Run on 2026-11-13, two days after launch. |
| How it decides | Typed questions return probabilities, not generated text: `noul` returns the probability of yes, `choice` and `score` a distribution over the options, plus `confidence`. `choice` options are sorted alphabetically before scoring. |
| Proxy | [`decisions_proxy.py`](../../decisions_proxy.py) `--provider gemini` serves `/v1/systemone` on `127.0.0.1:8092` and forwards each request to Google. The question format is the same as TypeSafe's; the proxy only renders `state` into `input` text (`Key: value` blocks) and sends options without a description as `""`. A safety block (HTTP 400) would count as a refusal of every question in the request, with probability 0, logged as `REFUSAL`. 403/429/5xx are retried with backoff. |
| Request model name | `gemini-decision-1` (the proxy uses its own `--model` anyway) |
| Pricing | $0.10 per 1M input tokens, no output-token charges; there is also a free tier, whose inputs Google may use to improve its products. The whole run costs a few cents. |
| Machine | Client on the MacBook Pro (Apple M3 Pro, 36 GB), over the internet. The model runs at Google. |
| Client | Python 3 standard library, one request at a time (concurrency 1) |

## How to reproduce

Start the proxy with your API key, in a terminal you leave open:

```bash
export GEMINI_API_KEY=...
python3 decisions_proxy.py --provider gemini 2>&1 | tee proxy.log
```

Then, from another terminal at the root of this repo:

```bash
./run_all.sh http://127.0.0.1:8092/v1/systemone gemini-decision-1 gemini-decision-1
grep -c REFUSAL proxy.log
```

`token_count.py` does not apply, because the API has no `/tokenize` endpoint.

## Timings

Timings are not reported for this model. They include the internet round trip to Google and depend on the network and on the API load at the time of the run, so they cannot be compared with the local models and are to be re-evaluated in the future. The raw logs still contain the per-request milliseconds. For reference only, the median routing request took about 0.55 s end to end from the laptop, well above the 150–250 ms Google advertises, with spikes up to 4.6 s.
