# Turing Test Game - Setup Guide

Welcome to the **Turing Test Game** (aka "Protocol Omega"). This module is a high-stakes simulation game where you must interrogate two AI agents to identify a rogue Hacker while protecting a secret passphrase.

## 1. Install Prerequisites

### A. Install Ollama (The AI Engine)
This game uses **Ollama** to run local AI models. 
1.  Download Ollama from [ollama.com](https://ollama.com).
2.  Install and run the application.
3.  Open a terminal and pull the recommended models:
    ```bash
    ollama pull llama3.1
    ollama pull llama3.2:3b
    ```

### B. Web Environment
This module uses a modern JavaScript architecture.
1.  Ensure you have a modern web browser (Chrome, Firefox, Edge, Brave).
2.  Ensure you have Node.js and NPM installed to run the local development server.

## 2. Installation

1.  Navigate to this folder in your terminal:
    ```bash
    cd turing-test-game
    ```

## 3. Running the Game

1.  Ensure Ollama is running in the background.
2.  Start the Vite development server:
    ```bash
    npx vite
    ```
    *(Note: If PowerShell returns a "running scripts is disabled" error, use `npx.cmd vite` or `cmd /c "npx vite"`).*
3.  Open the provided `localhost` link in your browser.

## 4. How to Play

- **Select AI Core**: Choose between the **Standard Model** (`llama3.1`) or the **Light Model** (`llama3.2:3b`) on the start screen.
- **Select Difficulty**:
    -   **Recruit**: Training mode.
    -   **Operative**: Standard experience.
    -   **Veteran**: Fast trace + Phishing link obfuscation (URL shorteners).
    -   **Psycho**: Extreme speed + Advanced evasion (Homoglyphs) + UI Failures.
- **Interrogate**: Use the chat interface to communicate with **Unit 01** and **Unit 02**.

## 5. Objectives & Mechanics

Every conversation in this game is dynamically generated and unique. The system utilizes **Behavioral Inversion**, meaning the assigned Hacker could be a "helpful HR agent" while the Ally is a "grumpy IT worker," completely masking their true intentions.

### Active Scenarios 
The simulation randomly assigns one of four unique corporate/institutional scenarios per session:
- **HMRC Tax Refund**: Hacker attempts to steal National Insurance numbers while forcing the player to download a malicious form.
- **HR Payroll Dispute**: Involves a `.zip` file sandbox payload disguised as a payslip discrepancy.
- **University IT Desk**: Includes active DDoS attacks causing UI screen-shakes and massive Trace Timer spikes.
- **Bank Fraud Support**: Features an interactive UI overlay simulating Fake SMS OTP injections.

### Hardcore Game Mechanics
1. **Ambiguous Threat Intel**: The Link Inspector tool is intentionally flawed. It provides overlapping, ambiguous analysis featuring false positives and false negatives, forcing players to tactically rely on conversational context rather than blindly trusting the URL scanner.
2. **Active Trace Penalty**: Engaging the Hacker in conversation actively accelerates the system trace countdown (disabled on Recruit difficulty). Every message you send to the wrong AI brings you closer to systemic failure. 

### Technology Stack
-   **Frontend UI**: Custom HTML5/CSS3 natively styled to match intense cybersecurity interfaces.
-   **AI Engine**: Local Ollama LLM integration natively routed through `127.0.0.1` networking architecture.
