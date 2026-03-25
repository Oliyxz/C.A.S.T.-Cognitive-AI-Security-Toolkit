# GenAI Vulnerability Lab - Setup Guide

Welcome to the **GenAI Vulnerability Lab** (aka "The Glass Box Bot"). This tool demonstrates how LLMs can accidentally reveal sensitive data through prompt injection.

## 1. Install Prerequisites

### A. Install Ollama (The AI Engine)
This project uses **Ollama** to run the AI model locally on your machine.
1.  Download Ollama from [ollama.com](https://ollama.com).
2.  Install and run the application.
3.  Open a terminal and pull the default model (Llama 3):
    ```bash
    ollama pull llama3
    ```
    *(Note: You can change the model in `config.yaml` later).*

### B. Python Environment
We recommend using **Anaconda**.
1.  Create the environment:
    ```bash
    conda create -n social_eng_toolkit python=3.10
    ```
2.  Activate it:
    ```bash
    conda activate social_eng_toolkit
    ```

## 2. Installation

1.  Navigate to this folder in your terminal:
    ```bash
    cd jailbroken_ai
    ```
2.  Install the project dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 3. Running the Lab

1.  Ensure Ollama is running in the background.
2.  Start the Streamlit application:
    ```bash
    streamlit run src/app.py
    ```
3.  The web interface will open automatically in your browser.

## 4. How to Use
- **Left Sidebar**: 
    - Change **Security Levels** to see how the AI defends itself (or fails to).
    - Enable **"Hacker View"** to see the hidden System Prompt and Data Context.
- **Chat**: Try to trick the bot into revealing the secret "Project Omega" details or Executive Salaries.

## 5. Auto-Reinforcement Loop ("War Game")

This project includes a self-improving security loop where a "Red Team" AI attacks a "Blue Team" AI.

### How it Works
1.  **Red Team**: Tries to breach the system using evolved social engineering strategies.
2.  **Blue Team**: Analyzes successful breaches and patches the system prompt (creating new levels).
3.  **Gold Team**: Verifies that new security rules don't break legitimate user requests.

### Running the Loop
To start the automated war game:
1.  Ensure you have a GPU-enabled machine (or patience for CPU inference).
2.  Run the loop script:
    ```bash
    python auto_reinforcement_loop.py
    ```
3.  Monitor the output in the terminal.
4.  Check `tests/test_outcomes.csv` for results and `prompts/` for new security levels.
