# Modernize the OpenAI integration

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds. It is maintained according to `PLANS.md` at the repository root.

## Purpose / Big Picture

After this work, a user can start `python main.py`, provide a permitted query, and have the application use a supported OpenAI client and the Responses API instead of retired GPT-4 model names and legacy Chat Completions function calls. The command-line interface will display the final model text just as it does today, and automated tests will prove the tool-call round trip without sending network traffic or requiring credentials.

## Progress

- [x] (2026-07-12 00:00Z) Inspected the existing OpenAI integration and ran the existing import and CLI startup checks.
- [x] (2026-07-12 00:00Z) Verified current model and API guidance from official OpenAI documentation fallback after configuring the Docs MCP connector for future sessions.
- [x] (2026-07-12 00:00Z) Replaced the legacy API integration and model defaults.
- [x] (2026-07-12 00:00Z) Added isolated tests for no-key and Responses API tool-call behavior.
- [x] (2026-07-12 00:00Z) Installed OpenAI 2.45.0, refreshed the editable package installation, and ran the complete test and startup checks.

## Surprises & Discoveries

- Observation: creating the pinned `openai==1.13.3` client fails before any API request because it passes a removed `proxies` keyword to the installed HTTP dependency.
  Evidence: `.venv/bin/python` raised `TypeError: __init__() got an unexpected keyword argument 'proxies'` while evaluating `Client(api_key='test')`.
- Observation: the existing test only imports the package and does not construct the client or exercise a model request.
  Evidence: `tests/test_import.py` contains one `hasattr` assertion group.
- Observation: the sandbox initially prevents dependency downloads, but the virtual environment installs and tests correctly once the scoped network permission is granted.
  Evidence: `openai-2.45.0` and `jiter-0.16.0` installed successfully; `pytest` reported `3 passed`.

## Decision Log

- Decision: migrate from Chat Completions to the Responses API and choose the current `gpt-5.6` alias as the default model.
  Rationale: the official model guide recommends GPT-5.6 for general API usage, and the current models support function calling through the Responses API. The existing `gpt-4-1106-preview` and `gpt-4` calls are obsolete.
  Date/Author: 2026-07-12 / Codex
- Decision: retain the one-query CLI flow and keep DeHashed access as the application-provided function tool.
  Rationale: this limits the update to the OpenAI integration and avoids changing the product workflow.
  Date/Author: 2026-07-12 / Codex
- Decision: validate behavior with a fake Responses client and mocked DeHashed lookup.
  Rationale: tests must be deterministic and must not expose credentials or make external requests.
  Date/Author: 2026-07-12 / Codex
- Decision: document `OPENAI_API_KEY` and the optional `OPENAI_MODEL` override in the existing setup instructions.
  Rationale: the original instructions mentioned only the DeHashed key, which would leave a modernized installation unable to configure its required OpenAI client.
  Date/Author: 2026-07-12 / Codex

## Outcomes & Retrospective

The application now defaults to `gpt-5.6` and allows an account-specific override through `OPENAI_MODEL`. It uses the Responses API's function-call-output flow, and it depends on OpenAI 2.x rather than the incompatible pinned 1.13.3 SDK. The deterministic test suite passes with three tests, and the normal CLI entry point starts and exits cleanly. The pre-existing urllib3 LibreSSL warning remains; it is environmental and did not prevent the migration from passing.

## Context and Orientation

`darkgpt/DarkAgent.py` owns model selection and calls OpenAI twice: first to select the DeHashed lookup arguments, then to formulate a user-facing answer. `darkgpt/functions.py` defines that lookup as a legacy function schema. `darkgpt/dehashed_api.py` performs the lookup. `darkgpt/cli.py` sends each entered line to `DarkGPT.GPT_with_function_output` and supplies a callback for visible output. Dependency declarations appear in `requirements.txt` and `setup.cfg`.

The Responses API is OpenAI's current unified text and tool-use interface. A function tool is a JSON schema that lets a model request a local Python operation. The program must execute that operation itself and return a `function_call_output` item associated with the model-provided call ID before asking the model for its final text.

## Plan of Work

Update `darkgpt/functions.py` to express `dehashed_search` as a strict Responses function tool with optional `mail` and `nickname` fields. Update `darkgpt/DarkAgent.py` to construct `OpenAI`, read `OPENAI_MODEL` with `gpt-5.6` as its default, create one Responses request with the router instructions and tool, process every requested `dehashed_search` call, and create a second Responses request containing the original response output and the local function outputs. The second response's `output_text` becomes the CLI output. Preserve a useful no-key result and call the supplied callback when one exists.

Remove the obsolete hard-coded GPT-4 model calls and legacy `functions=` parameter. Use a JSON serialization for the tool result so it is valid tool output even when the lookup returns a Python value other than a string.

Update `requirements.txt` and `setup.cfg` to use a modern, compatible OpenAI SDK major-version range. Update `README.md` so its environment-variable example includes the OpenAI key and optional model override. Add tests in `tests/test_dark_agent.py` that replace the client and lookup with fakes. One test will assert that a no-key instance avoids API calls. A second will supply a fake function-call response followed by a final response and assert that the tool arguments, returned call ID, final output, and callback behavior are all correct.

## Concrete Steps

Run these commands from `/Users/frankierodriguez/Projects/Tools/DarkGPT` after editing:

    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python -m pytest
    printf 'exit\\n' | .venv/bin/python main.py

The test command should report all import and new agent tests passing. The final command should print the banner, the welcome prompt, and `Sesión terminada.` without contacting the API.

## Validation and Acceptance

Acceptance is met when the test suite proves that the code sends the declared function tool to `client.responses.create`, executes the requested local lookup, submits a matching `function_call_output`, and relays the resulting final text through the CLI callback. It is also met when the client can be constructed with the installed dependency set and the existing `exit` startup interaction completes successfully.

## Idempotence and Recovery

The code and test edits are repeatable. Dependency installation may be run again safely. If an account does not have access to the default model, set `OPENAI_MODEL` in `.env` to another current Responses- and function-calling-capable model without editing source. No test sends API requests or uses the real `.env` values.

## Artifacts and Notes

Official guidance consulted: the [OpenAI models guide](https://developers.openai.com/api/docs/models) identifies `gpt-5.6` as the current general default and states that current models are available through the Responses API; the [model capability listing](https://developers.openai.com/api/docs/models/compare) records function-calling and streaming support for current GPT models.

## Interfaces and Dependencies

At completion, `darkgpt.DarkAgent.DarkGPT` will expose `execute_function_call(message: str) -> str` and `GPT_with_function_output(historial: list, callback=None) -> str`. The module will use `OpenAI` from the `openai` package and invoke `client.responses.create(model=..., instructions=..., input=..., tools=...)`. The final response will be read from `response.output_text`. The package dependency will allow OpenAI SDK version 2 or later and exclude version 3 until it is intentionally evaluated.

Plan updated on 2026-07-12 because the dependency incompatibility makes a model-string-only update insufficient.

Plan updated on 2026-07-12 after implementation and validation to record the installed SDK version, test evidence, and remaining environment warning.
