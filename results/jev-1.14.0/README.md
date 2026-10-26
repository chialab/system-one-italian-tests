# Jev 1.14 (TypeSafe)

Results of the System One Italian tests for **[Jev](https://docs.typesafe.ai/models.md) `jev-1.14.0`** by TypeSafe AI, the reference System One model whose wire format these tests use. It is a hosted model: requests were sent from the same MacBook Pro over the internet straight to `https://api.typesafe.ai/v1/systemone`, with no adapter. The suites and the request format are described in the [main README](../../README.md).

## Summary

The test cases were written by hand. They do not measure accuracy on real traffic (see [Caveats](../../README.md#caveats)).

| Use | Verdict | Evidence |
|---|---|---|
| **Routing to agents, teams or tools** (8–9 options) | ✅ Reliable, IT and EN alike | 180/180 on clean requests. 59/60 on messy Italian. |
| **Confidence as a fallback signal** | ✅ Usable | The only error had p = 0.52. At p ≥ 0.8 it accepts 216 of 240 decisions with no errors; at p ≥ 0.5, 239 with 1 error. |
| **"Does this chat need a human?"** (`noul`) | ✅ Reliable, narrower margins | 107/108. One English false alarm ("How do I get a library card?", 0.77). Some real escalations score only 0.76–0.85, so the gap to the no cases is smaller than with Winnow or GPT-6 Luna. |
| **"Is anyone's safety or health at risk?"** (`noul`) | ✅ Very good | Flagged all 11 real emergencies with no false alarms, including the suicidal hint (0.91) and the 9-year-old left alone (0.93). Lowest: "no place to sleep tonight" (0.70 IT, 0.75 EN). |
| **Graded urgency** (`score` 0/1/2) | ⚠️ Partly usable | Cleanly separates "no human needed" (mean 0.01–0.06) from the rest. Urgent cases always score ≥ 1.93, but non-urgent escalations spread from 1.07 to 1.97 (exact 30/40 IT, 29/40 EN, 20/28 hard). |
| **Robustness to option order** | ✅ The most stable so far | Correct in 238/240 runs with the options reversed. The top answer flips in only 3 of 240 requests. |
| **Latency** | – Not reported | It depends on the network and the API load; to be re-evaluated in the future (see [Timings](#timings)). |
| **Italian vs English** | ✅ No accuracy gap | 90/90 in both languages on the base suite. |

**Suggested way to use it.** Route with a `choice` and accept p ≥ ~0.8; below that, ask the user to clarify. For escalation, use two separate `noul` questions, "needs a human?" and "risk to safety or health?". A 0.5 threshold works on these cases, but the margins are narrower than Winnow's, so calibrate it on real conversations. The urgency `score` is reliable for "nobody needed" vs "somebody needed", not for "useful" vs "urgent".

**Hosted model.** It runs on TypeSafe's hardware, not on the laptop, and its size and architecture are not disclosed. TypeSafe says English is still its strongest language and expects the largest gain of 1.14 to be in multilingual support.

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
| base | Service desk (8) | 32/32 | 32/32 | 32 / 32 | 0 / 0 |
| base | E-commerce support (8) | 20/20 | 20/20 | 20 / 20 | 1 / 1 |
| base | Company internal helpdesk (9) | 22/22 | 22/22 | 22 / 22 | 0 / 0 |
| base | Coding agent tool choice (8) | 16/16 | 16/16 | 16 / 15 | 0 / 1 |
| **hard** (IT only) | all four domains | **59/60** | – | 59 | 0 |

- **The only error:** "ma perché la CI è rossa?" went to `chiedi_utente` (0.52) instead of `esegui_test`, in both orders. Kev-4B and GPT-6 Luna also stumbled on it.
- **Correct only in one order:** "Add documentation comments to the module's public functions." went to `write_docs` with p = 0.50, and to `search_code` (0.52) when reversed.
- **No flips on the hard suite.** Typos, dialect, all caps and vague requests did not change its answer when the options were reversed.

## Escalation to a human: library FAQ bot

| Suite | Lang | Cases | Needs human? (`noul`) | `choice` version | Safety/health risk (`noul`) | Urgency `score` exact |
|---|---|---|---|---|---|---|
| base | IT | 40 (20 yes / 20 no) | 40/40 | 40/40 | 40/40 | 30/40 |
| base | EN | 40 (20 / 20) | 39/40 (false alarm: "How do I get a library card?", 0.77) | 39/40 (same case, 0.77) | 40/40 | 29/40 |
| hard | IT | 28 + 2 borderline | 28/28 | 28/28 | 29/29 | 20/28 |

- **Narrower margins than Winnow and GPT-6 Luna.** No cases stay ≤ 0.13 (IT) and ≤ 0.10 (hard), apart from the English library-card outlier. But several real escalations sit at 0.76–0.85: the double charge for a course (0.76 IT, 0.84 EN), "voglio parlare con una persona" and "questo bot non mi serve a niente" (0.83, 0.77), the blocked card (0.79 IT, 0.84 EN), "no place to sleep tonight" (0.82).
- **Safety risk:** all 11 emergencies at 0.70 or above. The highest non-emergency is the wallet stolen in the reading room (0.40).
- **Urgency `score`:** mean 0.01 / 1.56 / 1.98 (IT) and 0.06 / 1.59 / 2.00 (EN) for no-human / useful / urgent; 0.03 / 1.68 / 2.00 on the hard set. All exact-match misses but one are non-urgent escalations rounded up to 2; the other is the English library-card question (1.01). Ranking urgent above useful gives AUROC 0.98 (IT), 1.00 (EN) and 1.00 (hard).
- **Borderline cases:**
  - the prompt injection asking for users' data was escalated (0.92);
  - "mi gira un po' la testa… c'è un posto dove sedersi al fresco?" was not escalated (0.08), with risk 0.22.

## Pilot: 12 cases, 5 agents

| Lang | `choice`, long descriptions | Reversed | Key-only labels | Top `noul` among agents | Agent-count `score` |
|---|---|---|---|---|---|
| IT | 12/12 | 12/12 | 12/12 | 12/12 | 9/12 |
| EN | 12/12 | 12/12 | 12/12 | 12/12 | 9/12 |

- **Perfect routing**, with long descriptions, reversed and with key-only labels (`criteria` values set to `null`).
- **Independent predicates work as a ranking.** The right agent always has the highest `noul`. Some requests also get a second yes, usually the front office, so pick the top one rather than every agent above 0.5.
- **The agent-count `score` is the most consistent across languages** (9/12 in both, against 10/12 IT and 7/12 EN for Winnow, 8 and 9 for Kev, 5 and 5 for GPT-6 Luna). The misses are the three requests that need two specialists, which score 1.0–1.2 instead of 2.

## Configuration

| Item | Value |
|---|---|
| Model | `jev-1.14.0` (Jev 1.14, released 14 October 2026), pinned by version rather than through the `jev-latest` alias. Hosted by TypeSafe; size and architecture not disclosed. |
| API | `POST https://api.typesafe.ai/v1/systemone`, `Authorization: Bearer` token. Run on 2026-10-26. No experimental (`TypeSafe-Danger-Zone-*`) headers, so default context. |
| How it decides | Typed questions return probabilities, not generated text: `noul` returns a yes probability, `choice` and `score` return a distribution over the options plus `confidence`. |
| Language | No language setting. The docs say English is the primary training language; other languages are handled "but not equally well". |
| Request model name | `jev-1.14.0` |
| Pricing | $0.042 per 1M input tokens, output free. The whole run costs about a cent. |
| Machine | Client on the MacBook Pro (Apple M3 Pro, 36 GB), over the internet. The model runs at TypeSafe. |
| Client | Python 3 standard library, one request at a time (concurrency 1). The API key is read from `TYPESAFE_API_KEY`. |

## How to reproduce

Put your key in a `.env` file at the root of this repo (it is gitignored); `run_all.sh` loads it:

```
TYPESAFE_API_KEY=...
```

Then, from the root of this repo:

```bash
./run_all.sh https://api.typesafe.ai/v1/systemone jev-1.14.0 jev-1.14.0
```

`token_count.py` does not apply, because the API has no `/tokenize` endpoint.

## Timings

Timings are not reported for this model. They include the internet round trip to TypeSafe and depend on the network and on the API load at the time of the run, so they cannot be compared with the local models and are to be re-evaluated in the future. The raw logs still contain the per-request milliseconds.
