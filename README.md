# C.A.S.T. (Cognitive AI Security Toolkit)

**A multi-module cybersecurity defense suite designed to demonstrate and detect modern social engineering attacks.**

![Project Status](https://img.shields.io/badge/Status-In%20Development-yellow)
![Language](https://img.shields.io/badge/Languages-Python%20%7C%20C%2B%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%205%20%7C%20Windows%20%7C%20Linux-green)

## 1. Project Overview
The **Social Engineering AI Toolkit** is a research and defense project developed by the **BCU Cyber Security Society**. It moves beyond traditional network security to address the "Human Element" of cybersecurity.

The toolkit features two distinct modules that operate in parallel to detect, simulate, and analyze social engineering threats:
1.  **AI Vulnerability Lab:** A demonstration of LLM Prompt Injection and "Jailbreaking."
2.  **Communication Threat Scanner:** A tool to analyze and flag phishing across Email, SMS, and Voice.

## 2. Architecture & Modules

### Module 1: The GenAI Vulnerability Lab (Chatbot)
* **Focus:** AI Safety, Prompt Injection, & Social Engineering Games.
* **Tech Stack:** Python, Streamlit, HTML/JS, OpenAI API & Local Ollama LLMs.
* **Functionality:**
    * **The "Glass Box" Bot:** A corporate chatbot containing hidden "Secret Data" (e.g., fake salaries) that users must try to extract via prompt engineering.
    * **The Turing Test Game:** A competitive cybersecurity simulation where users must deduce the identity of the "Hacker" AI versus the "Ally" AI.
        * Includes extreme mechanics like **Behavioral Inversion** (randomized personalities), **Active Trace Penalties**, and **Ambiguous Threat Intel** URL scanners.
        * **Nightmare Mechanics:** Features aggressive live-threat injections such as **Active DDoS Attacks** (requiring the player to input `\FLUSH_DNS` overrides), **MitM Signal Interception** where the Hacker masks its identity, and **Intelligent System Message Spoofing**.
        * **AI Benchmarking:** Supports an **API-Key Multi-Provider Mode** allowing you to pull models directly from **Google Gemini, OpenAI, and Anthropic Claude**, alongside local **Ollama** models. Upon mission completion, automatically outputs a telemetry "Turing Score" report analyzing generation speed, deception success, and prompt integrity.

### Module 2: The Fraud Hunter (Threat Scanner)
* **Focus:** Phishing, Vishing, & Smishing Detection.
* **Tech Stack:** Python, OpenAI API, SpeechRecognition.
* **Functionality:**
    * **Text Scanner:** Analyzes Emails and SMS for urgency patterns and suspicious links, outputting beautifully structured, strictly formatted **Markdown AI Reports** within Streamlit UI callout boxes.
    * **Voice Scanner:** Transcribes `.mp3` / `.wav` audio files to detect "Vishing" scripts.
    * **Modular AI Datasets:** Utilizes Free-Shot prompting against customizable `.json` threat intelligence databases to massively boost local detection accuracy.

## 3. Future Roadmap: The Biometric Gatekeeper (Hardware)
While the core web and AI scanner modules are fully operational, the toolkit is designed to eventually integrate with a physical endpoint defense system. Due to time constraints, this hardware module is currently in active development.

* **Focus:** Physical Security & Impersonation Detection.
* **Upcoming Hardware Requirements:** Raspberry Pi 4/5, 1x USB Webcam.
* **Planned Functionality:**
    * Capture dual video streams (Live Face + ID Card).
    * Use C++ and OpenCV to compare facial embeddings.
    * Calculate a "Match Confidence %" to validate physical identity before granting network access.

## 4. Installation & Setup

### Prerequisites
1.  **Git:** `sudo apt install git`
2.  **Python 3.10+:** Pre-installed on most systems.
3.  **C++ Compiler:** `sudo apt install build-essential cmake`
4.  **AI Services:** An **OpenAI API Key** (for Modules B and C) and **Ollama** installed locally (for the Turing Test feature in Module B).

### Base Installation
```bash
git clone https://github.com/Oliyxz/Social-Engineering-Toolkit.git
cd Social-Engineering-Toolkit
```
*(Please see the individual README files inside each module's folder for specific execution instructions).*
