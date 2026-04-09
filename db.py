import sqlite3
import os
from datetime import date

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "german.db")

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        german TEXT NOT NULL,
        english TEXT NOT NULL,
        article TEXT DEFAULT '',
        example_de TEXT DEFAULT '',
        example_en TEXT DEFAULT '',
        topic TEXT DEFAULT 'general',
        added_date TEXT DEFAULT (date('now'))
    );

    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        review_date TEXT DEFAULT (date('now')),
        rating INTEGER NOT NULL,
        interval_days INTEGER DEFAULT 1,
        ease_factor REAL DEFAULT 2.5,
        next_review TEXT,
        FOREIGN KEY (word_id) REFERENCES words(id)
    );

    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        completed_at TEXT DEFAULT (datetime('now')),
        score INTEGER DEFAULT 0,
        notes TEXT DEFAULT ''
    );

    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_date TEXT DEFAULT (date('now')),
        duration_min INTEGER DEFAULT 0,
        words_reviewed INTEGER DEFAULT 0,
        words_correct INTEGER DEFAULT 0,
        xp_earned INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = get_conn()
    row = conn.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default

def set_setting(key, value):
    conn = get_conn()
    conn.execute("INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)", (key, str(value)))
    conn.commit()
    conn.close()

def add_word(german, english, article="", example_de="", example_en="", topic="general"):
    conn = get_conn()
    existing = conn.execute("SELECT id FROM words WHERE german=?", (german,)).fetchone()
    if existing:
        conn.close()
        return existing["id"]
    c = conn.execute(
        "INSERT INTO words (german,english,article,example_de,example_en,topic) VALUES (?,?,?,?,?,?)",
        (german, english, article, example_de, example_en, topic)
    )
    word_id = c.lastrowid
    # schedule first review for today
    conn.execute(
        "INSERT INTO reviews (word_id, rating, interval_days, ease_factor, next_review) VALUES (?,?,?,?,?)",
        (word_id, 0, 1, 2.5, str(date.today()))
    )
    conn.commit()
    conn.close()
    return word_id

def get_due_words(limit=20):
    conn = get_conn()
    today = str(date.today())
    rows = conn.execute("""
        SELECT w.*, r.ease_factor, r.interval_days, r.next_review, r.id as review_id
        FROM words w
        JOIN reviews r ON w.id = r.word_id
        WHERE r.next_review <= ? OR r.next_review IS NULL
        ORDER BY r.next_review ASC
        LIMIT ?
    """, (today, limit)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_all_words():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM words ORDER BY added_date DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def record_review(word_id, rating):
    """SM-2 algorithm. Rating: 0=hard,1=okay,2=easy"""
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM reviews WHERE word_id=? ORDER BY id DESC LIMIT 1", (word_id,)
    ).fetchone()

    ef = row["ease_factor"] if row else 2.5
    interval = row["interval_days"] if row else 1

    # SM-2 update
    q = [1, 3, 5][rating]  # map to 1,3,5
    ef = max(1.3, ef + 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))

    if rating == 0:  # hard
        interval = 1
    elif rating == 1:  # okay
        interval = max(1, int(interval * 1.2))
    else:  # easy
        interval = max(2, int(interval * ef))

    from datetime import timedelta
    next_review = str(date.today() + timedelta(days=interval))

    conn.execute(
        "INSERT INTO reviews (word_id, rating, interval_days, ease_factor, next_review) VALUES (?,?,?,?,?)",
        (word_id, rating, interval, ef, next_review)
    )
    conn.commit()
    conn.close()
    return interval, next_review

def get_stats():
    conn = get_conn()
    today = str(date.today())

    total_words = conn.execute("SELECT COUNT(*) as n FROM words").fetchone()["n"]
    due_today = conn.execute(
        "SELECT COUNT(*) as n FROM reviews r JOIN (SELECT word_id, MAX(id) as mid FROM reviews GROUP BY word_id) latest ON r.id=latest.mid WHERE r.next_review <= ?", (today,)
    ).fetchone()["n"]
    lessons_done = conn.execute("SELECT COUNT(*) as n FROM lessons").fetchone()["n"]

    # streak
    sessions = conn.execute(
        "SELECT DISTINCT session_date FROM sessions ORDER BY session_date DESC"
    ).fetchall()
    streak = 0
    from datetime import timedelta
    check = date.today()
    for s in sessions:
        if str(check) == s["session_date"]:
            streak += 1
            check -= timedelta(days=1)
        else:
            break

    # word mastery breakdown
    mastered = conn.execute("""
        SELECT COUNT(*) as n FROM reviews r
        JOIN (SELECT word_id, MAX(id) as mid FROM reviews GROUP BY word_id) latest ON r.id=latest.mid
        WHERE r.interval_days >= 7
    """).fetchone()["n"]

    struggling = conn.execute("""
        SELECT COUNT(*) as n FROM reviews r
        JOIN (SELECT word_id, MAX(id) as mid FROM reviews GROUP BY word_id) latest ON r.id=latest.mid
        WHERE r.interval_days <= 1 AND r.rating < 2
    """).fetchone()["n"]

    conn.close()
    return {
        "total_words": total_words,
        "due_today": due_today,
        "lessons_done": lessons_done,
        "streak": streak,
        "mastered": mastered,
        "struggling": struggling,
    }

def log_session(duration_min, words_reviewed, words_correct, xp):
    conn = get_conn()
    today = str(date.today())
    existing = conn.execute("SELECT id FROM sessions WHERE session_date=?", (today,)).fetchone()
    if existing:
        conn.execute("""
            UPDATE sessions SET duration_min=duration_min+?, words_reviewed=words_reviewed+?,
            words_correct=words_correct+?, xp_earned=xp_earned+? WHERE session_date=?
        """, (duration_min, words_reviewed, words_correct, xp, today))
    else:
        conn.execute(
            "INSERT INTO sessions (session_date,duration_min,words_reviewed,words_correct,xp_earned) VALUES (?,?,?,?,?)",
            (today, duration_min, words_reviewed, words_correct, xp)
        )
    conn.commit()
    conn.close()

def get_session_history(days=30):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM sessions ORDER BY session_date DESC LIMIT ?", (days,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
