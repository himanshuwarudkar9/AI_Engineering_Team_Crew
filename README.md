# EngineeringTeam Crew - Trading Platform Builder

Welcome to the EngineeringTeam Crew project, powered by [crewAI](https://crewai.com). This multi-agent AI system uses specialized engineering agents to collaboratively design, develop, and test a complete trading simulation platform with an interactive web interface.

![freepik_candid_i_with_natural_textures_and_highly_realisti_96683](https://github.com/user-attachments/assets/e52bac3b-537d-410f-86d4-4c031a07adda)

## Project Overview

This project leverages four AI agents working together:
- **Engineering Lead**: Creates detailed system designs from requirements
- **Backend Engineer**: Implements Python backend logic for account management and trading
- **Frontend Engineer**: Builds interactive Gradio-based UI
- **Test Engineer**: Generates comprehensive unit tests

The agents collaborate to produce a fully functional trading platform saved in the `output/` directory.

# Application Preview
<img width="1914" height="873" alt="Screenshot 2026-01-19 224141" src="https://github.com/user-attachments/assets/f6764451-9abd-42b4-ba49-d41317cba3b2" />


*AI-generated trading simulation platform with account management, portfolio tracking, and transaction history*


# EngineeringTeam Crew - Trading Platform Builder

> A four-agent CrewAI system that takes plain-English requirements and autonomously generates a production-ready trading simulation platform — complete with backend logic, a Gradio UI, unit tests, and a system design document — all in a single `crewai run`.

![freepik_candid_i_with_natural_textures_and_highly_realisti_96683](https://github.com/user-attachments/assets/e52bac3b-537d-410f-86d4-4c031a07adda)

---

## Table of Contents

1. [Key Features](#key-features)
2. [Architecture](#architecture)
3. [Application Preview](#application-preview)
4. [Quick Start](#quick-start)
5. [Project Structure](#project-structure)
6. [Results & Benchmarks](#results--benchmarks)
7. [Technical Decisions](#technical-decisions)
8. [Customising the Platform](#customising-the-platform)
9. [Troubleshooting](#troubleshooting)
10. [Future Roadmap](#future-roadmap)

---

## Key Features

- **4-Agent Sequential Pipeline** — Engineering Lead → Backend Engineer → Frontend Engineer → Test Engineer; each agent's output feeds directly into the next as context.
- **Design-First Workflow** — The Engineering Lead produces a full Markdown design spec (`accounts.py_design.md`) before any code is written, enforcing a structured SDLC.
- **Self-Contained Backend** — AI-generated `accounts.py` handles account onboarding, deposit/withdraw, buy/sell shares with average-price tracking, P&L calculation, and transaction history.
- **Gradio UI Auto-Generation** — Frontend Engineer builds a working multi-tab Gradio app (`app.py`) directly from the backend module, runnable immediately after crew completion.
- **AI-Written Unit Tests** — Test Engineer produces `test_accounts.py` covering all edge cases (negative balance, invalid symbols, oversell).
- **Optional Docker Sandboxing** — Backend and test agents can be configured to execute and self-validate their code inside isolated Docker containers.
- **LLM-Agnostic** — All agents use Gemini 3 Flash by default; swap to any OpenAI-compatible model via a single `.env` change.
- **Fully Configurable via YAML** — Agent roles, goals, backstories, and task pipelines all live in `config/agents.yaml` and `config/tasks.yaml`.

---

## Architecture

```mermaid
flowchart TD
    subgraph Input["Input — main.py"]
        REQ["requirements: str\nmodule_name: str\nclass_name: str"]
    end

    subgraph Crew["CrewAI Sequential Pipeline"]
        direction TB
        A["Engineering Lead\n(gemini-3-flash-preview)\ndesign_task"]
        B["Backend Engineer\n(gemini-3-flash-preview)\ncode_task"]
        C["Frontend Engineer\n(gemini-3-flash-preview)\nfrontend_task"]
        D["Test Engineer\n(gemini-3-flash-preview)\ntest_task"]

        A -->|"design spec as context"| B
        B -->|"backend module as context"| C
        B -->|"backend module as context"| D
    end

    subgraph Output["output/ (generated files)"]
        O1["accounts.py_design.md\n(System Design)"]
        O2["accounts.py\n(Backend Logic)"]
        O3["app.py\n(Gradio UI)"]
        O4["test_accounts.py\n(Unit Tests)"]
    end

    subgraph Optional["Optional — Docker Sandbox"]
        DOC["Docker Container\nSafe code execution\n& auto-validation"]
    end

    REQ --> Crew
    A --> O1
    B --> O2
    C --> O3
    D --> O4
    B -.->|"allow_code_execution=True"| DOC
    D -.->|"allow_code_execution=True"| DOC
```

---

## Application Preview

<img width="1914" height="873" alt="Screenshot 2026-01-19 224141" src="https://github.com/user-attachments/assets/f6764451-9abd-42b4-ba49-d41317cba3b2" />

*AI-generated trading simulation platform with account management, portfolio tracking, and transaction history*

---

## Quick Start

### Prerequisites

| Requirement | Notes |
|---|---|
| Python | `>=3.10, <3.13` |
| [UV](https://docs.astral.sh/uv/) | Fast Python package manager |
| Gemini or OpenAI API key | Gemini 3 Flash used by default |
| Docker Desktop *(optional)* | For safe agent code execution |

### 1. Install UV

```bash
pip install uv
```

### 2. Install project dependencies

```bash
cd engineering_team
crewai install
```

### 3. Configure API keys

Create or edit the `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
# or
OPENAI_API_KEY=your_openai_api_key_here
```

### 4. Run the crew

```bash
crewai run
```

The crew runs four tasks in sequence and writes all outputs to `output/`:

| Step | Agent | Output file |
|---|---|---|
| 1 | Engineering Lead | `output/accounts.py_design.md` |
| 2 | Backend Engineer | `output/accounts.py` |
| 3 | Frontend Engineer | `output/app.py` |
| 4 | Test Engineer | `output/test_accounts.py` |

### 5. Launch the generated trading app

```bash
cd output
uv add gradio
uv run app.py
```

Open `http://localhost:7860` in your browser.

---

## Project Structure

```
engineering_team/
├── src/engineering_team/
│   ├── crew.py              # Agent & task definitions (CrewBase)
│   ├── main.py              # Entry point — define requirements here
│   └── config/
│       ├── agents.yaml      # Agent roles, goals, backstories, LLM
│       └── tasks.yaml       # Task descriptions, expected outputs, output files
├── output/                  # All AI-generated files land here
│   ├── accounts.py          # Generated backend (Account class)
│   ├── app.py               # Generated Gradio UI
│   ├── test_accounts.py     # Generated unit tests
│   └── accounts.py_design.md # Generated system design document
├── knowledge/
│   └── user_preference.txt  # Optional crew knowledge source
├── pyproject.toml           # UV/Hatchling project config
└── .env                     # API keys (not committed)
```

---

## Results & Benchmarks

| Metric | Value |
|---|---|
| Agents | 4 (Lead, Backend, Frontend, Test) |
| LLM | Gemini 3 Flash Preview |
| Execution process | Sequential (deterministic ordering) |
| Tasks per run | 4 tasks, each with file output |
| Avg. end-to-end run time | ~3–6 minutes (Gemini API latency dependent) |
| Generated backend | ~150–200 lines — full `Account` class with 7 methods |
| Generated UI | Multi-tab Gradio app: onboarding, trade panel, portfolio view, transaction history |
| Generated tests | Edge-case coverage: invalid inputs, insufficient funds, unknown symbols, oversell |
| Supported stock symbols | COALINDIA (₹450), MARICO (₹670), ICICIAMC (₹1200) via `get_share_price()` |
| Code execution mode | Disabled by default; Docker sandbox available |

> Run time is network-bound. With Docker execution enabled, agents self-validate output and retry up to 5 times before finalising.

---

## Technical Decisions

### CrewAI over LangGraph / AutoGen
- **Declarative YAML config** — agent roles and task flows are defined in `agents.yaml` / `tasks.yaml` without writing graph wiring code.
- **Built-in context chaining** — CrewAI's `context:` field in `tasks.yaml` automatically passes the output of `design_task` into `code_task`, mimicking a real code-review handoff with zero boilerplate.
- **`crewai run` CLI** — single-command execution with built-in retry logic and verbose tracing.

### Sequential process over Hierarchical
- The SDLC has a strict dependency order: design → code → UI/tests. A sequential process enforces this without a manager LLM adding cost and latency.

### Gemini 3 Flash over GPT-4o
- **Cost** — Flash tier is significantly cheaper at the output token volumes generated (150–200 lines of Python per task).
- **Speed** — Lower time-to-first-token reduces total crew runtime.
- **Swappable** — Changing `llm:` in `agents.yaml` to `openai/gpt-4o` is a one-line change; no code modification needed.

### YAML-defined agents over hardcoded Python
- Separating configuration from logic means changing an agent's LLM, role, or goal requires editing a YAML file rather than touching `crew.py`, reducing the risk of introducing bugs during prompt iteration.

### Optional Docker sandboxing (disabled by default)
- Enabling `allow_code_execution=True` with `code_execution_mode="safe"` lets Backend and Test agents run their output inside an isolated Docker container and self-correct on errors. It is opt-in because it requires Docker Desktop and increases run time.

### Design-first task ordering
- Requiring the Engineering Lead to output a Markdown spec first grounds all downstream agents. The backend agent receives exact function signatures to implement, reducing hallucinated APIs and improving inter-agent consistency.

---

## Customising the Platform

### Change the requirements

Edit `src/engineering_team/main.py`:

```python
requirements = """
Your custom requirements here...
"""
module_name = "my_module.py"
class_name = "MyClass"
```

### Enable Docker code execution

Uncomment the relevant lines in `src/engineering_team/crew.py` for `backend_engineer` and `test_engineer`:

```python
allow_code_execution=True,
code_execution_mode="safe",   # uses Docker
max_code_execution_time=240,
max_retries=5,
```

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `503 Service Unavailable` | Gemini/OpenAI rate limit — wait 5–10 minutes and retry |
| `Docker is not installed` | Comment out `allow_code_execution` lines in `crew.py`, or install Docker Desktop |
| `ModuleNotFoundError: gradio` | Run `uv add gradio` inside the `output/` directory before `uv run app.py` |

---

## Future Roadmap

- [ ] **Live market data** — Replace the `get_share_price()` mock with a real NSE/BSE API (e.g., `yfinance` or Alpha Vantage).
- [ ] **Parallel execution** — Run Frontend and Test engineers concurrently after the Backend task, cutting total run time roughly in half.
- [ ] **Multi-module generation** — Support requirements that span several Python modules (e.g., separate `auth.py`, `portfolio.py`, `orders.py`).
- [ ] **Persistent crew memory** — Use CrewAI's long-term memory store so agents learn from previous runs and avoid repeating design mistakes.
- [ ] **Automated test runner** — Post-crew hook that runs `pytest output/test_accounts.py` and feeds failures back to the Test Engineer for self-correction.
- [ ] **Streaming output UI** — Gradio/Streamlit dashboard showing agent logs and generated code in real-time as the crew runs.
- [ ] **Generalised project generator** — Fully parameterise the crew so any spec sheet generates a complete Python project, not just a trading platform.
- [ ] **CI/CD integration** — GitHub Actions workflow that runs the crew on push, commits generated files, and opens a PR for human review.

---

## License

This project uses the [crewAI](https://crewai.com) framework. Refer to their repository for licensing details. Always review AI-generated code in the `output/` directory before deploying to production.


