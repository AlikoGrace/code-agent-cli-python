
# Code Agent CLI (Python)

A command-line AI coding agent that can understand a repository and perform actions through OpenAI-compatible tool calls.

The agent is designed to work like modern coding assistants: it can inspect a codebase, plan changes, read files, apply edits, run commands/tests, and iterate based on tool output.

## What it does
- Accepts a natural language task from the terminal
- Uses an LLM to reason about the task
- Calls tools to interact with the local repository (read/search/edit/run)
- Iterates in a loop until the task is completed
- Produces a final summary of actions taken

## Supported Capabilities
- Chat completion via OpenRouter (OpenAI-compatible API)
- Tool calling (function-call style)
- Repository file reading
- Repository file editing (patch-based)
- Running shell commands (tests, linting, builds)
- Multi-step agent loop (plan → act → observe → refine)

## Tech Stack
- Python
- OpenRouter (OpenAI-compatible API)
- uv (dependency management)

## Setup

### 1) Create a `.env` file
Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
USE_FREE=true

```

### 2) Install dependencies
```env
uv sync
```
### 3) Run the agent
```env
uv run python app/main.py -p "Hello"
```
Notes
This project uses OpenRouter, so you can switch between different models (including free routes) without changing code.

For local development, the agent is designed to run safely within the repository root.

Acknowledgements

This project was built as part of the CodeCrafters ["Build Your own Claude Code" Challenge](https://codecrafters.io/challenges/claude-code).

