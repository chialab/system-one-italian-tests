# Kev-4B

Results of the System One Italian tests for **[Kev-4B](https://huggingface.co/jaredpalmer/kev-4b)** (Jared Palmer), run locally on a MacBook Pro through Kev's own server on MLX. The suites and the request format are described in the [main README](../../README.md).

## Summary

The test cases were written by hand. They do not measure accuracy on real traffic (see [Caveats](../../README.md#caveats)).

| Use | Verdict | Evidence |
|---|---|---|
| **Routing to agents, teams or tools** (8–9 options) | ✅ Good, IT and EN alike | 176/180 on clean requests (88 IT, 88 EN). 55/60 on messy Italian. |
| **Confidence as a fallback signal** | ✅ Usable, with a lower threshold | All 9 errors had p < 0.8, but so did 89 of 231 correct answers. At p ≥ 0.5 it accepts 212 of 240 decisions with 2 errors. |
| **"Does this chat need a human?"** (`noul`) | ⚠️ Good, misses some | 105/108 (AUROC 1.00 on every suite, so the ranking is perfect but the 0.5 threshold is not). Missed a GDPR complaint threat (0.37), someone else's data in the user's profile (0.47) and a **suicidal hint (0.31)**. |
| **"Is anyone's safety or health at risk?"** (`noul`) | ⚠️ Partial | Flagged 8 of 11 real emergencies, with 1 false alarm. Missed the suicidal hint (0.09), a 9-year-old left alone at closing time (0.41) and "no place to sleep tonight" in Italian (0.38). |
| **Graded urgency** (`score` 0/1/2) | ⚠️ Works on clean cases | Base suite: mean score 0.2 for no-human, 1.3 for useful, 1.7 for urgent (exact 35/40 IT, 34/40 EN). On the hard set the real emergencies average 1.0, below the non-urgent escalations (1.3). |
| **Robustness to option order** | ✅ Mostly | Correct in 231/240 runs with the options reversed. The top answer flips in 18 of 240 requests, mostly vague ones. |
| **Latency on a laptop** | ✅ About 0.5–1 s per request | Almost 4 times faster than Winnow-12B on the same machine (see [Timings](#timings)). |
| **Italian vs English** | ✅ No accuracy gap | Same accuracy. Italian is about 25% slower because it uses more tokens. |

**Suggested way to use it.** Route with a `choice` and accept p ≥ ~0.5; Kev's probabilities are flatter than Winnow's, so a 0.8 threshold would reject many correct answers. Escalation works with a `noul`, but do not rely on it alone for safety: it missed a suicidal hint that Winnow-12B caught. Unlike the other models tested, its urgency `score` is meaningful on clear-cut cases.

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
| base | Service desk (8) | 32/32 | 32/32 | 32 / 32 | 2 / 1 |
| base | E-commerce support (8) | 20/20 | 19/20 | 20 / 20 | 0 / 1 |
| base | Company internal helpdesk (9) | 22/22 | 22/22 | 22 / 22 | 1 / 2 |
| base | Coding agent tool choice (8) | 14/16 | 15/16 | 14 / 15 | 2 / 0 |
| **hard** (IT only) | all four domains | **55/60** | – | 54 | 9 |

- **Base suite errors, all low-confidence:**
  - "Perché fallisce il test del login?" went to `ask_user` (0.34);
  - "Fai quella modifica di cui parlavamo" went to `git` (0.33);
  - a phishing email went to `account_privacy` instead of `security_fraud` (0.49);
  - "Find all the places where we still use the old date library" went to `web_search` (0.51).
- **Hard suite errors:**
  - "nn mi è arrivato un caxxo" went to returns instead of shipping (0.63);
  - "credo sia un problema di pagamento: vedo 3 ordini che non ho fatto e la password non funziona più" went to `account_privacy` instead of `security_fraud` (0.32);
  - "abbiamo finito il caffè" went to finance (0.25);
  - "perché la CI è rossa?" went to `search_code` (0.29);
  - the slow-query case went to `search_code` (0.45).
- **The coding-tools domain is the weakest**, as with Winnow, because the tools overlap.

## Escalation to a human: library FAQ bot

| Suite | Lang | Cases | Needs human? (`noul`) | `choice` version | Safety/health risk (`noul`) | Urgency `score` exact |
|---|---|---|---|---|---|---|
| base | IT | 40 (20 yes / 20 no) | 39/40 (missed: GDPR threat) | 40/40 | 38/40 (missed: no place to sleep; false alarm: school visit) | 35/40 |
| base | EN | 40 (20 / 20) | 40/40 | 40/40 | 40/40 | 34/40 |
| hard | IT | 28 + 2 borderline | 26/28 (missed: suicidal hint, someone else's data) | 27/28 (missed: suicidal hint) | 27/29 (missed: suicidal hint, child alone) | 21/28 |

- **The margins are narrower than Winnow's.** In the base suite yes cases go as low as 0.37 (IT) and 0.65 (EN), and no cases reach 0.23 and 0.36.
- **Borderline cases:**
  - the prompt injection asking for users' phone numbers was escalated (0.79);
  - "mi gira la testa… va meglio" was not escalated (0.09).

## Pilot: 12 cases, 5 agents

| Lang | `choice`, long descriptions | Reversed | Key-only labels | Top `noul` among agents | Agent-count `score` |
|---|---|---|---|---|---|
| IT | 12/12 | 12/12 | 12/12 | 11/12 | 8/12 |
| EN | 12/12 | 12/12 | 12/12 | 11/12 | 9/12 |

## Configuration

| Item | Value |
|---|---|
| Model | `jaredpalmer/kev-4b` (snapshot `139fdd9`), Apache 2.0: a rank-16 LoRA adapter plus a small pointer head on `Qwen/Qwen3.5-4B-Base`, merged into the base at load time. |
| How it decides | A decoder LLM reads the state once, then each question in its own branch. A pointer head scores each option's hidden state against the question's decision token and returns a softmax over the options. No text generation. |
| Language | The model card describes the training data as English (≤384-token states for the 0.8B/4B/9B sizes). Italian comes from the multilingual Qwen3.5 base model. |
| Server | [`jaredpalmer/kev`](https://github.com/jaredpalmer/kev) at commit `90512f1`, `python -m kev.serve`, MLX backend in bfloat16, picked automatically on Apple Silicon. Python 3.13 environment created by `uv`. |
| Launch | `uv run --extra serve python -m kev.serve --run jaredpalmer/kev-4b --port 8009` |
| Request model name | `kev-latest` |
| Machine | MacBook Pro, Apple M3 Pro (6 performance + 6 efficiency cores), 36 GB unified memory, macOS 26.6.2. No other model server running during the tests. |
| Client | Python 3 standard library, one request at a time (concurrency 1), after one warm-up request |

## How to reproduce

```bash
brew install uv
git clone https://github.com/jaredpalmer/kev.git && cd kev
uv sync --extra serve
uv run --extra serve python -m kev.serve --run jaredpalmer/kev-4b --port 8009
```

The first start downloads the Qwen3.5-4B base and the adapter from Hugging Face, and the first request loads the model, so send one warm-up request before timing anything. Then, from the root of this repo:

```bash
./run_all.sh http://127.0.0.1:8009/v1/systemone kev-latest kev-4b
```

## Timings

All timings were measured on the laptop above, at concurrency 1, end to end through HTTP, with no other model server running.

| Request | Median |
|---|---|
| One routing `choice`, 5 agents with long (~60-word) descriptions | 0.75 s |
| One routing `choice`, 5 agents with key-only labels | 0.21 s |
| Suite routing request: 2 `choice` questions (normal + reversed), 8–9 one-sentence descriptions | 0.93 s IT / 0.74 s EN |
| Escalation request: 4 questions on a short conversation | 0.57 s IT / 0.48 s EN |
| Pilot request: 9 questions | 5.5 s IT / 4.9 s EN |

- **Almost 4 times faster than Winnow-12B** on the same requests (0.93 s against 3.5 s for routing in Italian). That fits a model a third the size, running on MLX.
- **Italian is about 25% slower than English**, for the same reason as Winnow: Italian text costs more tokens.
- **The pilot is slow per request** because it asks 9 questions, 3 of them `choice` questions with long descriptions.
