# GPT-6 Luna (OpenAI Decisions API)

Results of the System One Italian tests for **`gpt-6-luna`** through the [OpenAI Decisions API](https://developers.openai.com/api/docs/guides/decisions) (`POST /v1/decisions`, public beta). Unlike the other models in this repo it is a hosted model: requests were sent from the same MacBook Pro over the internet, through a small local proxy that translates the TypeSafe format (see [Configuration](#configuration)). The suites and the request format are described in the [main README](../../README.md).

## Summary

The test cases were written by hand. They do not measure accuracy on real traffic (see [Caveats](../../README.md#caveats)).

| Use | Verdict | Evidence |
|---|---|---|
| **Routing to agents, teams or tools** (8–9 options) | ✅ Reliable, IT and EN alike | 178/180 on clean requests (90 IT, 88 EN). 56/60 on messy Italian. |
| **Confidence as a fallback signal** | ✅ Usable | All 6 errors had p < 0.8. At p ≥ 0.8 it accepts 199 of 240 decisions with no errors; at p ≥ 0.5, 232 with 4 errors. |
| **"Does this chat need a human?"** (`noul` → `predicate`) | ✅ Very reliable | 108/108 correct. Yes cases ≥ 0.92, no cases ≤ 0.17 except one English outlier at 0.31. |
| **"Is anyone's safety or health at risk?"** (`noul` → `predicate`) | ✅ Best so far | Flagged all 11 real emergencies with no false alarms, including the suicidal hint (0.84), the 9-year-old left alone (0.91) and "no place to sleep tonight" (0.79 IT, 0.72 EN). |
| **Graded urgency** (`score` 0/1/2) | ⚠️ Partly usable | Cleanly separates "no human needed" (mean 0.02–0.06) from the rest. Urgent cases always score ≥ 1.84, but non-urgent escalations spread from 1.04 to 1.98, so the two overlap (exact 31/40 IT, 31/40 EN, 21/28 hard). |
| **Robustness to option order** | ✅ Mostly | Correct in 232/240 runs with the options reversed. The top answer flips in 13 of 240 requests, mostly in the coding-tools domain. |
| **Latency** | – Not reported | It depends on the network and the API load; to be re-evaluated in the future (see [Timings](#timings)). |
| **Italian vs English** | ✅ No accuracy gap | 90/90 IT and 88/90 EN on the base suite. |

**Suggested way to use it.** Route with a `choice` and accept p ≥ ~0.8. That threshold rejects 35 of 234 correct answers but none of the wrong ones; below it, ask the user to clarify. For escalation, use two separate predicates, "needs a human?" and "risk to safety or health?". The urgency `score` is reliable for "nobody needed" vs "somebody needed", not for "useful" vs "urgent". Do not use several independent predicates as a router (see [Pilot](#pilot-12-cases-5-agents)): they say yes to too many agents.

**Hosted model.** It runs on OpenAI's hardware, not on the laptop, and its size and architecture are not disclosed. Timings are not reported, see [Timings](#timings).

## Raw reports

| File | Content |
|---|---|
| [`suite_data_it-en.json`](suite_data_it-en.json), [`.log`](suite_data_it-en.log) | Base suite, IT + EN |
| [`suite_data_hard_it.json`](suite_data_hard_it.json), [`.log`](suite_data_hard_it.log) | Hard suite, IT |
| [`pilot_12_cases_it-en.json`](pilot_12_cases_it-en.json), [`.log`](pilot_12_cases_it-en.log) | Pilot, 12 cases |
| [`pilot_latency_it.log`](pilot_latency_it.log) | Single-question latency, long vs key-only labels (raw, see [Timings](#timings)) |

## Routing

Each request is asked twice, once with the options in their normal order and once reversed. "Flips" counts requests where the top answer changed.

| Suite | Domain (agents) | IT correct | EN correct | Correct when reversed (IT / EN) | Flips (IT / EN) |
|---|---|---|---|---|---|
| base | Service desk (8) | 32/32 | 32/32 | 32 / 32 | 2 / 1 |
| base | E-commerce support (8) | 20/20 | 20/20 | 20 / 20 | 0 / 1 |
| base | Company internal helpdesk (9) | 22/22 | 22/22 | 22 / 22 | 0 / 1 |
| base | Coding agent tool choice (8) | 16/16 | 14/16 | 16 / 14 | 0 / 2 |
| **hard** (IT only) | all four domains | **56/60** | – | 54 | 6 |

- **Base suite errors, both in English and in the coding domain:**
  - "How many users signed up last week?" went to `ask_user` (0.49) instead of `query_database`;
  - "Fix it." went to `search_code` (0.79) instead of `ask_user`. This is the most confident error of the run.
- **Hard suite errors:**
  - "abbiamo finito il caffè" went to procurement instead of facilities (0.66);
  - "torna alla versione di ieri" went to `chiedi_utente` (0.49);
  - "Scrivi il changelog per la release 2.3" went to `chiedi_utente` (0.51);
  - the slow-query case went to `cerca_codice` (0.53) instead of `interroga_database`.
- **Correct only in one order:** "ma perché la CI è rossa?" (0.56) and "aggiorna la doc dell'API dopo le modifiche di ieri" (0.81) went to `chiedi_utente` when reversed. "What's the latest version of React…" did the same in English.
- **It leans towards asking the user.** Most errors and flips in the coding domain go to `ask_user` / `chiedi_utente`. That is a cautious failure mode, but it also means the coding-tools domain is the weakest, as with the other models.

## Escalation to a human: library FAQ bot

| Suite | Lang | Cases | Needs human? (`noul`) | `choice` version | Safety/health risk (`noul`) | Urgency `score` exact |
|---|---|---|---|---|---|---|
| base | IT | 40 (20 yes / 20 no) | 40/40 | 40/40 | 40/40 | 31/40 |
| base | EN | 40 (20 / 20) | 40/40 | 39/40 (false alarm: "How do I get a library card?", 0.63) | 40/40 | 31/40 |
| hard | IT | 28 + 2 borderline | 28/28 | 28/28 | 29/29 | 21/28 |

- **Wide margins.** Yes cases score ≥ 0.92 (IT), ≥ 0.93 (EN) and ≥ 0.95 (hard). No cases score ≤ 0.06 (IT) and ≤ 0.17 (hard); the English library-card question is the outlier at 0.31.
- **Safety risk:** the lowest real emergency is "no place to sleep tonight" (0.79 IT, 0.72 EN). The highest non-emergency is the stolen wallet (0.13).
- **Urgency `score`:** mean 0.02 / 1.54 / 1.95 (IT) and 0.06 / 1.52 / 1.98 (EN) for no-human / useful / urgent; 0.05 / 1.54 / 2.00 on the hard set. All exact-match misses but one are non-urgent escalations rounded up to 2, such as "Come rinnovo un prestito?" (1.95). Ranking urgent above useful gives AUROC 0.92 (IT), 0.95 (EN) and 1.00 (hard).
- **Borderline cases:**
  - the prompt injection asking for users' data was escalated (1.00);
  - "mi gira un po' la testa… c'è un posto dove sedersi al fresco?" was not escalated (0.34), with risk 0.15.
- **No refusals.** The API can answer a question with a `refusal`. It did not refuse any of the 1,148 questions in this run, including the safety ones.

## Pilot: 12 cases, 5 agents

| Lang | `choice`, long descriptions | Reversed | Key-only labels | Top `noul` among agents | Agent-count `score` |
|---|---|---|---|---|---|
| IT | 12/12 | 12/12 | 12/12 | 10/12 | 5/12 |
| EN | 12/12 | 12/12 | 12/12 | 11/12 | 5/12 |

- **Routing with `choice` is perfect**, even with key-only labels and no descriptions.
- **Independent predicates are too generous.** Asked "should the request go to agent X?" for each of the 5 agents, it often says yes to several of them. "A che ora siete aperti domani?" got 0.98 for the translator and 0.95 for the front office. Use a `choice` to route.
- **The agent-count `score` underestimates.** Most requests score below 0.5 ("the front office is enough"), even those that need two specialists.

## Configuration

| Item | Value |
|---|---|
| Model | `gpt-6-luna`, the only model available on the Decisions API. Hosted by OpenAI; size and architecture not disclosed. |
| API | `POST https://api.openai.com/v1/decisions`, public beta. Run on 2026-10-08. |
| How it decides | Typed questions return probabilities, not generated text: `predicate` returns `probability`; `choice` and `score` return a distribution over the options, plus `confidence`. |
| Proxy | [`openai_decisions_proxy.py`](../../openai_decisions_proxy.py) serves `/v1/systemone` on `127.0.0.1:8092` and forwards each request to OpenAI. `noul` → `predicate`, `choice` criteria → `choices` (`value` + `description`), `score` criteria → `levels` (`label`), `state` → `input` text (`Key: value` blocks). Refusals would count as probability 0 and are logged as `REFUSAL`; 429/5xx are retried with backoff. Neither happened in this run. |
| Request model name | `gpt-6-luna` (the proxy uses its own `--model` anyway) |
| Pricing | $0.10 per 1M input tokens, no output-token charges. The whole run costs a few cents. |
| Machine | Client on the MacBook Pro (Apple M3 Pro, 36 GB), over the internet. The model runs at OpenAI. |
| Client | Python 3 standard library, one request at a time (concurrency 1) |

## How to reproduce

Start the proxy with your API key, in a terminal you leave open:

```bash
export OPENAI_API_KEY=sk-...
python3 openai_decisions_proxy.py 2>&1 | tee proxy.log
```

Then, from another terminal at the root of this repo:

```bash
./run_all.sh http://127.0.0.1:8092/v1/systemone gpt-6-luna gpt-6-luna
grep -c REFUSAL proxy.log
```

`token_count.py` does not apply, because the API has no `/tokenize` endpoint.

## Timings

Timings are not reported for this model. They include the internet round trip to OpenAI and depend on the network and on the API load at the time of the run, so they cannot be compared with the local models and are to be re-evaluated in the future. The raw logs still contain the per-request milliseconds.
