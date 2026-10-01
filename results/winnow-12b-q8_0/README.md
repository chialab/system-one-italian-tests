# Winnow-12B Q8_0

Results of the System One Italian tests for **[Winnow-12B](https://huggingface.co/EldanRing/Winnow-12B)**, Q8_0, run locally on a MacBook Pro. The suites and the request format are described in the [main README](../../README.md).

## Summary

The test cases were written by hand. They do not measure accuracy on real traffic (see [Caveats](../../README.md#caveats)).

| Use | Verdict | Evidence |
|---|---|---|
| **Routing to agents, teams or tools** (8–9 options) | ✅ Reliable, IT and EN alike | 180/180 on clean requests. 59/60 on messy Italian (typos, slang, rambling, vague, mixed language). |
| **Confidence as a fallback signal** | ✅ Usable | Mean probability 0.96–0.99 when right. The only miss had p = 0.55. |
| **"Does this chat need a human?"** (`noul`) | ✅ Very reliable | 108/108 correct. Yes cases ≥ 0.97, no cases ≤ 0.02 (one outlier at 0.43). |
| **"Is anyone's safety or health at risk?"** (`noul`) | ✅ Good, one miss | Flagged 10 of 11 real emergencies (gas, fainting, lost child, suicidal hint…) with no false alarms. Missed "no place to sleep tonight" in Italian (0.30; 0.82 in English). |
| **Graded urgency** (`score` 0/1/2) | ❌ Not usable | Any case that needs a human gets about 2 ("urgent"), so non-urgent and urgent cannot be told apart. |
| **Robustness to option order** | ⚠️ Mostly | Correct in 236/240 runs with the options reversed. On ambiguous or vague requests the top answer can flip (13 of 240). |
| **Latency on a laptop** | ⚠️ 1–4 s per request | Fine for one routing decision per conversation, too slow for per-step agent loops on this machine (see [Timings](#timings)). |
| **Italian vs English** | ✅ No accuracy gap | Same accuracy. Italian routing is about 30% slower because it uses about 36% more tokens for the same text (see [Italian vs English](#italian-vs-english)). |

**Suggested way to use it.** Route with a `choice` that gives a one-sentence description for each agent. Accept answers with p ≥ ~0.8; below that, ask the user to clarify or fall back to an LLM or a human. Handle escalation with two separate `noul` questions, "needs a human?" and "risk to safety or health?", and do not use a `score` for urgency.

## Raw reports

| File | Content |
|---|---|
| [`suite_data_it-en.json`](suite_data_it-en.json), [`.log`](suite_data_it-en.log) | Base suite, IT + EN |
| [`suite_data_hard_it.json`](suite_data_hard_it.json), [`.log`](suite_data_hard_it.log) | Hard suite, IT |
| [`pilot_12_cases_it-en.json`](pilot_12_cases_it-en.json), [`.log`](pilot_12_cases_it-en.log) | Pilot, 12 cases |
| [`pilot_latency_it.log`](pilot_latency_it.log) | Single-question latency, long vs key-only labels |

The JSON files hold every prediction and probability; the logs are the console output.

## Routing

Each request is asked twice, once with the options in their normal order and once reversed, to measure position bias. "Flips" counts requests where the top answer changed between the two runs. Some cases accept more than one agent; those are the ambiguous ones.

| Suite | Domain (agents) | IT correct | EN correct | Correct when reversed | Flips |
|---|---|---|---|---|---|
| base | Service desk (8) | 32/32 | 32/32 | 64/64 | 5 |
| base | E-commerce support (8) | 20/20 | 20/20 | 40/40 | 0 |
| base | Company internal helpdesk (9) | 22/22 | 22/22 | 44/44 | 2 |
| base | Coding agent tool choice (8) | 16/16 | 16/16 | 32/32 | 0 |
| **hard** (IT only) | all four domains | **59/60** | – | 56/60 | 6 |

- **The one miss (hard):** "La query di ricerca prodotti è lentissima, guarda il piano di esecuzione" went to `ask_user` (p 0.55) instead of `query_database`. With the options reversed it went to `search_code`.
- **Low-confidence or flipping cases are genuinely ambiguous:**
  - a police letter that someone cannot read: translator or immigration advisor;
  - salary file sent by mistake: cybersecurity or HR;
  - "abbiamo finito il caffè": facilities or procurement;
  - "perché la CI è rossa?": run tests or search code.
- **Keyword traps did not fool it.** "Corso sulla *sicurezza* sul lavoro" went to training, "*Excel* non si apre" went to IT helpdesk, and "sono un *traduttore* e cerco finanziamenti" went to the grants expert.

## Escalation to a human: library FAQ bot

Each case is a short conversation between a user and a bot that only answers with preset FAQ replies.

| Suite | Lang | Cases | Needs human? (`noul`) | `choice` version | Safety/health risk (`noul`) | Urgency `score` exact |
|---|---|---|---|---|---|---|
| base | IT | 40 (20 yes / 20 no) | 40/40 | 40/40 | 39/40 (missed: no place to sleep) | 24/40 |
| base | EN | 40 (20 / 20) | 40/40 | 40/40 | 40/40 | 25/40 |
| hard | IT | 28 + 2 borderline | 28/28 | 27/28 (false alarm: lost umbrella) | 29/29 | 18/28 |

- **What the hard set contains:** sarcasm ("grazie mille eh, utilissimo 👏"), a serious problem mentioned in passing ("comunque mi hanno rubato il portafoglio"), a bot that misunderstands while the user stays polite, frustration that ends up resolved, "sei un umano o un bot?" asked as a joke, typos, all caps, and a suicidal hint.
- **Borderline cases are reported but not scored:**
  - a prompt injection asking for users' phone numbers: escalated (0.95);
  - "mi gira la testa… va meglio": not escalated, risk 0.08.

## Pilot: 12 cases, 5 agents

This was the first run, before the main suite existed. It is kept for reference and produced with `pilot_12_cases.py`.

| Lang | `choice`, long descriptions | Reversed | Key-only labels | Top `noul` among agents | Agent-count `score` |
|---|---|---|---|---|---|
| IT | 12/12 | 12/12 | 11/12 | 12/12 | 10/12 |
| EN | 12/12 | 12/12 | 12/12 | 12/12 | 7/12 |

On the same 12 cases, the released [CLM-8B](https://github.com/Contrastive-LM/CLM) head (Contrastive-LM) never went above 7/12 in our earlier tests. That comparison was the reason for trying Winnow.

## Configuration

| Item | Value |
|---|---|
| Model | `EldanRing/Winnow-12B`, a Gemma 4 12B IT fine-tune, Apache 2.0. File `Winnow-12B-Q8_0.gguf` (11.8 GiB), checksum verified by the setup script. |
| How it decides | A single decoder LLM, with no separate encoder. It reads state, question and letter-labelled options as one prompt and returns the softmax over the option letters' next-token logits, generating no text. |
| Language | The LoRA fine-tune teaches typed decisions; it is not Italian-specific (training data is private). Italian comes from the multilingual Gemma 4 base model, and the tokenizer is Gemma's unchanged one. |
| Server | [`EldanRing/winnow-inference`](https://github.com/EldanRing/winnow-inference) at commit `77d1458`. llama.cpp pinned at `911f6cd` with the repo's 4 patches, Metal build. |
| Launch | `python3 scripts/serve.py --profile apple-silicon --text-only --context 8192` |
| Effective settings | 8K context, f16 KV cache, 1 decision branch, exclusive memory, letter-logit "selected" head, temperature 1, no vision projector. Endpoint on `127.0.0.1:8091`. |
| Machine | MacBook Pro, Apple M3 Pro (6 performance + 6 efficiency cores), 36 GB unified memory, macOS 26.6.2. No other model server running during the tests. |
| Client | Python 3 standard library, one request at a time (concurrency 1) |

## How to reproduce

```bash
git clone https://github.com/EldanRing/winnow-inference.git && cd winnow-inference
python3 scripts/setup.py --profile apple-silicon --text-only
python3 scripts/serve.py --profile apple-silicon --text-only --context 8192
```

The setup script needs `cmake` and `openssl@3`, downloads about 12 GB and builds llama.cpp. Once the server is up, run from the root of this repo:

```bash
./run_all.sh http://127.0.0.1:8091/v1/systemone Winnow-12B winnow-12b-q8_0
```

`run_all.sh` runs the base suite, the hard suite, the pilot and the latency measurement, and writes every report into the model's folder.

## Timings

All timings were measured on the laptop above, at concurrency 1, end to end through HTTP, with no other model server running. A first run with another idle model server loaded gave the same medians within 2%. **They reflect this machine, not the model's ceiling.** The Winnow model card reports runs on an RTX 5070 Ti, and the hosted Jev API reports 70–500 ms per request.

| Request | Median |
|---|---|
| One routing `choice`, 5 agents with long (~60-word) descriptions | 2.7 s |
| One routing `choice`, 5 agents with key-only labels | 0.9 s |
| Suite routing request: 2 `choice` questions (normal + reversed), 8–9 one-sentence descriptions | 3.5 s IT / 2.7 s EN |
| Escalation request: 4 questions on a short conversation | 2.1–2.2 s |
| Pilot request: 9 questions | 7.4 s IT / 6.5 s EN |

Why it costs this much here:

- **Latency is dominated by prefill.** Winnow reads every option's text and then the label logits, so time grows with the number of option tokens and with the number of questions per request. The key-only versus long-description gap shows this directly.
- **The M3 Pro GPU is the bottleneck.** A 12B model at Q8 on a laptop GPU prefills far more slowly than on a desktop or datacenter GPU.
- **Requests run one at a time.** The decision service processes requests sequentially, so throughput scales with the hardware, not with concurrency.
- **Italian costs more tokens than English**, which is why the English runs were faster (see below).

### Italian vs English

The tokenizer splits Italian into more tokens than English for the same amount of text. The Italian option descriptions are only 3% longer in characters but 36% longer in tokens, and time follows the token count.

| Per request (base suite, averages) | IT | EN | IT vs EN |
|---|---|---|---|
| Routing: request text | 17 tok | 15 tok | +13% |
| Routing: question | 27 tok | 23 tok | +17% |
| Routing: option descriptions, per `choice` | 251 tok (1,000 chars) | 184 tok (971 chars) | +36% tokens, +3% chars |
| **Routing: median time** (2 `choice`) | **3.5 s** | **2.7 s** | **+31%** |
| Escalation: conversation | 37 tok | 34 tok | +9% |
| **Escalation: median time** (4 questions) | **2.2 s** | **2.1 s** | **+6%** |

Option descriptions are most of a routing request, so the language gap shows there. In escalation the conversation is a small part of the input and the questions are short, so the gap almost disappears. Token counts come from the server's `/tokenize` endpoint (`python3 token_count.py`).
