# issue-agent

A small coding agent that reads a bug report, explores a Python repo, edits the code, runs the tests, and produces a fix, plus an evaluation harness that measures **how often its fixes are actually correct**, not just whether the visible tests pass.

Built from scratch with the Gemini API (free tier) and plain Python. No agent frameworks.

## How it works

    issue text + repo -> agent loop (LLM + tool calls) -> edited repo -> tests (Docker sandbox)
                              |
       tools: list_files, read_file, search, edit_file, run_tests

- `agent/tools.py`: repo tools. Paths are restricted to the repo, and `edit_file` only accepts an unambiguous single match. Tests run through `run_pytest`, which can use the Docker sandbox.
- `agent/loop.py`: the tool-calling loop, with retries for rate limits and a full step-by-step trace of every run.
- `agent/prompts.py`: versioned system prompts (v1, v2, v3) so prompt changes can be compared fairly.
- `fix.py`: command-line tool that runs the agent on any repo plus issue text, shows a diff, and only changes your files with `--apply`.
- `evals/`: the benchmark tasks, runner, and analysis scripts (`aggregate.py`, `show_trace.py`, and `fix_size.py`, an approximate count of lines changed per fix).
- `sandbox/image/Dockerfile`: the test-runner image.

## Web interface

A small FastAPI backend plus a single-page frontend (`app.py`, `static/index.html`). Pick an example bug or paste your own code and tests, choose the prompt version, and watch the agent's tool calls live. When it finishes you see the diff, whether the visible tests pass, and, for the example bugs, whether the hidden tests pass.

    pip install -r requirements.txt
    $env:SANDBOX="docker"
    python -m uvicorn app:app --port 8000

Then open http://127.0.0.1:8000. Run it only on your own machine: it executes test code, so do not expose it to the internet.

## Docker sandbox

Model-written code should not run on the machine that holds your secrets. With `SANDBOX=docker`, every test run, including the benchmark scoring step that runs the agent's code plus the hidden tests, happens in a container with:

- no network access,
- the repo mounted read-only (no `.env` or other files of mine are visible),
- limits of 512 MB memory, 1 CPU, 128 processes, and 60 seconds,
- a non-root user, and a fresh container for every run.

If Docker itself fails, the harness stops with a sandbox error instead of counting it as a failed task. The sandbox covers test execution only. The agent's file edits happen in a working copy of the repo, and Docker is not a perfect security boundary. The default is `SANDBOX=off`.

## How the evaluation works

Each task is a small buggy repo with an issue description. Scoring is stricter than "the tests pass":

- **Hidden tests.** The agent only sees a few tests. After it finishes, extra tests it never saw are added and everything is re-run.
- **OVERFIT label.** The agent passes the visible tests but fails the hidden ones, meaning it fixed the symptom and not the root cause.
- **Tamper check.** Editing the visible test files counts as a failure.
- **Vague issues.** Some issues describe symptoms only ("customers are charged the wrong amount") without naming the file or function.
- **Repeated runs.** LLM output varies between runs, so experiments are repeated and the spread is reported.

## Results

Model: `gemini-flash-lite-latest` (free tier). The tasks are small bugs written by me with AI assistance, so read these as a pilot study.

| Task set | Prompt | Runs | Hidden-test solve rate |
|---|---|---|---|
| 12 easy single-file bugs (visible tests only) | v1 | 1 | 12/12 (benchmark saturated, so I made harder tasks) |
| 5 harder tasks with hidden tests | v1 | 2 | 60%, then 20% (high variance) |
| 5 harder tasks | v2 | 1 | 100% (contaminated, see below) |
| 5 harder tasks | v3 | 1 | 100% |
| 5 held-out tasks (18-22) | v1 | 3 | 80%, 80%, 80% |
| 5 held-out tasks (18-22) | v3 | 3 | 100%, 100%, 100% |
| 5 more held-out tasks (23-27) | v1 | 2 | 60%, 80% |
| 5 more held-out tasks (23-27) | v3 | 2 | 100%, 100% |
| 5 held-out tasks (18-22), tests run in the Docker sandbox | v3 | 1 | 100% (matches the unsandboxed runs) |

Across all 10 held-out tasks, v1 solved 19 of 25 task-runs (76%) and v3 solved 25 of 25 (100%). v1's misses came from three tasks: `22_overdraft` (0 of 3), `26_pagination` (1 of 2), and `27_median` (0 of 2). Both prompts solved the other seven tasks in every run.

## What I learned

1. **A saturated benchmark tells you nothing.** The first 12 tasks were solved 12/12, so I added hidden tests and vaguer issues to get a baseline with room to improve.
2. **Passing visible tests is not the same as being correct.** On the hard tasks, prompt v1 often passed the visible tests and failed the hidden ones (OVERFIT).
3. **I found leakage in my own experiment.** Prompt v2 listed example edge cases that overlapped with the hidden tests, so its 100% is contaminated. Prompt v3 removed the task-specific hints and I evaluated it on held-out tasks that no prompt had been tuned on.
4. **Concrete failure example.** On `22_overdraft`, v1 added a balance check to `withdraw` and stopped once the visible tests passed. It left `transfer` depositing into the destination before withdrawing from the source, so a failed transfer still credited the destination. v3 found that ordering bug in all three runs. Traces are in `evals/traces/`. I have only inspected this one task in detail so far.
5. **Run-to-run variance is large, but task-dependent.** v1 scored 60% and then 20% on the harder set under identical settings, yet was perfectly steady at 80% on tasks 18-22. Single-run comparisons are unreliable.

## Limitations

- Small benchmark (27 tasks, 10 of them held out), hand-made rather than taken from real projects. It is not SWE-bench.
- Tasks 23-27 were written after seeing v1 fail on task 22, so they may lean toward the failure type that v3 targets.
- Hidden tests check edge cases by design, which suits a prompt that asks the agent to think about edge cases. Real issues do not come with hidden tests.
- Two to three runs per setting is enough to see a consistent difference, but not enough for statistical claims. Repeated runs of the same task are not independent.
- Only one model was tested, and the Docker sandbox was verified with a single benchmark run.
- The agent sometimes makes changes beyond what was asked (for example, extra input validation).
- Free-tier rate limits (about 500 requests per day) restrict how many repeated runs are practical.

## Why v1 failed

`evals/why_failed.py` replays the edits recorded in each saved trace onto the original task repo and runs the hidden tests against the result. `evals/trace_findings.md` lists, for every saved run of the tasks where v1 struggled, which tests failed and the code the agent wrote, next to the v3 runs for comparison.

## Run it

Setup (Windows PowerShell):

    python -m venv .venv
    .venv\Scripts\activate
    pip install google-genai python-dotenv pytest

Create a `.env` file containing `GEMINI_API_KEY=your-key`, then run the agent on any repo:

    python fix.py path\to\repo "describe the bug here"

To use the Docker sandbox, start Docker Desktop, then build the image once and turn the sandbox on:

    docker build -t issue-agent-sandbox sandbox\image
    $env:SANDBOX="docker"

Run the benchmark (three runs per task, prompt v3, held-out tasks):

    $env:PROMPT_VERSION="v3"
    $env:TAG="heldout"
    $env:RUNS="3"
    python evals\run_evals.py 18 19 20 21 22

Summarize the runs, or read one trace step by step:

    python evals\aggregate.py
    python evals\show_trace.py heldout_v1_run1_22_overdraft

## Roadmap

- Tasks taken from real open-source bug reports
- Test with a second model
