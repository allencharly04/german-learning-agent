# 🇩🇪 German Learning Agent

A personal German tutor app built with Streamlit + SQLite + Ollama.
Built for Allen — RWTH Aachen M.Sc. student, starting from A1.

## Features
- **10 structured A1 lessons** (articles, verbs, numbers, transport, shopping, etc.)
- **SRS flashcard system** (SM-2 algorithm — same as Anki)
- **Story reader** — Grimm fairy tales (A1) + DW slow news (A2-B1)
- **6 Aachen roleplay scenarios** — bakery, bus, supermarket, Bürgeramt, restaurant, doctor
- **AI tutor (Klaus)** — powered by Ollama locally or Groq API on cloud
- **Progress dashboard** — streak, mastery chart, session history

## Quick Start (Local)

```bash
# 1. Clone / navigate to the folder
cd german-agent

# 2. Create conda environment
conda create -n german-agent python=3.11
conda activate german-agent

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start Ollama (for AI tutor)
ollama serve
ollama pull llama3.1   # first time only

# 5. Run
streamlit run app.py
```

Open: http://localhost:8501

## Deploy to Render (Free)

1. Push to GitHub: `git init && git add . && git push`
2. Go to render.com → New Web Service
3. Connect your GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Add environment variable: `GROQ_API_KEY=your_key_here` (get free key at console.groq.com)
7. Deploy!

## Deploy to Streamlit Cloud (Free)

1. Push to GitHub
2. Go to share.streamlit.io
3. Connect repo, set `app.py` as entry point
4. Add secret: `GROQ_API_KEY = "your_key_here"`
5. Deploy!

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_OLLAMA` | `true` | Use Ollama locally (set to `false` on cloud) |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `OLLAMA_MODEL` | `llama3.1:latest` | Model to use |
| `GROQ_API_KEY` | `` | Groq API key (free at console.groq.com) |

## Project Structure

```
german-agent/
├── app.py           # Main Streamlit app (all pages)
├── db.py            # SQLite database + SRS logic
├── curriculum.py    # A1 lesson content (10 lessons)
├── llm.py           # Ollama/Groq wrapper
├── scenarios.py     # Aachen roleplay scenarios
├── story_reader.py  # Grimm stories + DW news
├── requirements.txt
└── data/
    └── german.db    # Created automatically on first run
```

## Lesson Curriculum (A1)

1. Greetings & Introductions
2. Articles: der, die, das
3. Numbers 1–100
4. Present tense: sein & haben
5. Food & Ordering (Aachen Bäckerei)
6. Days, Months & Time
7. Getting Around Aachen
8. Family & People
9. Shopping & Supermarket
10. University & Modal Verbs

## Adding More Lessons

Edit `curriculum.py` and add entries to the `LESSONS` list.
Each lesson needs: `id`, `topic`, `grammar`, `explanation`, `vocabulary`, `quiz`.
