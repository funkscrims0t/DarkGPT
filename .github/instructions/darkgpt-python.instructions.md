---
description: "Use when working in the DarkGPT repository on Python modules, tests, or small bug fixes. Covers debugging, change scope, and verification habits for this workspace."
applyTo: "**/*.py"
---
# DarkGPT Python Workflow Guidelines

- Reproduce the issue or failure before changing code.
- Prefer the smallest root-cause fix over broad refactors.
- Keep edits focused on the relevant module, test, or config file rather than sweeping changes.
- When touching behavior, update or add a targeted regression test when practical.
- Verify changes with the most relevant command available, such as pytest or a direct import check.
- Preserve existing patterns in the repository unless there is a clear reason to change them.
- Avoid introducing new dependencies or unrelated cleanup in the same change.
- Summarize the diagnosis, files changed, and verification evidence clearly.
