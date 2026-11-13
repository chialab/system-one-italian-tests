# System One Italian tests

These tests check whether a "System One" decision model, local or hosted, can handle two jobs in Italian, with English for comparison:

- routing a user request to the right agent, team or tool;
- deciding when a FAQ chatbot should hand the conversation to a human.

A System One model answers typed questions about a piece of text (`choice`, `noul` for yes/no, `score` for an ordinal scale) and returns probabilities instead of generated text.

## Results by model


**TL;DR**

- **Jev 1.14** (TypeSafe, hosted), the reference model for this API format, matches Winnow on routing (239/240) and is the most stable when the options are reversed (3 flips out of 240). It flagged all 11 emergencies. It is a paid cloud API: your text leaves the machine.
  - Its "needs a human?" margins are narrower: some real escalations score only 0.76–0.85, and it raised one false alarm in English. A 0.5 threshold works here, but calibrate it on real conversations.
- **Winnow-12B** is as accurate as Jev and the most confident. It is also the slowest: 2–4 s on this laptop.
- **Kev-4B** is almost as accurate and about 4 times faster, but its probabilities are flatter and it missed more safety signals.
  - *Flatter* means Kev spreads its probability across the options even when it picks the right one. The chosen agent gets 0.82 on average, against 0.98 for Winnow. Kev is often right but rarely sure, so a 0.8 threshold would reject 89 of its 231 correct answers; use about 0.5 instead.
  - It flagged 8 of 11 emergencies against Winnow's 10. It missed a suicidal hint and a 9-year-old left alone at closing time, both of which Winnow caught.
- **Strands Decider 2B** (AWS Strands Labs, open weights) is the smallest model that routes well: 233/240, about as accurate as Kev and 1.4 times faster on this laptop, with the fewest flips among local models when the options are reversed (8 of 240). It is the weakest of the usable models on escalation.
  - Its "needs a human?" `noul` missed 12 of 108 escalations at p ≥ 0.5, including a lost 6-year-old and a suicidal hint. The bot/human `choice` misses none but raises 7 false alarms.
  - It flagged only 4 of 11 emergencies. Use it for routing, not as a safety net.
- **GPT-6 Luna** (OpenAI Decisions API, hosted) is almost as accurate and, like Jev, flagged all 11 emergencies. Jev and Luna are the only models whose urgency `score` separates "nobody needed" from "somebody needed" everywhere; neither tells "useful" from "urgent". It is a paid cloud API: your text leaves the machine. Its timings depend on the network and are to be re-evaluated in the future.
  - Its probabilities sit between Winnow's and Kev's (0.92 on average for the chosen agent). A 0.8 threshold keeps 199 of 240 decisions with no errors.
  - Its errors lean towards `ask_user` on vague coding requests, a cautious way to be wrong.
- **Gemini Decision 1** (Gemini Decisions API, hosted) is as accurate as Luna on routing (235/240) and the most clear-cut of the hosted models on confidence: all its errors had p ≤ 0.55, so a 0.8 threshold keeps 205 of 240 decisions with no errors. Like Jev and Luna it flagged all 11 emergencies, and its urgency `score` separates "nobody needed" from "somebody needed" but not "useful" from "urgent". It is a paid cloud API, with a free tier whose inputs Google may use; your text leaves the machine. Its timings depend on the network and are to be re-evaluated in the future.
  - The API sorts `choice` options alphabetically before scoring, so its position bias cannot be measured with the reversed-order run.
  - Unlike Luna, it did not escalate the prompt injection asking for users' data (0.17).
  - Two days after launch the API was flaky: sporadic `403` errors that succeeded on retry, and one request that hung.
