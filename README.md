# issue-agent

A small coding agent that reads a bug report, explores a Python repo, edits the code, runs the tests, and produces a fix, plus an evaluation harness that measures **how often its fixes are actually correct**, not just whether the visible tests pass.

Built from scratch with the Gemini API (free tier) and plain Python. No agent frameworks.

## How it works

    issue text + repo -> agent loop (LLM + tool calls) -> edited repo -> tests
                              |
       tools: list_files, read_file, search, edit_file, run_tests

- `agent/tools.py`: repo tools. Paths are sandboxed to the repo, and `edit_file` only accepts an unambiguous single match.
- `agent/loop.py`: the tool-calling loop, with retries for rate limits and a full step-by-step trace of every run.
- `agent/prompts.py`: versioned system prompts (v1, v2, v3) so prompt changes can be compared fairly.
- `evals/`: the benchmark tasks, runner, and analysis scripts.

## How the evaluation works

Each task is a small buggy repo with an issue description. Scoring is stricter than "the tests pass":

- **Hidden tests.** The agent only sees a few tests. After it finishes, extra tests it never saw are added and everything is re-run.
- **OVERFIT label.** The agent passes the visible tests but fails the hidden ones, meaning it fixed the symptom and not the root cause.
- **Tamper check.** Editing the visible test files counts as a failure.
- **Vague issues.** Some issues describe symptoms only ("customers are charged the wrong amount") without naming the file or function.
- **Repeated runs.** LLM output varies between runs, so experiments are repeated and the spread is reported.

## Results

Model: `gemini-flash-lite-latest` (free tier). All tasks are small hand-written bugs, so read these as a pilot study.

| Task set | Prompt | Runs | Hidden-test solve rate |
|---|---|---|---|
| 12 easy single-file bugs (visible tests only) | v1 | 1 | 12/12 (benchmark saturated, so I made harder tasks) |
| 5 harder tasks with hidden tests | v1 | 2 | 60%, then 20% (high variance) |
| 5 harder tasks | v2 | 1 | 100% (contaminated, see below) |
| 5 harder tasks | v3 | 1 | 100% |
| 5 held-out tasks (18-22) | v1 | 3 | 80%, 80%, 80% |
| 5 held-out tasks (18-22) | v3 | 3 | 100%, 100%, 100% |

On the held-out tasks, both prompts solved tasks 18 to 21 in every run. The whole difference comes from `22_overdraft`: v1 solved it 0 of 3 times and v3 solved it 3 of 3 times.

## What I learned

1. **A saturated benchmark tells you nothing.** The first 12 tasks were solved 12/12, so I added hidden tests and vaguer issues to get a baseline with room to improve.
2. **Passing visible tests is not the same as being correct.** On the hard tasks, prompt v1 often passed the visible tests and failed the hidden ones (OVERFIT).
3. **I found leakage in my own experiment.** Prompt v2 listed example edge cases that overlapped with the hidden tests, so its 100% is contaminated. Prompt v3 removed the task-specific hints and I evaluated it on new held-out tasks that no prompt had been tuned on.
4. **Concrete failure example.** On `22_overdraft`, v1 added a balance check to `withdraw` and stopped once the visible tests passed. It left `transfer` depositing into the destination before withdrawing from the source, so a failed transfer still credited the destination. v3 found that ordering bug in all three runs. Traces are in `evals/traces/`.
5. **Run-to-run variance is large, but task-dependent.** v1 scored 60% and then 20% on the harder set under identical settings, yet was perfectly steady at 80% on the held-out set. Single-run comparisons are unreliable.

## Limitations

- Small, hand-written benchmark (22 tasks, 5 of them held out). It is not SWE-bench.
- The held-out comparison between v1 and v3 rests on a single task (`22_overdraft`). Both prompts solved the other four every time.
- Three runs per setting is enough to see a consistent difference on one task, but not enough for statistical claims.
- The agent sometimes makes changes beyond what was asked (for example, extra input validation).
- Agent-run code executes on the host machine (a Docker sandbox is planned).
- Free-tier rate limits (about 500 requests per day) restrict how many repeated runs are practical.

## Run it

Setup (Windows PowerShell):

    python -m venv .venv
    .venv\Scripts\activate
    pip install google-genai python-dotenv pytest

Create a `.env` file containing `GEMINI_API_KEY=your-key`, then:

    python run_agent.py

Run the benchmark (three runs per task, prompt v3, held-out tasks):

    $env:PROMPT_VERSION="v3"
    $env:TAG="heldout"
    $env:RUNS="3"
    python evals\run_evals.py 18 19 20 21 22

Summarize the runs, or read one trace step by step:

    python evals\aggregate.py
    python evals\show_trace.py heldout_v1_run1_22_overdraft

## Roadmap

- Docker sandbox for running the tests
- Measure how minimal each fix is (lines changed)
- More held-out tasks and a larger sample
