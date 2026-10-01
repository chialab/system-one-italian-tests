# Laya 0.3.22

Results of the System One Italian tests for **[Laya](https://github.com/NandhaKishorM/laya)** (Convai Innovations), package `laya==0.3.22`, run locally on a MacBook Pro with the built-in router choosing the checkpoint. The suites and the request format are described in the [main README](../../README.md).

## Summary

The test cases were written by hand. They do not measure accuracy on real traffic (see [Caveats](../../README.md#caveats)). Laya was used out of the box, without fine-tuning; its authors present the shipped checkpoints as "a fast base to specialise".

| Use | Verdict | Evidence |
|---|---|---|
| **Routing in Italian** (8–9 options) | ❌ Not usable as is | 47/90 (52%) on clean requests, 22/60 (37%) on messy ones. |
| **Routing in English** | ⚠️ Weak | 69/90 (77%) on clean requests. |
| **Confidence as a fallback signal** | ❌ IT / ⚠️ EN | In Italian the errors are confident (mean p 0.68, many ≥ 0.9), so a threshold cannot catch them. In English the errors sit lower (mean p 0.40). |
| **Keyword traps** | ❌ Falls for them | "traduzione del contratto di *lavoro*" goes to the job coach; "sono un *traduttore* e cerco finanziamenti" goes to the translator. |
| **"Does this chat need a human?"** (`noul`) | ❌ Not usable | AUROC 0.43 / 0.48 / 0.23 (base IT / base EN / hard IT): no better than chance. In Italian the no cases score higher (0.90) than the yes cases (0.79). |
| **Same question as a `choice`** (bot / human) | ⚠️ Some signal, wrong threshold | AUROC 0.70–0.81 with no false alarms, but at p ≥ 0.5 it misses 10–16 of the 20 escalations in the base suite. |
| **"Is anyone's safety or health at risk?"** (`noul`) | ❌ Never fires | 0 of 11 real emergencies flagged. The highest risk probability on any case is 0.18. |
| **Graded urgency** (`score` 0/1/2) | ❌ Not usable | Escalation and non-escalation cases get almost the same mean score (1.26 vs 1.17 base IT; 1.15 vs 1.26 hard IT). |
| **Robustness to option order** | ❌ Low in Italian | The top answer flips in 28/90 (base IT), 27/60 (hard IT) and 12/90 (base EN) requests when the options are reversed. |
| **Latency** | ✅ Very fast | About 57 ms per request in Italian and 105 ms in English on this laptop, after warm-up. |

**Bottom line.** Out of the box, Laya does not handle these Italian routing and escalation tasks. It is 20–60 times faster than Winnow-12B on the same machine. That speed only pays off if it is fine-tuned on the target labels, which these tests do not cover.

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
| base | Service desk (8) | 16/32 | 27/32 | 20 / 27 | 8 / 4 |
| base | E-commerce support (8) | 7/20 | 17/20 | 7 / 18 | 7 / 3 |
| base | Company internal helpdesk (9) | 15/22 | 16/22 | 11 / 18 | 9 / 4 |
| base | Coding agent tool choice (8) | 9/16 | 9/16 | 11 / 10 | 4 / 1 |
| **hard** (IT only) | all four domains | **22/60** | – | 23 | 27 |

- **Confident Italian errors.** "Il televisore è arrivato con lo schermo rotto" and "voglio cancellare il mio account" both go to `security_fraud` (p ≈ 0.95–0.98). `security_fraud` takes 8 of the Italian base-suite errors. "Quanti utenti si sono registrati la settimana scorsa?" goes to `ask_user` (0.99).
- **English errors are mostly low-confidence:** "Fix it" goes to `search_code` (0.33), "I need the logo guidelines" to HR (0.22).

## Escalation to a human: library FAQ bot

| Suite | Lang | Cases | Needs human? (`noul`) | `choice` version | Safety/health risk (`noul`) | Urgency `score` exact |
|---|---|---|---|---|---|---|
| base | IT | 40 (20 yes / 20 no) | 19/40, AUROC 0.43 | 30/40 (10 missed), AUROC 0.70 | 36/40 (all 4 emergencies missed) | 15/40 |
| base | EN | 40 (20 / 20) | 23/40, AUROC 0.48 | 24/40 (16 missed), AUROC 0.75 | 36/40 (all 4 missed) | 16/40 |
| hard | IT | 28 + 2 borderline | 12/28, AUROC 0.23 | 23/28 (5 missed), AUROC 0.81 | 26/29 (all 3 missed) | 11/28 |

The "correct" counts for the risk question come only from the non-emergency cases: the model answers "no risk" to everything.

## Pilot: 12 cases, 5 agents

| Lang | `choice`, long descriptions | Reversed | Key-only labels | Top `noul` among agents | Agent-count `score` |
|---|---|---|---|---|---|
| IT | 10/12 | 10/12 | 9/12 | 8/12 | 6/12 |
| EN | 8/12 | 8/12 | 8/12 | 7/12 | 3/12 |

With only 5 agents Laya does better than on the main suite: 10/12 in Italian, against 7/12 for the CLM-8B head and 12/12 for Winnow-12B.

## Configuration

| Item | Value |
|---|---|
| Package | `laya==0.3.22` from PyPI, server `laya-serve` (`laya[serve]`), Apache 2.0 |
| Checkpoints | Bundle `convaiinnovations/laya` at revision `55cf4c4` (the package's reviewed SHA). Loaded: `english` (ModernBERT-large, 421M, 512-token window) and `multilingual` (mmBERT-base, 322M, 1,024-token window, 100+ languages). |
| Checkpoint choice | Request field `model: "convaiinnovations/laya"`, which lets Laya's router pick per request: Italian goes to `multilingual`, English to `english`. |
| How it decides | Encoder-only *cross-encoder*: state, question and options are encoded together in one bidirectional pass, and a scoring head returns a probability per option. No text generation. |
| Option budget | The question and options share a head budget of 192 tokens (`english`) or 256 tokens (`multilingual`). Each option description is cut to its first 48 tokens, and with 8–9 options to about 20–30 tokens. The one-sentence agent descriptions of the suite are therefore truncated. |
| Known warning | At startup Laya warns that one shipped temperature is out of range: "Treat confidence from the affected entries as uncalibrated." |
| Launch | `LAYA_DEVICE=mps LAYA_PORT=8000 LAYA_HOST=127.0.0.1 LAYA_MODELS=english,multilingual laya-serve` |
| Machine | MacBook Pro, Apple M3 Pro (6 performance + 6 efficiency cores), 36 GB unified memory, macOS 26.6.2. Python 3.12, torch 2.14.1 on MPS. No other model server running during the tests. |
| Client | Python 3 standard library, one request at a time (concurrency 1) |

## How to reproduce

```bash
python3.12 -m venv ~/laya-venv
~/laya-venv/bin/pip install "laya[serve]==0.3.22"
LAYA_DEVICE=mps LAYA_PORT=8000 LAYA_HOST=127.0.0.1 LAYA_MODELS=english,multilingual ~/laya-venv/bin/laya-serve
```

The first start downloads the checkpoints from Hugging Face. Then, from the root of this repo:

```bash
./run_all.sh http://127.0.0.1:8000/v1/systemone convaiinnovations/laya laya-0.3.22
```

## Timings

All timings were measured on the laptop above, at concurrency 1, end to end through HTTP, with no other model server running.

| Request | Median |
|---|---|
| One routing `choice`, 5 agents with long (~60-word) descriptions | 50 ms (first two calls: 709 and 183 ms, warm-up) |
| One routing `choice`, 5 agents with key-only labels | 36 ms (first two calls: 183 and 110 ms) |
| Suite routing request: 2 `choice` questions (normal + reversed) | 57 ms IT / 105 ms EN |
| Escalation request: 4 questions on a short conversation | 58 ms IT / 118 ms EN |
| Pilot request: 9 questions | 259 ms IT / 433 ms EN |

- **English is slower than Italian, the opposite of Winnow.** The router sends English to the `english` checkpoint (ModernBERT-large, 421M parameters) and Italian to the smaller `multilingual` one (mmBERT-base, 322M). Token count plays almost no role, because the options are truncated to a fixed budget anyway.
- **Why it is fast.** It is a 0.3–0.4B encoder that reads everything in one forward pass, against a 12B decoder for Winnow. Each new request pays only a short warm-up the first time a checkpoint runs on MPS.