- **Laya** is very fast but not usable for Italian out of the box. Its authors say so themselves: they present the shipped checkpoints "as a fast base to specialise, not as a zero-shot decision engine". They recommend [fine-tuning on your own labels](https://github.com/NandhaKishorM/laya#fine-tune-for-better-accuracy). On their own typed-decisions benchmark fine-tuning raises accuracy from 0.36 to 0.77. These tests use Laya without fine-tuning.

Each tested model has its own folder under `results/`, with a README (verdicts, detailed results, configuration, timings, how to reproduce) and the raw reports.

All local models were run on the same MacBook Pro (M3 Pro, 36 GB), one at a time, with no other model server running. The hosted models (Jev at TypeSafe, GPT-6 Luna at OpenAI, Gemini Decision 1 at Google) were called from the same laptop over the internet, so their latency depends on the network: it is not reported and is to be re-evaluated in the future.

| Model | Architecture | Routing: clean IT · clean EN · messy IT | Needs human? | Safety risk | Urgency `score` | Routing latency (IT / EN) | Report |
|---|---|---|---|---|---|---|---|
| [Jev 1.14](https://docs.typesafe.ai/models.md) `jev-1.14.0` | Hosted (TypeSafe API), not disclosed | 90/90 · 90/90 · 59/60 | 107/108 (1 false alarm) | 11 of 11 | ⚠️ none vs some, not useful vs urgent | – (depends on the network, to be re-evaluated) | [results/jev-1.14.0](results/jev-1.14.0/README.md) |
| [Winnow-12B](https://huggingface.co/EldanRing/Winnow-12B) Q8_0 | 12B decoder LLM, option-letter logits | 90/90 · 90/90 · 59/60 | 108/108 | 10 of 11 emergencies | ❌ not usable | 3.5 s / 2.7 s | [results/winnow-12b-q8_0](results/winnow-12b-q8_0/README.md) |
| [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b) | 4B decoder LLM (Qwen3.5) + LoRA + pointer head, MLX | 88/90 · 88/90 · 55/60 | 105/108 (missed a suicidal hint) | 8 of 11 | ⚠️ clean cases only | 0.93 s / 0.74 s | [results/kev-4b](results/kev-4b/README.md) |
| [Strands Decider 2B](https://huggingface.co/StrandsAgents/strands-decider-2B-qwen3.5-v1-2610) | 2B decoder LLM (Qwen3.5) + LoRA + pointer head, MPS | 89/90 · 90/90 · 54/60 | 96/108 (12 missed, incl. a suicidal hint) | 4 of 11 | ❌ not usable | 0.66 s / 0.54 s | [results/strands-decider-2b](results/strands-decider-2b/README.md) |
| [GPT-6 Luna](https://developers.openai.com/api/docs/guides/decisions) `gpt-6-luna` | Hosted (OpenAI Decisions API, beta), not disclosed | 90/90 · 88/90 · 56/60 | 108/108 | 11 of 11 | ⚠️ none vs some, not useful vs urgent | – (depends on the network, to be re-evaluated) | [results/gpt-6-luna](results/gpt-6-luna/README.md) |
| [Gemini Decision 1](https://aistudio.google.com/docs/decisions-api) `gemini-decision-1` | Hosted (Gemini Decisions API, v1beta), not disclosed | 89/90 · 88/90 · 58/60 | 108/108 | 11 of 11 | ⚠️ none vs some, not useful vs urgent | – (depends on the network, to be re-evaluated) | [results/gemini-decision-1](results/gemini-decision-1/README.md) |
| [Laya](https://github.com/NandhaKishorM/laya) 0.3.22 | 0.3–0.4B encoder (cross-encoder) | 47/90 · 69/90 · 22/60 | 54/108 (≈ chance) | 0 of 11 | ❌ not usable | 57 ms / 105 ms | [results/laya-0.3.22](results/laya-0.3.22/README.md) |

Routing latency is the median of one suite request with two `choice` questions over 8–9 options.

**Confidence thresholds.** Over all 240 routing decisions (base + hard), this is what each model gives you if you only accept answers above a probability threshold and send the rest to a fallback:

| Model | Accept p ≥ 0.5 | Accept p ≥ 0.8 |
|---|---|---|
| Jev 1.14 | 239 accepted, 1 wrong | 216 accepted, 0 wrong |
| Winnow-12B | 238 accepted, 1 wrong | 233 accepted, 0 wrong |
| Kev-4B | 212 accepted, 2 wrong | 142 accepted, 0 wrong |
| Strands Decider 2B | 231 accepted, 2 wrong | 185 accepted, 0 wrong |
| GPT-6 Luna | 232 accepted, 4 wrong | 199 accepted, 0 wrong |
| Gemini Decision 1 | 229 accepted, 3 wrong | 205 accepted, 0 wrong |
| Laya 0.3.22 | 167 accepted, 55 wrong | 112 accepted, 33 wrong |

## Test suites

| File | Content |
|---|---|
| `suite_data.py` | **Base suite**, IT + EN. 90 routing requests across 4 domains, each agent with a one-sentence description. 40 library escalation conversations (20 yes, 20 no; 4 are real emergencies). |
| `suite_data_hard.py` | **Hard suite**, IT only, reusing the same agents and questions. 60 routing requests: typos, dialect and slang, all caps, rambling, IT/EN mixing, sarcasm, negations ("non mi serve una traduzione…"), one-word or vague requests. 30 escalation conversations, 2 of them borderline. |
| `suite_run.py` | Runner for both suites. Prints one line per case, then a summary, and writes JSON and log to `results/<tag>/`. |
| `pilot_12_cases.py`, `pilot_latency.py` | The pilot run (12 cases, 5 agents) and the single-question latency measurement. |
| `run_all.sh` | Runs everything above for one model and writes the reports into `results/<tag>/`. |
| `token_count.py` | IT vs EN token counts of the base suite, via the server's `/tokenize`. |
| `decisions_proxy.py` | Local proxy that serves `/v1/systemone` on top of the [OpenAI Decisions API](https://developers.openai.com/api/docs/guides/decisions) (`--provider openai`, `gpt-6-luna`) or the [Gemini Decisions API](https://aistudio.google.com/docs/decisions-api) (`--provider gemini`, `gemini-decision-1`), so the same runners work with hosted decision APIs. |

Routing requests are asked twice, once with the options in their normal order and once reversed, to measure position bias. Escalation cases are short conversations between a user and a library bot that only answers with preset FAQ replies.

Each request sends questions in the TypeSafe System One format to `POST /v1/systemone`:

```json
{
  "model": "Winnow-12B",
  "state": {"Richiesta": "Mi è scaduto il permesso di soggiorno, come lo rinnovo?"},
  "questions": {
    "route": {
      "type": "choice",
      "instructions": "Sei il supervisore di uno sportello di servizi e coordini otto agenti. A quale agente affidi questa richiesta?",
      "criteria": {"consulente_immigrazione": "Consulenza legale su permessi di soggiorno, …", "traduttore": "…"}
    }
  } 
}
```

Escalation requests put `Contesto` and `Conversazione` (`Utente: …` / `Bot: …`) in `state` and ask four questions in one call: `noul` needs-human, `choice` bot/human, `score` urgency, and `noul` safety risk. A response counts as positive when p ≥ 0.5.

## How to run

The client uses only the Python 3 standard library and sends one request at a time. Start a TypeSafe-compatible `/v1/systemone` server (the model's README explains how to set up its own), then run from this repo:

```bash
./run_all.sh <url> <model> <tag>
./run_all.sh http://127.0.0.1:8091/v1/systemone Winnow-12B winnow-12b-q8_0
```

`<model>` is the name sent in the request body and `<tag>` the results folder (e.g. `results/kev-4b/`). The script runs the base suite (IT + EN), the hard suite (IT), the pilot and the latency measurement. To run a single suite instead:

```bash
python3 suite_run.py --data suite_data_hard --langs it --url <url> --model <model> --tag <tag>
```

For a hosted server that needs a key, such as Jev at `https://api.typesafe.ai/v1/systemone`, put the key in a `.env` file at the root of this repo (it is gitignored). `run_all.sh` loads it and the runners send it as a bearer token:

```
TYPESAFE_API_KEY=...
```

```bash
./run_all.sh https://api.typesafe.ai/v1/systemone jev-1.14.0 jev-1.14.0
```

To test the OpenAI Decisions API, start the local proxy with your key in a terminal you leave open:

```bash
export OPENAI_API_KEY=sk-...
python3 decisions_proxy.py --provider openai 2>&1 | tee proxy.log
```

Then, from another terminal, point `run_all.sh` at it:

```bash
./run_all.sh http://127.0.0.1:8092/v1/systemone gpt-6-luna gpt-6-luna
```

The Gemini Decisions API works the same way, with a key from Google AI Studio:

```bash
export GEMINI_API_KEY=...
python3 decisions_proxy.py --provider gemini 2>&1 | tee proxy.log
```

```bash
./run_all.sh http://127.0.0.1:8092/v1/systemone gemini-decision-1 gemini-decision-1
```

The proxy logs any refusal as `REFUSAL`; the runners count it as probability 0. OpenAI refuses single questions; Gemini blocks a whole request with a safety error, so every question in that request counts as refused.

Gemini sorts `choice` options alphabetically before scoring, so the reversed-order run cannot show position bias there: expect 0 flips by construction.

When adding a model, also add a `README.md` in its folder and a row to [Results by model](#results-by-model). For comparable timings, run one model server at a time.

## Caveats

- **The cases are synthetic.** All requests and conversations were written by the author, and labels are clear-cut by design. Perfect scores mean a model handles these patterns, not that it will be perfect on real users. The next step is a few dozen anonymised real requests.
- **Small samples.** n = 60–90 per suite and language, from a single deterministic run with no confidence intervals.
- **Ambiguous cases accept several agents.** Where a case accepts more than one agent, any of them counts as correct.
- **What these tests do not cover:** long documents (Winnow-class models are mostly trained on short inputs), 20+ options, and multi-turn agent loops.
- **Timings depend on the machine.** Each model README states the hardware its timings were measured on. For hosted models they also depend on the network and the API load.
- **Hosted models can change.** `gpt-6-luna` was tested on 2026-10-08, while the Decisions API was in public beta; OpenAI can update the model behind the same name. `jev-1.14.0` was tested on 2026-10-26, pinned by version rather than through the `jev-latest` alias. `gemini-decision-1` was tested on 2026-11-13, two days after the Gemini Decisions API launched on `v1beta`.

## Layout

```
suite_data.py          base suite (IT + EN)
suite_data_hard.py     hard suite (IT)
suite_run.py           runner
pilot_12_cases.py      pilot run
pilot_latency.py       single-question latency
token_count.py         IT vs EN token counts
run_all.sh             all suites for one model
decisions_proxy.py     /v1/systemone on top of the OpenAI or Gemini Decisions API
results/               one folder per model: README.md + raw reports
  winnow-12b-q8_0/     Winnow-12B Q8_0
  kev-4b/              Kev-4B (MLX, bfloat16)
  strands-decider-2b/  Strands Decider 2B (MPS, bfloat16)
  laya-0.3.22/         Laya 0.3.22 (router: english + multilingual)
  gpt-6-luna/          GPT-6 Luna (OpenAI Decisions API, via proxy)
  jev-1.14.0/          Jev 1.14 (TypeSafe API)
  gemini-decision-1/   Gemini Decision 1 (Gemini Decisions API, via proxy)
```
