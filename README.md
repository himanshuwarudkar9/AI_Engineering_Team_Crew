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


## Installation

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management.

### Step 1: Install UV

```bash
pip install uv
```

### Step 2: Install Project Dependencies

Navigate to your project directory and install:

```bash
cd engineering_team
crewai install
```

### Step 3: Configure API Keys

**Add your `GEMINI_API_KEY` or `OPENAI_API_KEY` into the `.env` file:**

```ini
GEMINI_API_KEY=your_api_key_here
# or
OPENAI_API_KEY=your_api_key_here
```

## Running the Project

### Generate the Trading Platform

Run the crew to generate the complete application:

```bash
crewai run
```

This will:
1. Create a detailed system design (`output/accounts.py_design.md`)
2. Generate backend code (`output/accounts.py`)
3. Build the frontend UI (`output/app.py`)
4. Create unit tests (`output/test_accounts.py`)

### Run the Generated Application

After the crew completes, navigate to the output folder and run the app:

```bash
cd output
uv add gradio
uv run app.py
```

The trading platform will launch in your browser at `http://localhost:7860`

## Important: Docker & Code Execution

### About Safe Code Execution

CrewAI supports **safe code execution** mode, which uses Docker containers to isolate and securely execute generated code. This prevents potentially harmful code from affecting your system.

**Current Configuration:** Code execution is **disabled** in this project (lines commented out in `src/engineering_team/crew.py`).

### Enabling Code Execution (Optional)

If you have Docker installed and want agents to test code automatically:

1. **Install Docker Desktop** from [docker.com](https://www.docker.com/products/docker-desktop/)

2. **Uncomment code execution lines** in `src/engineering_team/crew.py`:

```python
@agent
def backend_engineer(self) -> Agent:
    return Agent(
        config=self.agents_config['backend_engineer'],
        verbose=True,
        allow_code_execution=True,      # Uncomment
        code_execution_mode="safe",     # Uncomment (uses Docker)
        max_code_execution_time=240,    # Uncomment
        max_retries=5,                  # Uncomment
    )

@agent
def test_engineer(self) -> Agent:
    return Agent(
        config=self.agents_config['test_engineer'],
        verbose=True,
        allow_code_execution=True,      # Uncomment
        code_execution_mode="safe",     # Uncomment (uses Docker)
        max_code_execution_time=240,    # Uncomment
        max_retries=5,                  # Uncomment
    )
```

3. **Run the crew again:**

```bash
crewai run
```

With Docker enabled, agents can validate their code automatically during generation.

## Project Structure

```
engineering_team/
├── src/engineering_team/
│   ├── crew.py              # Agent definitions
│   ├── main.py              # Entry point with requirements
│   └── config/
│       ├── agents.yaml      # Agent configurations
│       └── tasks.yaml       # Task definitions
├── output/                  # Generated application files
│   ├── accounts.py          # Backend trading logic
│   ├── app.py              # Gradio web interface
│   ├── test_accounts.py    # Unit tests
│   └── accounts.py_design.md # System design document
└── .env                    # API keys (create this)
```

## Customizing the Platform

### Modify Requirements

Edit `src/engineering_team/main.py` to change the trading platform requirements:

```python
requirements = """
Your custom requirements here...
"""
```

### Configure Agents

- **Agents**: Modify `src/engineering_team/config/agents.yaml`
- **Tasks**: Modify `src/engineering_team/config/tasks.yaml`
- **Logic**: Modify `src/engineering_team/crew.py`

## Features of Generated Trading Platform

- ✅ User account creation and onboarding
- ✅ Deposit and withdraw funds with validation
- ✅ Buy/sell shares with real-time price lookup
- ✅ Portfolio value calculation with P&L tracking
- ✅ Transaction history with filtering
- ✅ Interactive Gradio web interface
- ✅ Comprehensive error handling and validation

## Troubleshooting

### API Rate Limits / Model Overloaded

If you see `503 Service Unavailable` errors:
- Wait 5-10 minutes and retry
- The LLM provider (Gemini/OpenAI) may be temporarily overloaded
- The crew has automatic retry logic built-in

### Docker Not Found Error

If you see `Docker is not installed` error:
- Ensure code execution lines are **commented out** in `crew.py`
- Or install Docker Desktop and uncomment those lines

### Missing Gradio Module

If `uv run app.py` fails:
```bash
cd output
uv add gradio
uv run app.py
```

## Support

For support, questions, or feedback:
- Visit [crewAI documentation](https://docs.crewai.com)
- [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with docs](https://chatg.pt/DWjSBZn)

## License

This project uses crewAI framework. Check their repository for licensing details.

---

**Note:** Always review generated code in the `output/` directory before running it in production environments. The agents generate functional code, but manual review ensures it meets your specific security and business requirements.
