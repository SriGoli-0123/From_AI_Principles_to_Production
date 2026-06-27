# Chapter 1: The "Hello World" Agent Loop

This directory contains the code assets and exercises for Chapter 1.

## Prerequisites & Setup
To run the scripts in this chapter, make sure you have:
1. Installed the `openai` Python SDK:
   ```bash
   pip install openai
   ```
2. Downloaded and run Ollama locally for zero-cost execution (if you don't have an OpenAI API key):
   * Visit [ollama.com](https://ollama.com) to download.
   * Run the Llama 3 model in your terminal:
     ```bash
     ollama run llama3
     ```
     *(Note: The scripts will automatically detect whichever model is installed on your local Ollama instance if you pulled another version like `llama3.1` or `qwen2.5`).*
