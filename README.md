# System One Italian tests

These tests check whether a local "System One" decision model can handle two jobs in Italian, with English for comparison:

- routing a user request to the right agent, team or tool;
- deciding when a FAQ chatbot should hand the conversation to a human.

A System One model answers typed questions about a piece of text (`choice`, `noul` for yes/no, `score` for an ordinal scale) and returns probabilities instead of generated text.

## Results by model

Each tested model has its own folder under `results/`, with a README (verdicts, detailed results, configuration, timings, how to reproduce) and the raw reports.

All models were run on the same MacBook Pro (M3 Pro, 36 GB), one at a time, with no other model server running.

| Model | Architecture | Routing: clean IT · clean EN · messy IT | Needs human? | Safety risk | Urgency `score` | Routing latency (IT / EN) | Report |
|---|---|---|---|---|---|---|---|
| [Winnow-12B](https://huggingface.co/EldanRing/Winnow-12B) Q8_0 | 12B decoder LLM, option-letter logits | 90/90 · 90/90 · 59/60 | 108/108 | 10 of 11 emergencies | ❌ not usable | 3.5 s / 2.7 s | [results/winnow-12b-q8_0](results/winnow-12b-q8_0/README.md) |
| [Kev-4B](https://huggingface.co/jaredpalmer/kev-4b) | 4B decoder LLM (Qwen3.5) + LoRA + pointer head, MLX | 88/90 · 88/90 · 55/60 | 105/108 (missed a suicidal hint) | 8 of 11 | ⚠️ clean cases only | 0.93 s / 0.74 s | [results/kev-4b](results/kev-4b/README.md) |
| [Laya](https://github.com/NandhaKishorM/laya) 0.3.22 | 0.3–0.4B encoder (cross-encoder) | 47/90 · 69/90 · 22/60 | 54/108 (≈ chance) | 0 of 11 | ❌ not usable | 57 ms / 105 ms | [results/laya-0.3.22](results/laya-0.3.22/README.md) |

Routing latency is the median of one suite request with two `choice` questions over 8–9 options.

**Confidence thresholds.** Over all 240 routing decisions (base + hard), this is what each model gives you if you only accept answers above a probability threshold and send the rest to a fallback:

| Model | Accept p ≥ 0.5 | Accept p ≥ 0.8 |
|---|---|---|
| Winnow-12B | 238 accepted, 1 wrong | 233 accepted, 0 wrong |
| Kev-4B | 212 accepted, 2 wrong | 142 accepted, 0 wrong |
| Laya 0.3.22 | 167 accepted, 55 wrong | 112 accepted, 33 wrong |

**In short:**

- **Winnow-12B** is the most accurate and the most confident. It is also the slowest: 2–4 s on this laptop.
- **Kev-4B** is almost as accurate and about 4 times faster, but its probabilities are flatter and it missed more safety signals.
- **Laya** is very fast but not usable for Italian out of the box.

## Test suites

| File | Content |
|---|---|
| `suite_data.py` | **Base suite**, IT + EN. 90 routing requests across 4 domains, each agent with a one-sentence description. 40 library escalation conversations (20 yes, 20 no; 4 are real emergencies). |
| `suite_data_hard.py` | **Hard suite**, IT only, reusing the same agents and questions. 60 routing requests: typos, dialect and slang, all caps, rambling, IT/EN mixing, sarcasm, negations ("non mi serve una traduzione…"), one-word or vague requests. 30 escalation conversations, 2 of them borderline. |
| `suite_run.py` | Runner for both suites. Prints one line per case, then a summary, and writes JSON and log to `results/<tag>/`. |
| `pilot_12_cases.py`, `pilot_latency.py` | The pilot run (12 cases, 5 agents) and the single-question latency measurement. |
| `run_all.sh` | Runs everything above for one model and writes the reports into `results/<tag>/`. |
| `token_count.py` | IT vs EN token counts of the base suite, via the server's `/tokenize`. |

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

When adding a model, also add a `README.md` in its folder and a row to [Results by model](#results-by-model). For comparable timings, run one model server at a time.

## Caveats

- **The cases are synthetic.** All requests and conversations were written by the author, and labels are clear-cut by design. Perfect scores mean a model handles these patterns, not that it will be perfect on real users. The next step is a few dozen anonymised real requests.
- **Small samples.** n = 60–90 per suite and language, from a single deterministic run with no confidence intervals.
- **Ambiguous cases accept several agents.** Where a case accepts more than one agent, any of them counts as correct.
- **What these tests do not cover:** long documents (Winnow-class models are mostly trained on short inputs), 20+ options, and multi-turn agent loops.
- **Timings depend on the machine.** Each model README states the hardware its timings were measured on.

## Layout

```
suite_data.py          base suite (IT + EN)
suite_data_hard.py     hard suite (IT)
suite_run.py           runner
pilot_12_cases.py      pilot run
pilot_latency.py       single-question latency
token_count.py         IT vs EN token counts
run_all.sh             all suites for one model
results/               one folder per model: README.md + raw reports
  winnow-12b-q8_0/     Winnow-12B Q8_0
  kev-4b/              Kev-4B (MLX, bfloat16)
  laya-0.3.22/         Laya 0.3.22 (router: english + multilingual)
```
