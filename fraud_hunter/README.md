# Module C: The Fraud Hunter

Welcome to **The Fraud Hunter**, a multi-modal threat scanner designed to analyze suspicious Emails, SMS messages, URLs, and Voicemails. This module uses local AI models to detect phishing attempts, social engineering tactics, and malicious links.

## 1. Install Prerequisites

### A. Install Ollama (The AI Engine)
This module uses **Ollama** to run the local language models for text analysis. 
1.  Download Ollama from [ollama.com](https://ollama.com).
2.  Install and run the application.
3.  Open a terminal and pull the recommended model:
    ```bash
    ollama pull llama3.1
    ```

### B. Python Environment
This module is built using Python and Streamlit.
1. Ensure you have Python 3.8+ installed on your system.
2. Navigate to this folder in your terminal:
   ```bash
   cd fraud_hunter
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: The requirements include `streamlit` for the UI, `requests` for API calls, and `openai-whisper` for local voicemail transcription).*

## 2. Running the Module

1.  Ensure Ollama is running in the background.
2.  Start the Streamlit application:
    ```bash
    python -m streamlit run app.py
    ```
    *(Note: If `streamlit run app.py` directly does not work on your system, the `python -m` method ensures it runs via your installed Python module).*
3.  The application will automatically open in your default web browser (usually at `http://localhost:8501`).

## 3. Features & How to Use

- **Text & Link Scanner**: Paste suspicious SMS messages, full raw Email sources (including headers), or URLs. You can also upload image screenshots of messages for OCR and analysis. 
- **Voice Mail Scanner**: Upload `.wav`, `.mp3`, `.m4a`, or `.flac` audio files. The application will securely transcribe the audio entirely locally using Whisper and then analyze it for Voice Phishing (Vishing) patterns.
- **VirusTotal Integration**: Enter a free VirusTotal API key in the sidebar to enable live threat intelligence scanning for URLs and extracted domains. The app will verify the key and fetch raw intelligence reports.
- **Threat Indicator Scoring & UI**: The AI provides a percentage-based Threat Confidence score and extracts specific red flags. **AI Analysis Reports** are strictly formatted using rich Markdown (bolding, spacing) and seamlessly rendered within immersive, color-coded Streamlit UI callout boxes (🚨 Red/Yellow for Threats, ✅ Green/Blue for Safe).

## 4. Modular AI Datasets

The Fraud Hunter uses local JSON datasets for "Few-Shot Prompting," which grounds the AI against known real-world threats to drastically increase detection accuracy.
- Place your custom JSON reference datasets inside the `datasets/` folder.
- The system rigidly expects exactly: `sms_dataset.json`, `email_dataset.json`, `url_dataset.json`, and `voice_dataset.json`. If missing or empty, it natively defaults to `phishing_knowledge_base.json`.
- The dataset loader features strict-bypass parsing (`strict=False`), meaning it gracefully handles third-party datasets containing unescaped control characters or massive multibyte layouts.
- The sidebar UI will automatically display the number of successfully loaded reference points for each modality on startup.
