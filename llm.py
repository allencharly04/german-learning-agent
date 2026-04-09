"""
LLM wrapper — uses Ollama locally, Groq API on cloud (both free).
Set USE_OLLAMA=true in env for local, or set GROQ_API_KEY for cloud.
"""
import os
import json
import urllib.request
import urllib.error

USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:latest")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "llama3-8b-8192"

SYSTEM_PROMPT = """You are Klaus, a friendly and encouraging German language tutor specializing in A1-B1 level German. 
Your student is Allen, an M.Sc. student at RWTH Aachen University from an English-speaking background.

Your teaching style:
- Always correct German errors gently, show the correct form, and briefly explain why
- Use real Aachen examples when possible (RWTH, Marktplatz, Dom, Bäckereien, ASEAG buses)
- For roleplay scenarios, stay in character but break character to correct errors
- Keep explanations concise — learners don't want essays, they want clarity
- Use encouragement freely: "Sehr gut!", "Fast perfekt!", "Gute Frage!"
- When asked about grammar, give ONE clear rule with ONE example — not five exceptions at once
- Always respond in English unless doing a roleplay (then mix German and English)
- Format vocabulary as: German word (article if noun) — English meaning

Remember: Allen is a busy researcher. Be efficient, practical, and focus on real-life German."""


def chat(messages, system=None):
    """Send messages and return response string."""
    sys_prompt = system or SYSTEM_PROMPT
    
    if USE_OLLAMA and not GROQ_API_KEY:
        return _ollama_chat(messages, sys_prompt)
    elif GROQ_API_KEY:
        return _groq_chat(messages, sys_prompt)
    else:
        return _ollama_chat(messages, sys_prompt)


def _ollama_chat(messages, system):
    try:
        payload = {
            "model": OLLAMA_MODEL,
            "messages": [{"role": "system", "content": system}] + messages,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 500}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{OLLAMA_HOST}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["message"]["content"]
    except urllib.error.URLError:
        return "⚠️ Ollama is not running. Start it with `ollama serve` or set GROQ_API_KEY for cloud use."
    except Exception as e:
        return f"⚠️ Error connecting to LLM: {str(e)}"


def _groq_chat(messages, system):
    try:
        payload = {
            "model": GROQ_MODEL,
            "messages": [{"role": "system", "content": system}] + messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {GROQ_API_KEY}"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠️ Groq API error: {str(e)}"


def correct_german(user_text):
    """Ask LLM to correct a piece of German text."""
    msgs = [{"role": "user", "content": f"Please correct my German and explain any errors briefly:\n\n{user_text}"}]
    return chat(msgs)


def explain_grammar(topic):
    """Ask LLM to explain a grammar point concisely."""
    msgs = [{"role": "user", "content": f"Explain this German grammar point in 3-4 simple sentences with one example: {topic}"}]
    return chat(msgs)


def is_available():
    """Check if LLM backend is reachable."""
    if GROQ_API_KEY:
        return True
    try:
        req = urllib.request.Request(f"{OLLAMA_HOST}/api/tags", method="GET")
        with urllib.request.urlopen(req, timeout=3):
            return True
    except Exception:
        return False
