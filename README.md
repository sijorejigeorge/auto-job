# auto-job: Autonomous Job Search Browser Agent

## Overview

**auto-job** is a Python-based browser automation agent designed to help users search and apply for jobs on web pages. It leverages Playwright for browser control and integrates with an LLM (Ollama, LangChain) to plan and execute actions step by step. The agent uses a feedback loop, extracting browser state and page content after each action, and asks the LLM what to do next until the goal is reached.

## Features
- Multi-step job search and application automation
- LLM-driven planning and action execution
- Feedback loop: browser state and page content sent to LLM after each step
- Supports multiple tabs/URLs in parallel
- Robust action execution with retries and error handling
- Modular codebase for easy extension
- Docker support for easy deployment

## How It Works
1. User provides one or more URLs and a job search instruction.
2. The agent opens each URL in a browser tab.
3. For each tab, the agent:
	- Extracts browser state and page content
	- Sends a prompt (with context) to the LLM
	- Receives a TODO list and JSON actions
	- Executes actions (type, click, wait, scroll, etc.)
	- Updates the TODO list and history
	- Repeats until tasks are complete or user stops

## Requirements
- Python
- Docker (optional, for containerized runs)
- Playwright
- LangChain (community)
- Ollama (LLM server)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
### Local Run
```bash
python main.py
```

### Docker Run
Build and run the container:
```bash
docker build -t auto-job .
docker run -it --rm -e DISPLAY=host.docker.internal:0 -v /tmp/.X11-unix:/tmp/.X11-unix auto-job
```

## File Structure
- `main.py` — Entry point, handles user input and agent orchestration
- `agent_runner.py` — Runs agents for each tab/URL, manages feedback loop
- `agent.py` — Playwright browser logic
- `llm.py` — LLM client (Ollama via LangChain)
- `prompt_example.py` — Example JSON action list for LLM prompt
- `action_executor.py` — Executes browser actions with retries
- `browser_state.py` — Extracts browser state and page info
- `history.py` — Tracks agent history and actions
- `requirements.txt` — Python dependencies
- `Dockerfile` — Docker setup for containerized runs
- `.dockerignore` — Files to ignore in Docker builds
- `system_prompt.md` — System prompt template for LLM
- `todo.md` — TODO list for agent planning

## Example LLM Prompt
See `prompt_example.py` for a sample JSON action list.


## Extending
- Add new actions in `action_executor.py`
- Refine browser state extraction in `browser_state.py`
- Update prompt templates in `system_prompt.md`
- Integrate with other LLMs by modifying `llm.py`

---

**Note:**
The intelligence and reliability of this agent are strongly influenced by the capabilities of the underlying LLM. More advanced models will produce better plans, handle complex page layouts, and adapt to dynamic web content more effectively. For best results, use the most capable LLM available to you.