# aat_llm — Project Context for Claude Code

## What this project is
aat_llm is a local LLM server (like Ollama) built with FastAPI and llama.cpp.
It runs on port 11435 and serves a REST API + streaming chat + web UI.

## Project structure
- server.py        → FastAPI backend, all API endpoints
- cli.py           → Terminal CLI (serve / run / list / pull / delete)
- model_manager.py → HuggingFace download, model list, delete helpers
- web/index.html   → Single-file dark-theme web UI
- models/          → GGUF model files live here
- test_server.py   → API endpoint tests (httpx + pytest)
- test_cli.py      → CLI tests (subprocess + pytest)
- test_gui.py      → Web UI tests (httpx + pytest)

## How to run
Start server:    python cli.py serve
Open UI:         http://localhost:11435
Pull a model:    python cli.py pull TheBloke/phi-2-GGUF phi-2.Q4_K_M.gguf
Chat via CLI:    python cli.py run phi-2.Q4_K_M.gguf "Hello"

## How to test
pytest test_server.py test_cli.py test_gui.py -v

## Key rules when editing this project
- Server always runs on port 11435
- Models are always referenced by filename only, never full path
- All API errors return JSON: { "error": "message" }
- Never show raw Python tracebacks in CLI output — use rich [red]...[/red]
- Streaming uses StreamingResponse with text/plain media type
- web/index.html must remain a single file — no separate JS or CSS files

## Dependencies
llama-cpp-python, fastapi, uvicorn, requests, huggingface_hub, rich, pytest, httpx, python-multipart

---

### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions)
- If something goes sideways, STOP and re-plan immediately - don't keep pushing
- Use plan mode for verification steps, not just building
- Write detailed specs upfront to reduce ambiguity
 
### 2. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution
 
### 3. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project
 
### 4. Verification Before Done
- Never mark a task complete without proving it works
- Diff behavior between main and your changes when relevant
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness
 
### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution"
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it
 
### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests - then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how
 
## Task Management
 
1. **Plan First**: Write plan to `tasks/todo.md` with checkable items
2. **Verify Plan**: Check in before starting implementation
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/todo.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections
 
## Core Principles
 
- **Simplicity First**: Make every change as simple as possible. Impact minimal code.
- **No Laziness**: Find root causes. No temporary fixes. Senior developer standards.

## gstack

- Use `/browse` for all web browsing — never use `mcp__claude-in-chrome__*` tools
- Available skills: `/plan-ceo-review`, `/plan-eng-review`, `/review`, `/ship`, `/browse`, `/qa`, `/setup-browser-cookies`, `/retro`
 
