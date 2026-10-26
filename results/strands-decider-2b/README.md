# Strands Decider 2B

Results of the System One Italian tests for **[Strands Decider 2B](https://huggingface.co/StrandsAgents/strands-decider-2B-qwen3.5-v1-2610)** (AWS Strands Labs), checkpoint `strands-decider-2B-qwen3.5-v1-2610`, run locally on a MacBook Pro through its own server on MPS. The suites and the request format are described in the [main README](../../README.md).

## Summary

The test cases were written by hand. They do not measure accuracy on real traffic (see [Caveats](../../README.md#caveats)).

| Use | Verdict | Evidence |
|---|---|---|
| **Routing to agents, teams or tools** (8–9 options) | ✅ Good, IT and EN alike | 179/180 on clean requests (89 IT, 90 EN). 54/60 on messy Italian. |
| **Confidence as a fallback signal** | ✅ Usable | All 7 errors had p < 0.8. At p ≥ 0.8 it accepts 185 of 240 decisions with no errors; at p ≥ 0.5, 231 with 2 errors. |
| **"Does this chat need a human?"** (`noul`) | ❌ Not at 0.5 | 96/108. All 12 errors are missed escalations, including the lost 6-year-old (0.49) and the suicidal hint (0.35). The ranking is almost right (AUROC 0.97–1.00), but real escalations go as low as 0.29 and routine questions as high as 0.48, so no single threshold works across suites. |
| **Same question as a `choice` (bot / human)** | ⚠️ Errs towards a human | 101/108 with no missed escalations. All 7 errors are false alarms on routine questions such as the wifi password. |
| **"Is anyone's safety or health at risk?"** (`noul`) | ❌ Not reliable | Flagged 4 of 11 real emergencies, with no false alarms. Missed the lost child, "no place to sleep tonight", the suicidal hint and the 9-year-old left alone (all ≤ 0.19). |
| **Graded urgency** (`score` 0/1/2) | ❌ Not usable | Every score falls between 0.54 and 1.30. The order is right on average (about 0.65 / 1.0 / 1.1 for no-human / useful / urgent), but the scale is too squeezed to read. |
| **Robustness to option order** | ✅ The most stable local model | Correct in 231/240 runs with the options reversed. The top answer flips in only 8 of 240 requests. |
| **Latency on a laptop** | ✅ About 0.5–0.7 s per request | Faster than Kev-4B on routing on the same machine (see [Timings](#timings)). |
| **Italian vs English** | ✅ No clear gap | Same routing accuracy; escalation errors are split between the two languages. Italian is about 20% slower. |

**Suggested way to use it.** Route with a `choice` and accept p ≥ ~0.8; below that, ask the user to clarify or fall back to an LLM or a human. Do not use it alone for escalation or safety. If you need it for escalation, ask the bot/human `choice` rather than the `noul`: it errs towards a human instead of missing real cases.

## Raw reports

| File | Content |
|---|---|
| [`suite_data_it-en.json`](suite_data_it-en.json), [`.log`](suite_data_it-en.log) | Base suite, IT + EN |
| [`suite_data_hard_it.json`](suite_data_hard_it.json), [`.log`](suite_data_hard_it.log) | Hard suite, IT |
| [`pilot_12_cases_it-en.json`](pilot_12_cases_it-en.json), [`.log`](pilot_12_cases_it-en.log) | Pilot, 12 cases |
| [`pilot_latency_it.log`](pilot_latency_it.log) | Single-question latency, long vs key-only labels |

## Routing

Each request is asked twice, once with the options in their normal order and once reversed. "Flips" counts requests where the top answer changed.

| Suite | Domain (agents) | IT correct | EN correct | Correct when reversed (IT / EN) | Flips (IT / EN) |
|---|---|---|---|---|---|
| base | Service desk (8) | 32/32 | 32/32 | 32 / 32 | 1 / 1 |
| base | E-commerce support (8) | 20/20 | 20/20 | 20 / 20 | 0 / 0 |
| base | Company internal helpdesk (9) | 21/22 | 22/22 | 20 / 20 | 1 / 2 |
| base | Coding agent tool choice (8) | 16/16 | 16/16 | 16 / 16 | 0 / 0 |
| **hard** (IT only) | all four domains | **54/60** | – | 55 | 3 |

- **Base suite error:** "Possiamo usare gli indirizzi email degli iscritti alla newsletter per una campagna con un partner?" went to `comunicazione` instead of `ufficio_legale` (0.36).
- **Correct only in one order (base):** the large-room booking went to training (`formazione` / `training`) when reversed, in both languages, and the salary file sent by mistake went to `finance_admin`.
- **Hard suite errors:**
  - two security cases went elsewhere: "vedo 3 ordini che non ho fatto e la mia password non funziona più" to `account_privacy` (0.40), and the SMS code given to a fake support call to `ordini_spedizioni` (0.37);
  - "abbiamo finito il caffè" went to `amministrazione` (0.33);
  - "ma perché la CI è rossa?" went to `chiedi_utente` (0.79), the most confident error of the run;
  - "dov'è che mandiamo le email di benvenuto?" went to `chiedi_utente` (0.63);
  - the slow-query case went to `chiedi_utente` (0.43), but to `interroga_database` when reversed.
- **The coding-tools domain is again the weakest on messy requests**, and as with GPT-6 Luna the errors lean towards asking the user.

## Escalation to a human: library FAQ bot

| Suite | Lang | Cases | Needs human? (`noul`) | `choice` version | Safety/health risk (`noul`) | Urgency `score` exact |
|---|---|---|---|---|---|---|
| base | IT | 40 (20 yes / 20 no) | 37/40 (missed: GDPR threat, lost child, double charge) | 37/40 (3 false alarms) | 38/40 (missed: lost child, no place to sleep) | 16/40 |
| base | EN | 40 (20 / 20) | 36/40 (missed: GDPR threat, lost child, double charge, blocked card) | 40/40 | 37/40 (missed: man following a woman, lost child, no place to sleep) | 16/40 |
| hard | IT | 28 + 2 borderline | 23/28 (missed 5, including the suicidal hint) | 24/28 (4 false alarms) | 27/29 (missed: suicidal hint, child alone) | 10/28 |

- **The `noul` probabilities overlap.** Real escalations go as low as 0.35 (IT), 0.30 (EN) and 0.29 (hard), while routine questions go as high as 0.48 (IT, the wifi password). The ranking is almost right (AUROC 0.995 IT, 1.00 EN, 0.97 hard), so a lower threshold calibrated on your own data could work, but it would differ between languages.
- **The `choice` version leans the other way.** It never missed an escalation, but it sent 7 routine questions to a human (p between 0.51 and 0.79).
- **Safety risk:** only the fainting (0.72 IT, 0.73 EN), the gas smell (0.72) and the man following a woman in Italian (0.60) cross 0.5. The other real emergencies score 0.13–0.37.
- **Urgency `score`:** mean 0.69 / 0.98 / 1.10 (IT), 0.61 / 1.04 / 1.12 (EN) and 0.70 / 0.93 / 0.98 (hard) for no-human / useful / urgent. The order is right on average but the ranges overlap.
- **Borderline cases:**
  - the prompt injection asking for users' data was escalated (0.62);
  - "mi gira un po' la testa… c'è un posto dove sedersi al fresco?" was not escalated (0.18), with risk 0.11.

## Pilot: 12 cases, 5 agents

| Lang | `choice`, long descriptions | Reversed | Key-only labels | Top `noul` among agents | Agent-count `score` |
|---|---|---|---|---|---|
| IT | 12/12 | 12/12 | 12/12 | 12/12 | 6/12 |
| EN | 12/12 | 12/12 | 12/12 | 11/12 | 6/12 |

- **Routing with `choice` is perfect**, even with key-only labels and no descriptions.
- **The agent-count `score` always lands near 1** (0.78–1.07). It gets the 6 single-specialist cases right and all the others wrong.

## Configuration

| Item | Value |
|---|---|
| Model | `StrandsAgents/strands-decider-2B-qwen3.5-v1-2610` (snapshot `216d1cc`), Apache 2.0: a rank-48 LoRA adapter plus a pointer head on `Qwen/Qwen3.5-2B-Base`, averaged over three training runs ("soup") and calibrated with one temperature per question type. |
| How it decides | A decoder LLM reads the state, then a pointer head scores each option and returns a softmax over the options. No text generation. |
| Language | The model card does not mention languages. The training data are mostly English public classification datasets; Italian comes from the multilingual Qwen3.5 base model. |
| Server | [`strands-labs/strands-decider`](https://github.com/strands-labs/strands-decider) 0.2.0 from PyPI, `strands-decider serve`, torch 2.14.1 on MPS in bfloat16, transformers 5.20.2. Python 3.13 environment created by `uv`. It accepts the suite requests unchanged, no proxy needed. |
| Launch | `strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8010 --device mps` |
| Request model name | `strands-decider-2B-qwen3.5-v1-2610` (the server ignores it) |
| Machine | MacBook Pro, Apple M3 Pro, 36 GB unified memory, macOS 26.6.2. No other model server running during the tests. |
| Client | Python 3 standard library, one request at a time (concurrency 1), after one warm-up request |

## How to reproduce

```bash
uv venv -p 3.13 ~/strands-decider
source ~/strands-decider/bin/activate && uv pip install strands-decider
strands-decider serve StrandsAgents/strands-decider-2B-qwen3.5-v1-2610 --port 8010 --device mps
```

The first start downloads the Qwen3.5-2B base and the adapter from Hugging Face, and the first request loads the model (about 3.5 s), so send one warm-up request before timing anything. Then, from the root of this repo:

```bash
./run_all.sh http://127.0.0.1:8010/v1/systemone strands-decider-2B-qwen3.5-v1-2610 strands-decider-2b
```

## Timings

All timings were measured on the laptop above, at concurrency 1, end to end through HTTP, with no other model server running.

| Request | Median |
|---|---|
| One routing `choice`, 5 agents with long (~60-word) descriptions | 0.48 s |
| One routing `choice`, 5 agents with key-only labels | 0.19 s |
| Suite routing request: 2 `choice` questions (normal + reversed), 8–9 one-sentence descriptions | 0.66 s IT / 0.54 s EN |
| Escalation request: 4 questions on a short conversation | 0.46 s IT / 0.45 s EN |
| Pilot request: 9 questions | 4.0 s IT / 3.5 s EN |

- **About 1.4 times faster than Kev-4B on routing** (0.66 s against 0.93 s in Italian). On escalation the two are close (0.46 s against 0.57 s).
- **Italian is about 20% slower than English on routing**, because Italian text costs more tokens.
- **The pilot is slow per request** because it asks 9 questions, 3 of them `choice` questions with long descriptions.
- **MLX was not tried.** The project says `--device mlx` is 1.4–1.6 times faster than MPS, but it needs an install from the git repository.
