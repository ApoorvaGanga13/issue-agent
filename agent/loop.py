import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

from agent.tools import RepoTools
from agent.prompts import SYSTEM_PROMPT
from agent.prompts import PROMPT_VERSION

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# This model name passed your check_gemini.py test
MODEL = "gemini-flash-lite-latest"

# Tool descriptions the model sees
TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="list_files",
        description="List files in the repo (optionally inside a subdirectory).",
        parameters={
            "type": "OBJECT",
            "properties": {"subdir": {"type": "STRING"}},
        },
    ),
    types.FunctionDeclaration(
        name="read_file",
        description="Read the contents of a file.",
        parameters={
            "type": "OBJECT",
            "properties": {"path": {"type": "STRING"}},
            "required": ["path"],
        },
    ),
    types.FunctionDeclaration(
        name="search",
        description="Search all source files for a text pattern.",
        parameters={
            "type": "OBJECT",
            "properties": {"pattern": {"type": "STRING"}},
            "required": ["pattern"],
        },
    ),
    types.FunctionDeclaration(
        name="edit_file",
        description="Replace exactly one occurrence of `old` with `new` in a file.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "path": {"type": "STRING"},
                "old": {"type": "STRING"},
                "new": {"type": "STRING"},
            },
            "required": ["path", "old", "new"],
        },
    ),
    types.FunctionDeclaration(
        name="run_tests",
        description="Run the test suite and return the output.",
    ),
]


def call_model(contents, config, retries=4):
    """Call the model; wait and retry when the free tier rate-limits us."""
    for attempt in range(retries):
        try:
            return client.models.generate_content(
                model=MODEL, contents=contents, config=config
            )
        except Exception as e:
            msg = str(e)
            if "429" in msg or "503" in msg or "RESOURCE_EXHAUSTED" in msg:
                wait = 30 * (attempt + 1)
                print(f"\n[{MODEL}] {msg[:400]}")
                print(f"Waiting {wait}s (attempt {attempt + 1}/{retries})...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Model kept failing after retries")


def run_agent(repo_path: str, issue: str, max_steps: int = 15) -> dict:
    tools = RepoTools(repo_path)
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_PROMPT,
        tools=[types.Tool(function_declarations=TOOL_DECLARATIONS)],
        # We run the loop ourselves so we can log and measure every step
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=f"Issue to fix:\n\n{issue}")],
        )
    ]
    trace = []

    for step in range(1, max_steps + 1):
        response = call_model(contents, config)
        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            return {"summary": "Stopped: empty model response", "steps": step, "trace": trace}
        contents.append(candidate.content)

        # Record any text the model wrote (its reasoning)
        for p in candidate.content.parts:
            if p.text:
                trace.append({"step": step, "type": "text", "text": p.text})

        calls = [p.function_call for p in candidate.content.parts if p.function_call]

        # No tool requested means the agent is done
        if not calls:
            return {"summary": response.text, "steps": step, "trace": trace}

        # Run every tool the model asked for and send the results back
        result_parts = []
        for call in calls:
            args = dict(call.args)
            print(f"[step {step}] {call.name}({args})")
            try:
                output = getattr(tools, call.name)(**args)
            except Exception as e:
                output = f"Error: {e}"
            trace.append({
                "step": step, "type": "tool", "tool": call.name,
                "args": args, "output": str(output)[:1500],
            })
            result_parts.append(
                types.Part.from_function_response(
                    name=call.name, response={"result": str(output)}
                )
            )
        contents.append(types.Content(role="user", parts=result_parts))

    return {"summary": "Stopped: max steps reached", "steps": max_steps, "trace": trace}

    for step in range(1, max_steps + 1):
        response = call_model(contents, config)
        candidate = response.candidates[0]
        if not candidate.content or not candidate.content.parts:
            return {"summary": "Stopped: empty model response", "steps": step}
        contents.append(candidate.content)

        calls = [p.function_call for p in candidate.content.parts if p.function_call]

        # No tool requested means the agent is done
        if not calls:
            return {"summary": response.text, "steps": step}

        # Run every tool the model asked for and send the results back
        result_parts = []
        for call in calls:
            args = dict(call.args)
            print(f"[step {step}] {call.name}({args})")
            try:
                output = getattr(tools, call.name)(**args)
            except Exception as e:
                output = f"Error: {e}"
            result_parts.append(
                types.Part.from_function_response(
                    name=call.name, response={"result": str(output)}
                )
            )
        contents.append(types.Content(role="user", parts=result_parts))

    return {"summary": "Stopped: max steps reached", "steps": max_steps}