# System One Italian tests

These tests check whether a local "System One" decision model can handle two jobs in Italian, with English for comparison:

- routing a user request to the right agent, team or tool;
- deciding when a FAQ chatbot should hand the conversation to a human.

A System One model answers typed questions about a piece of text (`choice`, `noul` for yes/no, `score` for an ordinal scale) and returns probabilities instead of generated text.

## Results by model

Each tested model has its own folder under `results/`, with a README (verdicts, detailed results, configuration, timings, how to reproduce) and the raw reports.

| Model | Setup | Routing (clean / messy IT) | Needs human? | Safety risk | Urgency `score` | Report |
|---|---|---|---|---|---|---|
| [Winnow-12B](https://huggingface.co/EldanRing/Winnow-12B) Q8_0 | Local, MacBook Pro M3 Pro | 180/180 · 59/60 | 108/108 | 10 of 11 emergencies | ❌ not usable | [results/winnow-12b-q8_0](results/winnow-12b-q8_0/README.md) |

## Test suites

| File | Content |
|---|---|
| `suite_data.py` | **Base suite**, IT + EN. 90 routing requests across 4 domains, each agent with a one-sentence description. 40 library escalation conversations (20 yes, 20 no; 4 are real emergencies). |
| `suite_data_hard.py` | **Hard suite**, IT only, reusing the same agents and questions. 60 routing requests: typos, dialect and slang, all caps, rambling, IT/EN mixing, sarcasm, negations ("non mi serve una traduzione…"), one-word or vague requests. 30 escalation conversations, 2 of them borderline. |
| `suite_run.py` | Runner for both suites. Prints one line per case, then a summary, and writes JSON and log to `results/<tag>/`. |
| `pilot_12_cases.py`, `pilot_latency.py` | The pilot run (12 cases, 5 agents) and the single-question latency measurement. |
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
python3 suite_run.py --data suite_data --langs it,en --url http://127.0.0.1:8091/v1/systemone --model Winnow-12B --tag winnow-12b-q8_0
python3 suite_run.py --data suite_data_hard --langs it --url http://127.0.0.1:8091/v1/systemone --model Winnow-12B --tag winnow-12b-q8_0
```

`--model` is the name sent in the body and `--tag` the results folder (e.g. `results/kev-9b/`). When adding a model, also add a `README.md` in its folder and a row to [Results by model](#results-by-model).

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
results/
  winnow-12b-q8_0/     Winnow-12B Q8_0: README.md + raw reports (one folder per model)
```
