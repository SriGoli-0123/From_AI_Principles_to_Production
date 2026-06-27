# Agentic AI Workbook Code Exercises & Solutions

Welcome to the companion code repository for the Agentic AI Workbook. This repository contains the simplified, first-principles examples, exercises, and official solutions for Chapters 1 through 11.

All code has been designed to run either against **OpenAI APIs** (if you have an API key) or **completely locally using Ollama** (with zero API keys needed).

---

## 🛠️ Step-by-Step Setup Guide

Follow these steps to set up the codebase on your local machine:

### 1. Clone this Repository
Open your terminal and run:
```bash
git clone https://github.com/your-username/agentic_ai_workbook_code.git
cd agentic_ai_workbook_code
```

### 2. Set Up a Python Virtual Environment
Creating a virtual environment ensures that the packages installed for this workbook do not conflict with your global system packages.
```bash
# Create the virtual environment
python3 -m venv venv

# Activate it (Mac/Linux)
source venv/bin/activate

# Activate it (Windows)
# venv\Scripts\activate
```

### 3. Install Dependencies
Install all required libraries (OpenAI, LangChain, LangGraph, Pydantic, etc.) using `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 4. Running Locally with Ollama (Optional & Recommended)
If you do not want to use OpenAI API keys, you can run all models locally using [Ollama](https://ollama.com/).

1. **Download and install Ollama** from [ollama.com](https://ollama.com/).
2. **Start Ollama** (either open the desktop application or run `ollama serve` in a background terminal).
3. **Pull the LLM and Embedding models** used in the book:
   ```bash
   ollama pull llama3
   ollama pull nomic-embed-text
   ```

All workbook scripts will automatically detect if `OPENAI_API_KEY` is absent in your environment variables and fallback to your local Ollama server seamlessly.

---

## 📁 Repository Structure

The code is organized under `harshith_scripts/` by chapter:

```text
harshith_scripts/
├── chapter1/
├── chapter2/
...
└── chapter11/
    ├── README.md             # Chapter-specific prerequisites and setup
    ├── examples/             # Simplified Python code examples
    ├── examples_output/      # Expected terminal output logs
    ├── exercises/            # Starter exercises (unsolved) for practice
    └── solutions/            # Complete, verified solutions
```

---

## 🚀 How to Run the Scripts

Each chapter contains chapter-specific instructions inside its own `README.md`.
To run any example or solution, make sure your virtual environment is active and run:
```bash
# Run an example:
python harshith_scripts/chapter3/examples/example1_react_loop.py

# Run a solution:
python harshith_scripts/chapter3/solutions/exercise3_1_solved.py
```
