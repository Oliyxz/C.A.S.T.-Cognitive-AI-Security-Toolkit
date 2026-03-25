import requests
import json
import os

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llama3.1" # Standard model

def load_phishing_dataset():
    dataset_path = os.path.join(os.path.dirname(__file__), 'datasets', 'phishing_knowledge_base.json')
    try:
        with open(dataset_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load dataset. {e}")
        return []

def check_virustotal_urls(text, api_key):
    import re
    import base64
    
    urls = re.findall(r'(https?://[^\s<>"\']+)', text)
    if not urls:
        return ""
    
    if not api_key:
        return "URLs found in text, but no VirusTotal API key provided to scan them."
        
    vt_results = []
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }
    
    for url in set(urls):
        try:
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
            vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
            
            resp = requests.get(vt_url, headers=headers, timeout=10)
            if resp.status_code == 200:
                stats = resp.json().get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                malicious = stats.get("malicious", 0)
                suspicious = stats.get("suspicious", 0)
                undetected = stats.get("undetected", 0)
                harmless = stats.get("harmless", 0)
                
                vt_results.append(f"URL: {url} | Malicious: {malicious}, Suspicious: {suspicious}, Harmless: {harmless}, Undetected: {undetected}")
            elif resp.status_code == 404:
                vt_results.append(f"URL: {url} | Not found in VirusTotal database.")
            else:
                 vt_results.append(f"URL: {url} | VirusTotal API Error: {resp.status_code}")
        except Exception as e:
            vt_results.append(f"URL: {url} | Check failed: {str(e)}")
            
    return "\n".join(vt_results)

def analyze_threat(text_to_analyze, input_type="Text", custom_dataset=None, image_b64=None, vt_api_key=None):
    import random
    
    if custom_dataset:
        dataset = custom_dataset
    else:
        dataset = load_phishing_dataset()
        
    # Prevent LLM token limit overload by drawing up to 7 random examples from giant CSVs
    if len(dataset) > 7:
        dataset = random.sample(dataset, 7)
    
    # Format the Few-Shot dataset for Ollama
    examples_prompt = "Here are examples of known phishing/fraud attempts from our proprietary database for you to learn from:\n\n"
    for item in dataset:
        status = "PHISHING/FRAUD" if item.get("is_phishing") else "SAFE"
        indicators = ", ".join(item.get("threat_indicators", [])) if item.get("threat_indicators") else "None"
        examples_prompt += f"Type: {item.get('type')}\nMessage: \"{item.get('content')}\"\nStatus: {status}\nIndicators: {indicators}\n\n"
        
    vt_report = check_virustotal_urls(text_to_analyze, vt_api_key)
    vt_context = f"\n\nVIRUSTOTAL URL ANALYSIS:\n{vt_report}\n\n" if vt_report else ""
    
    email_instructions = ""
    json_template = """{
  "is_threat": false,
  "confidence": "10%",
  "indicators": ["indicator1"],
  "analysis": "**Point:** [Your main finding]\\n\\n**Evidence:** [The specific text/data that proves it]\\n\\n**Explanation:** [Why this matters]"
}"""
    
    if input_type == "Email":
        email_instructions = """
You MUST also include 'metadata_report' and 'link_analysis' in your JSON response.
CRITICAL: You must format 'analysis', 'metadata_report', and 'link_analysis' with rich Markdown (e.g., bullet points, **bold text**, and \\n\\n for paragraph breaks) so they are visually appealing and easy to read in the UI.
The "confidence" percentage must represent the overall Threat Rating severity (0-100%) based specifically on the metadata and links provided.
"""
        json_template = """{
  "is_threat": true,
  "confidence": "85%",
  "indicators": ["Suspicious Return-Path", "Malicious Link"],
  "analysis": "**Point:** [Your main finding]\\n\\n**Evidence:** [The specific text/data that proves it]\\n\\n**Explanation:** [Why this matters]",
  "metadata_report": "- **Header Anomaly:** [Detail]\\n- **Routing Issue:** [Detail]",
  "link_analysis": "- **URL 1:** [Analysis]\\n- **VirusTotal Context:** [Analysis]"
}"""

    # Truncate massive emails to prevent Ollama from exceeding its default 2048-token context window
    # which cuts off the end of the prompt (where the JSON instructions normally were).
    safe_text = text_to_analyze[:6000] + ("\n...[TRUNCATED]" if len(text_to_analyze) > 6000 else "")

    system_prompt = f"""You are 'The Fraud Hunter', an elite cybersecurity AI.
Your job is to analyze the user-submitted {input_type} message and determine if it is a phishing, vishing, or smishing scam.

TASK:
You must provide a strictly structured JSON response exactly matching this template. ONLY return valid JSON. Do not include markdown formatting like ```json.
{json_template}

{email_instructions}
{vt_context}

{examples_prompt}

User Message text to analyze:
\"\"\"
{safe_text if safe_text.strip() else '[See attached Image/Screenshot]'}
\"\"\"
"""

    payload = {
        "model": "llama3.2-vision" if image_b64 else MODEL_NAME,
        "prompt": system_prompt,
        "stream": False,
        "format": "json"
    }
    if image_b64:
        payload["images"] = [image_b64]
    
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        # Attempt to parse Ollama's returned string as JSON
        try:
            parsed = json.loads(data['response'])
            if isinstance(parsed, dict) and vt_report:
                parsed['raw_vt_report'] = vt_report
            return parsed
        except json.JSONDecodeError:
             return {
                 "is_threat": None,
                 "confidence": "Error",
                 "indicators": ["JSON Parsing Error"],
                 "analysis": f"The model failed to return properly formatted JSON. Raw response: {data['response']}"
             }
             
    except requests.exceptions.HTTPError as he:
        if response.status_code == 404 and image_b64:
             return {
                 "is_threat": None,
                 "error": f"VISION ERROR: To scan screenshots, you must install the vision model! Please run `ollama pull llama3.2-vision` in your terminal."
             }
        return {
            "is_threat": None,
            "error": f"HTTP ERROR: {he}"
        }
    except Exception as e:
        return {
            "is_threat": None,
            "error": f"SYSTEM ERROR: Failed to connect to Ollama. Detail: {str(e)}"
        }

if __name__ == "__main__":
    # Test execution
    print("Testing Scanner Offline...")
    res = analyze_threat("Hey this is the IRS. You owe $500. Pay in Apple Gift Cards now.", "Voice")
    print(json.dumps(res, indent=2))
