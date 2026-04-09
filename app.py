import streamlit as st
import time
import random
from datetime import date, datetime
import plotly.graph_objects as go
import plotly.express as px

import db
import llm
import curriculum
import camera_vision
import scenarios
import story_reader

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deutsch Lernen — Allen's German Agent",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 { font-family: 'DM Serif Display', serif; }

.main { background: #0f0f13; }
.stApp { background: #0f0f13; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #16161d;
    border-right: 1px solid #2a2a3a;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: #1a1a24;
    border: 1px solid #2a2a3a;
    border-radius: 12px;
    padding: 16px;
}

/* Flashcard styles */
.flashcard {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border: 1px solid #3a3a5c;
    border-radius: 20px;
    padding: 50px 40px;
    text-align: center;
    min-height: 200px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.german-word {
    font-family: 'DM Serif Display', serif;
    font-size: 2.8rem;
    color: #e8d5b7;
    margin-bottom: 8px;
}
.article-badge {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 16px;
}
.der { background: #1e3a5f; color: #7eb8f7; }
.die { background: #3d1a2e; color: #f78bc0; }
.das { background: #1a3d1a; color: #7ef7a0; }
.example-text {
    font-style: italic;
    color: #8888aa;
    font-size: 1.0rem;
    max-width: 500px;
}

/* Chat messages */
.chat-user {
    background: #1e2d4a;
    border-left: 3px solid #5b8dd9;
    padding: 12px 16px;
    border-radius: 0 12px 12px 0;
    margin: 8px 0;
    color: #c8d8f0;
}
.chat-tutor {
    background: #1e3020;
    border-left: 3px solid #5b9e6a;
    padding: 12px 16px;
    border-radius: 0 12px 12px 0;
    margin: 8px 0;
    color: #c0e0c8;
}

/* Story text */
.story-text {
    font-family: 'DM Serif Display', serif;
    font-size: 1.15rem;
    line-height: 2.0;
    color: #d0c8b8;
    background: #13131b;
    padding: 32px;
    border-radius: 16px;
    border: 1px solid #2a2a3a;
}
.story-word {
    cursor: pointer;
    border-bottom: 1px dashed #5a5a7a;
    color: #d0c8b8;
}

/* Lesson content */
.lesson-box {
    background: #13131b;
    border: 1px solid #2a2a3a;
    border-radius: 16px;
    padding: 28px;
}

/* Quiz options */
.stButton button {
    width: 100%;
    text-align: left;
    background: #1a1a24;
    border: 1px solid #2a2a3a;
    color: #c0c0d8;
    border-radius: 10px;
    padding: 12px 20px;
    transition: all 0.2s;
}
.stButton button:hover {
    background: #22223a;
    border-color: #5b8dd9;
    color: #e0e0f8;
}

/* Progress bar */
.streak-fire { font-size: 2rem; }

/* XP bar */
.xp-bar-bg {
    background: #2a2a3a;
    border-radius: 10px;
    height: 8px;
    margin: 4px 0;
}
.xp-bar-fill {
    background: linear-gradient(90deg, #5b8dd9, #9b59b6);
    border-radius: 10px;
    height: 8px;
    transition: width 0.5s;
}

/* Nav pills */
.nav-pill {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.85rem;
    background: #22223a;
    color: #8888aa;
    margin: 2px;
}

/* Correct/wrong colors */
.correct { color: #5b9e6a; font-weight: 600; }
.wrong { color: #c0504d; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# ── Init ───────────────────────────────────────────────────────────────────────
db.init_db()

# Seed starter vocabulary if empty
if db.get_setting("vocab_seeded") != "true":
    for w in curriculum.STARTER_VOCABULARY:
        db.add_word(w["german"], w["english"], w.get("article",""), w.get("example_de",""), w.get("example_en",""), w.get("topic","general"))
    db.set_setting("vocab_seeded", "true")

# Session state defaults
for key, val in [
    ("page", "home"),
    ("fc_words", []),
    ("fc_idx", 0),
    ("fc_revealed", False),
    ("fc_session_correct", 0),
    ("fc_session_total", 0),
    ("chat_messages", []),
    ("current_scenario", None),
    ("quiz_idx", 0),
    ("quiz_score", 0),
    ("quiz_done", False),
    ("quiz_answered", False),
    ("quiz_selected", None),
    ("lesson_id", 1),
    ("session_start", time.time()),
    ("story_id", None),
    ("tutor_messages", []),
]:
    if key not in st.session_state:
        st.session_state[key] = val

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇩🇪 Deutsch Lernen")
    st.markdown("*Dein persönlicher Deutschlehrer*")
    st.divider()

    stats = db.get_stats()
    streak = stats["streak"]
    fire = "🔥" * min(streak, 5) if streak > 0 else "❄️"
    st.markdown(f"**Streak:** {fire} {streak} {'day' if streak==1 else 'days'}")
    st.markdown(f"**Words learned:** {stats['total_words']}")
    st.markdown(f"**Due for review:** {stats['due_today']}")
    st.markdown(f"**Lessons done:** {stats['lessons_done']}")
    st.divider()

    pages = {
        "🏠  Home": "home",
        "📖  Today's Lesson": "lesson",
        "🃏  Flashcards (SRS)": "flashcards",
        "📚  Story Reader": "stories",
        "🎭  Roleplay": "roleplay",
        "💬  AI Tutor": "tutor",
        "📷  Camera Vision": "camera",
        "🎙️  Audio Translator": "audio",
        "📊  Progress": "progress",
    }
    for label, page_id in pages.items():
        active = "→ " if st.session_state.page == page_id else "   "
        if st.button(f"{active}{label}", key=f"nav_{page_id}", use_container_width=True):
            st.session_state.page = page_id
            st.rerun()

    st.divider()
    llm_ok = llm.is_available()
    st.markdown(f"**AI Tutor:** {'🟢 Online' if llm_ok else '🔴 Offline'}")
    if not llm_ok:
        st.caption("Start Ollama or set GROQ_API_KEY")

# ── Page: Home ─────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    st.markdown("# Willkommen zurück, Allen! 👋")
    st.markdown(f"*{datetime.now().strftime('%A, %d %B %Y')}*")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔥 Streak", f"{stats['streak']} days")
    with col2:
        st.metric("📝 Words", stats['total_words'])
    with col3:
        st.metric("🃏 Due Today", stats['due_today'])
    with col4:
        st.metric("✅ Mastered", stats['mastered'])

    st.divider()
    st.markdown("### Your 60-minute session today")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Recommended order:**")
        steps = [
            ("5 min", "🔥 Warm-up", "Review yesterday's hardest words", "flashcards"),
            ("20 min", "📖 Lesson", f"Lesson {db.get_setting('current_lesson', '1')}: structured grammar + vocab", "lesson"),
            ("15 min", "📚 Story", "Read a graded German text", "stories"),
            ("10 min", "🎭 Roleplay", "Practice a real Aachen scenario", "roleplay"),
            ("10 min", "🃏 Flashcards", "SRS review session", "flashcards"),
        ]
        for time_est, title, desc, target in steps:
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{title}** `{time_est}`\n\n{desc}")
                with c2:
                    if st.button("Start", key=f"home_{target}_{title}"):
                        st.session_state.page = target
                        st.rerun()
                st.divider()

    with col_b:
        st.markdown("**Daily German tip:**")
        tips = [
            "🎯 In German, the verb ALWAYS goes in position 2 in a statement — even after a time phrase. 'Heute **gehe** ich in die Mensa.'",
            "🎯 Always learn nouns with their article: not just 'Hund' but 'der Hund'. Articles are non-negotiable in German.",
            "🎯 'halb vier' = 3:30, not 4:30! Germans say 'half [of] four' meaning halfway to four.",
            "🎯 'Sie' (capital S) = formal 'you'. 'sie' (lowercase) = she or they. Context and verb form help tell them apart.",
            "🎯 German adjectives change endings depending on gender: ein alt**er** Mann, eine alt**e** Frau, ein alt**es** Kind.",
            "🎯 Umlauts matter: 'schon' = already, 'schön' = beautiful. They're completely different words!",
            "🎯 Germans say 'Ich habe Hunger' (I have hunger) not 'Ich bin hungrig'. Same for 'Ich habe Durst' (I'm thirsty).",
        ]
        st.info(random.choice(tips))

        st.markdown("**Quick vocabulary test:**")
        if stats['total_words'] > 0:
            due = db.get_due_words(limit=3)
            if due:
                st.markdown("Can you remember these words?")
                for w in due:
                    art = f"({w['article']}) " if w['article'] else ""
                    with st.expander(f"{art}{w['german']}"):
                        st.markdown(f"**{w['english']}**")
                        if w.get('example_de'):
                            st.caption(f"*{w['example_de']}*")
            else:
                st.success("All caught up! No words due right now. 🎉")


# ── Page: Lesson ───────────────────────────────────────────────────────────────
elif st.session_state.page == "lesson":
    lesson_id = int(db.get_setting("current_lesson", "1"))
    lesson = curriculum.get_lesson(lesson_id)

    if not lesson:
        st.error("All lessons completed! You're ready for B1. 🏆")
        st.stop()

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"# Lesson {lesson['id']}: {lesson['topic']}")
        st.caption(f"Grammar focus: *{lesson['grammar']}*")
    with col2:
        st.markdown(f"**{lesson_id} / {curriculum.get_total_lessons()}** lessons")
        prog = lesson_id / curriculum.get_total_lessons()
        st.progress(prog)

    tab1, tab2, tab3 = st.tabs(["📖 Explanation", "📝 Vocabulary", "❓ Quiz"])

    with tab1:
        st.markdown('<div class="lesson-box">', unsafe_allow_html=True)
        st.markdown(lesson["explanation"])
        st.markdown('</div>', unsafe_allow_html=True)

        # Add vocab to SRS deck
        if st.button("➕ Add all vocabulary to my SRS deck", type="primary"):
            count = 0
            for w in lesson["vocabulary"]:
                wid = db.add_word(
                    w["german"], w["english"], w.get("article",""),
                    w.get("example_de",""), w.get("example_en",""), lesson["topic"]
                )
                count += 1
            st.success(f"✅ Added {count} words from this lesson to your flashcard deck!")

    with tab2:
        st.markdown("### Vocabulary for this lesson")
        st.caption("Click 'Add to deck' on any word to add it to your SRS flashcards.")
        for w in lesson["vocabulary"]:
            with st.container():
                c1, c2, c3 = st.columns([2, 3, 1])
                with c1:
                    art = w.get("article", "")
                    art_col = {"der": "🔵", "die": "🔴", "das": "🟢"}.get(art, "⚪")
                    st.markdown(f"**{art_col} {art} {w['german']}**" if art else f"**{w['german']}**")
                with c2:
                    st.markdown(w["english"])
                    if w.get("example_de"):
                        st.caption(f"*{w['example_de']}*")
                with c3:
                    if st.button("Add", key=f"add_{w['german']}"):
                        db.add_word(w["german"], w["english"], w.get("article",""),
                                   w.get("example_de",""), w.get("example_en",""), lesson["topic"])
                        st.toast(f"Added: {w['german']}")
                st.divider()

    with tab3:
        st.markdown("### Quiz")
        quiz = lesson["quiz"]

        if st.session_state.quiz_done:
            score = st.session_state.quiz_score
            total = len(quiz)
            pct = int(score/total*100)
            if pct == 100:
                st.balloons()
                st.success(f"🏆 Perfect score! {score}/{total} — Ausgezeichnet!")
            elif pct >= 75:
                st.success(f"✅ Sehr gut! {score}/{total} ({pct}%)")
            else:
                st.warning(f"🔄 {score}/{total} ({pct}%) — Review the explanation and try again!")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Retry quiz"):
                    st.session_state.quiz_idx = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_done = False
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
                    st.rerun()
            with col2:
                if pct >= 75 and st.button("➡️ Next lesson", type="primary"):
                    next_id = lesson_id + 1
                    db.set_setting("current_lesson", str(next_id))
                    conn = db.get_conn()
                    conn.execute("INSERT INTO lessons (topic, score) VALUES (?,?)", (lesson["topic"], score))
                    conn.commit()
                    conn.close()
                    st.session_state.quiz_idx = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_done = False
                    st.session_state.quiz_answered = False
                    st.rerun()
        else:
            q_idx = st.session_state.quiz_idx
            if q_idx < len(quiz):
                q = quiz[q_idx]
                st.markdown(f"**Question {q_idx+1} of {len(quiz)}:**")
                st.markdown(f"### {q['q']}")
                st.markdown("")

                options = q["options"]
                if not st.session_state.quiz_answered:
                    for opt in options:
                        if st.button(opt, key=f"quiz_opt_{q_idx}_{opt}"):
                            st.session_state.quiz_answered = True
                            st.session_state.quiz_selected = opt
                            if opt == q["a"]:
                                st.session_state.quiz_score += 1
                            st.rerun()
                else:
                    sel = st.session_state.quiz_selected
                    for opt in options:
                        if opt == q["a"]:
                            st.markdown(f'<p class="correct">✅ {opt}</p>', unsafe_allow_html=True)
                        elif opt == sel and sel != q["a"]:
                            st.markdown(f'<p class="wrong">❌ {opt}</p>', unsafe_allow_html=True)
                        else:
                            st.markdown(f"   {opt}")

                    st.markdown("")
                    if st.button("Next question →"):
                        st.session_state.quiz_idx += 1
                        st.session_state.quiz_answered = False
                        st.session_state.quiz_selected = None
                        if st.session_state.quiz_idx >= len(quiz):
                            st.session_state.quiz_done = True
                        st.rerun()


# ── Page: Flashcards ───────────────────────────────────────────────────────────
elif st.session_state.page == "flashcards":
    st.markdown("# 🃏 Flashcard Review (SRS)")

    # Load due words if not loaded
    if not st.session_state.fc_words:
        due = db.get_due_words(limit=30)
        if not due:
            st.success("🎉 Nothing due right now! Come back later or study ahead.")
            st.caption(f"Total words in deck: {db.get_stats()['total_words']}")
            if st.button("Study all words anyway"):
                st.session_state.fc_words = db.get_all_words()
                st.session_state.fc_idx = 0
                st.rerun()
            st.stop()
        random.shuffle(due)
        st.session_state.fc_words = due
        st.session_state.fc_idx = 0
        st.session_state.fc_session_correct = 0
        st.session_state.fc_session_total = 0

    words = st.session_state.fc_words
    idx = st.session_state.fc_idx

    if idx >= len(words):
        # Session complete
        correct = st.session_state.fc_session_correct
        total = st.session_state.fc_session_total
        pct = int(correct/total*100) if total > 0 else 0
        st.success(f"✅ Session complete! {correct}/{total} correct ({pct}%)")
        db.log_session(
            duration_min=max(1, int((time.time()-st.session_state.session_start)/60)),
            words_reviewed=total,
            words_correct=correct,
            xp=correct*10
        )
        if st.button("🔄 Start new session"):
            st.session_state.fc_words = []
            st.session_state.fc_idx = 0
            st.session_state.fc_revealed = False
            st.session_state.session_start = time.time()
            st.rerun()
        st.stop()

    word = words[idx]
    progress = idx / len(words)

    # Progress bar
    col1, col2, col3 = st.columns([6, 1, 1])
    with col1:
        st.progress(progress, text=f"Card {idx+1} of {len(words)}")
    with col2:
        st.markdown(f"✅ {st.session_state.fc_session_correct}")
    with col3:
        st.markdown(f"❌ {st.session_state.fc_session_total - st.session_state.fc_session_correct}")

    # Flashcard
    article = word.get("article", "")
    art_class = article if article in ["der", "die", "das"] else ""
    art_html = f'<div class="article-badge {art_class}">{article}</div>' if article else ""
    example = word.get("example_de", "")
    example_html = f'<p class="example-text">"{example}"</p>' if example else ""

    st.markdown(f"""
    <div class="flashcard">
        {art_html}
        <div class="german-word">{word['german']}</div>
        <p style="color:#555577;font-size:0.9rem;margin-top:8px">🔵 der &nbsp;|&nbsp; 🔴 die &nbsp;|&nbsp; 🟢 das</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.fc_revealed:
        col_center = st.columns([1, 2, 1])[1]
        with col_center:
            if st.button("👁️ Reveal answer", use_container_width=True, type="primary"):
                st.session_state.fc_revealed = True
                st.rerun()
    else:
        # Show answer
        st.markdown(f"""
        <div style="text-align:center;padding:20px;background:#1a1a24;border-radius:12px;margin:12px 0">
            <div style="font-size:1.6rem;color:#e8d5b7;font-family:'DM Serif Display',serif">{word['english']}</div>
            {example_html}
        </div>
        """, unsafe_allow_html=True)

        if word.get("example_en"):
            st.caption(f"*{word['example_en']}*")

        st.markdown("**How well did you know it?**")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("😓 Hard\n\nReview tomorrow", use_container_width=True):
                db.record_review(word["id"], 0)
                st.session_state.fc_session_total += 1
                st.session_state.fc_idx += 1
                st.session_state.fc_revealed = False
                st.rerun()
        with col2:
            if st.button("🙂 Okay\n\nReview in 2+ days", use_container_width=True):
                db.record_review(word["id"], 1)
                st.session_state.fc_session_total += 1
                st.session_state.fc_session_correct += 1
                st.session_state.fc_idx += 1
                st.session_state.fc_revealed = False
                st.rerun()
        with col3:
            if st.button("😎 Easy\n\nReview in 4+ days", use_container_width=True):
                db.record_review(word["id"], 2)
                st.session_state.fc_session_total += 1
                st.session_state.fc_session_correct += 1
                st.session_state.fc_idx += 1
                st.session_state.fc_revealed = False
                st.rerun()

    # Skip option
    if st.button("⏭ Skip this card"):
        st.session_state.fc_idx += 1
        st.session_state.fc_revealed = False
        st.rerun()


# ── Page: Stories ──────────────────────────────────────────────────────────────
elif st.session_state.page == "stories":
    st.markdown("# 📚 Story Reader")
    st.caption("Read graded German texts. Click on a word you don't know to save it to your deck.")

    tab1, tab2 = st.tabs(["🧸 Grimm Stories (A1)", "📰 DW News (A2-B1)"])

    with tab1:
        stories = story_reader.get_grimm_stories()
        if not st.session_state.story_id:
            st.markdown("### Choose a story")
            for s in stories:
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{s['title']}** `{s['level']}`")
                with c2:
                    if st.button("Read →", key=f"story_{s['id']}"):
                        st.session_state.story_id = s["id"]
                        st.rerun()
                st.divider()
        else:
            story = story_reader.get_grimm_story(st.session_state.story_id)
            if story:
                if st.button("← Back to stories"):
                    st.session_state.story_id = None
                    st.rerun()

                st.markdown(f"## {story['title']}")
                st.caption(f"Level: {story['level']}")

                # Render story text with clickable words
                st.markdown('<div class="story-text">', unsafe_allow_html=True)
                st.markdown(story["text"])
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("### 📖 Glossary for this story")
                st.caption("Add any word to your SRS deck:")
                cols = st.columns(3)
                for i, (german, english) in enumerate(story["glossary"].items()):
                    with cols[i % 3]:
                        with st.container():
                            st.markdown(f"**{german}**")
                            st.caption(english)
                            if st.button("+ Add to deck", key=f"gloss_{german}"):
                                db.add_word(german, english, topic="stories")
                                st.toast(f"Added '{german}' to your deck!")

    with tab2:
        st.markdown("### DW Langsam gesprochene Nachrichten")
        st.caption("Slow German news — specially made for language learners (A2-B1 level)")

        if st.button("🔄 Fetch latest news from DW"):
            with st.spinner("Fetching..."):
                articles = story_reader.fetch_dw_news()
                if articles:
                    st.session_state["dw_articles"] = articles
                    st.success(f"Loaded {len(articles)} articles!")
                else:
                    st.warning("Couldn't fetch live news (no internet?). Showing sample articles.")
                    st.session_state["dw_articles"] = story_reader.get_sample_dw_news()

        articles = st.session_state.get("dw_articles", story_reader.get_sample_dw_news())
        for art in articles:
            with st.expander(f"📰 {art['title']} `{art['level']}`"):
                st.markdown('<div class="story-text">', unsafe_allow_html=True)
                st.markdown(art["text"])
                st.markdown('</div>', unsafe_allow_html=True)
                if art.get("link"):
                    st.markdown(f"[Read full article on DW →]({art['link']})")
                if st.button("🔍 Ask tutor about this article", key=f"tutor_art_{art['title'][:20]}"):
                    st.session_state.tutor_messages = [{"role": "user", "content": f"Can you help me understand this German text and explain any difficult vocabulary?\n\n{art['text'][:500]}"}]
                    st.session_state.page = "tutor"
                    st.rerun()


# ── Page: Roleplay ─────────────────────────────────────────────────────────────
elif st.session_state.page == "roleplay":
    st.markdown("# 🎭 Roleplay — Aachen Scenarios")

    all_scenarios = scenarios.get_all_scenarios()

    if not st.session_state.current_scenario:
        st.caption("Pick a real-life Aachen scenario and practice speaking German. The AI will play the other person and correct your German!")
        for s in all_scenarios:
            diff_color = {"A1": "🟢", "A2": "🟡", "B1": "🟠"}.get(s["difficulty"], "⚪")
            with st.container():
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f"**{s['title']}** {diff_color} `{s['difficulty']}`")
                    st.caption(s["description"])
                    st.markdown("💡 *" + s["tips"] + "*")
                with c2:
                    if st.button("Start →", key=f"sc_{s['id']}", use_container_width=True):
                        st.session_state.current_scenario = s["id"]
                        st.session_state.chat_messages = [{"role": "assistant", "content": s["starter"]}]
                        st.rerun()
                st.divider()
    else:
        sc = scenarios.get_scenario(st.session_state.current_scenario)
        if not sc:
            st.error("Scenario not found")
            st.stop()

        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"## {sc['title']}")
            st.caption(sc["description"])
        with col2:
            if st.button("🚪 Exit scenario"):
                st.session_state.current_scenario = None
                st.session_state.chat_messages = []
                st.rerun()

        # Vocab hints
        with st.expander("💡 Useful words for this scenario"):
            cols = st.columns(3)
            for i, hint in enumerate(sc.get("vocab_hints", [])):
                with cols[i % 3]:
                    st.markdown(f"• **{hint}**")
        st.caption(f"💡 Try: *{sc['tips']}*")
        st.divider()

        # Chat display
        for msg in st.session_state.chat_messages:
            role = msg["role"]
            content = msg["content"]
            css_class = "chat-tutor" if role == "assistant" else "chat-user"
            label = "🇩🇪 " + sc["title"] if role == "assistant" else "👤 You"
            st.markdown(f'<div class="{css_class}"><strong>{label}:</strong><br>{content}</div>', unsafe_allow_html=True)

        st.markdown("")
        user_input = st.text_input(
            "Your reply (type in German):",
            placeholder="Ich hätte gerne...",
            key=f"roleplay_input_{len(st.session_state.chat_messages)}"
        )

        if st.button("Send 📤", type="primary") and user_input.strip():
            st.session_state.chat_messages.append({"role": "user", "content": user_input})

            # Build messages for LLM
            llm_msgs = [{"role": m["role"], "content": m["content"]}
                       for m in st.session_state.chat_messages]

            with st.spinner("Antwort..."):
                response = llm.chat(llm_msgs, system=sc["system_prompt"])

            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()


# ── Page: AI Tutor ─────────────────────────────────────────────────────────────
elif st.session_state.page == "tutor":
    st.markdown("# 💬 AI Tutor — Klaus")
    st.caption("Ask anything about German grammar, vocabulary, or pronunciation. Klaus will explain and correct your German.")

    if not llm.is_available():
        st.warning("⚠️ AI Tutor is offline. Start Ollama (`ollama serve`) or add a GROQ_API_KEY to your environment.")

    # Quick prompts
    st.markdown("**Quick questions:**")
    quick = [
        "Explain when to use 'seit' vs 'vor' in German",
        "What's the difference between 'kennen' and 'wissen'?",
        "Correct my German: Ich bin 25 Jahre.",
        "How do German adjective endings work?",
        "When do I use 'du' vs 'Sie'?",
        "Explain the Dativ case simply.",
    ]
    cols = st.columns(3)
    for i, q in enumerate(quick):
        with cols[i % 3]:
            if st.button(q, key=f"quick_{i}"):
                st.session_state.tutor_messages.append({"role": "user", "content": q})
                with st.spinner("Klaus is thinking..."):
                    response = llm.chat(st.session_state.tutor_messages)
                st.session_state.tutor_messages.append({"role": "assistant", "content": response})
                st.rerun()

    st.divider()

    # Chat history
    for msg in st.session_state.tutor_messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user"><strong>You:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-tutor"><strong>🧑‍🏫 Klaus:</strong><br>{msg["content"]}</div>', unsafe_allow_html=True)

    st.markdown("")
    user_q = st.text_input(
        "Ask Klaus anything:",
        placeholder="Warum sagt man 'Ich habe Hunger' und nicht 'Ich bin hungrig'?",
        key=f"tutor_input_{len(st.session_state.tutor_messages)}"
    )

    c1, c2 = st.columns([1, 5])
    with c1:
        if st.button("Ask 📤", type="primary") and user_q.strip():
            st.session_state.tutor_messages.append({"role": "user", "content": user_q})
            with st.spinner("Klaus is thinking..."):
                response = llm.chat(st.session_state.tutor_messages)
            st.session_state.tutor_messages.append({"role": "assistant", "content": response})
            st.rerun()
    with c2:
        if st.button("🗑️ Clear chat") and st.session_state.tutor_messages:
            st.session_state.tutor_messages = []
            st.rerun()


# ── Page: Progress ─────────────────────────────────────────────────────────────
elif st.session_state.page == "progress":
    st.markdown("# 📊 Your Progress")

    stats = db.get_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Streak", f"{stats['streak']} days")
    c2.metric("📝 Total words", stats['total_words'])
    c3.metric("✅ Mastered (7+ day interval)", stats['mastered'])
    c4.metric("⚠️ Still struggling", stats['struggling'])

    st.divider()

    # Session history chart
    history = db.get_session_history(30)
    if history:
        st.markdown("### 📅 Activity (last 30 days)")
        dates = [h["session_date"] for h in reversed(history)]
        words = [h["words_reviewed"] for h in reversed(history)]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=dates, y=words,
            marker_color="#5b8dd9",
            name="Words reviewed"
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c0c0d8"),
            xaxis=dict(gridcolor="#2a2a3a"),
            yaxis=dict(gridcolor="#2a2a3a", title="Words reviewed"),
            margin=dict(l=0, r=0, t=10, b=0),
            height=250,
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Complete your first session to see your activity chart!")

    # Word mastery breakdown
    st.markdown("### 🗂️ Vocabulary by topic")
    conn = db.get_conn()
    topics = conn.execute(
        "SELECT topic, COUNT(*) as n FROM words GROUP BY topic ORDER BY n DESC"
    ).fetchall()
    conn.close()

    if topics:
        labels = [t["topic"] for t in topics]
        values = [t["n"] for t in topics]
        fig2 = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.5,
            marker_colors=["#5b8dd9","#9b59b6","#5b9e6a","#d4ac0d","#c0504d","#5b8dd9","#3498db"],
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#c0c0d8"),
            showlegend=True,
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Lessons completed
    st.markdown("### 📚 Lessons completed")
    conn = db.get_conn()
    done = conn.execute("SELECT * FROM lessons ORDER BY completed_at DESC").fetchall()
    conn.close()

    if done:
        for l in done:
            st.markdown(f"✅ **{l['topic']}** — score {l['score']}/4 — {l['completed_at'][:10]}")
    else:
        st.info("Complete your first lesson to see it here!")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💾 Add a custom word")
        with st.form("add_word_form"):
            german = st.text_input("German word")
            english = st.text_input("English translation")
            article = st.selectbox("Article", ["", "der", "die", "das"])
            example = st.text_input("Example sentence (German)", "")
            topic = st.text_input("Topic", "custom")
            if st.form_submit_button("Add to deck"):
                if german and english:
                    db.add_word(german, english, article, example, "", topic)
                    st.success(f"Added: {article} {german} = {english}")
                else:
                    st.error("Please fill in German and English.")


# ── Page: Camera Vision ────────────────────────────────────────────────────────
elif st.session_state.page == "camera":
    import socket

    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "localhost"

    ip = get_local_ip()

    st.markdown("# 📷 Camera Vision — Real-world German")
    st.caption("Live object detection with German labels. Runs in your browser — no extra installs needed beyond the server.")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎥 Live Object Detection")
        st.markdown(f"""
The camera runs via YOLO-World. Point at anything — objects get labelled in German with the correct article.
Open on any device on your WiFi, or use the embedded view below.
""")
        st.markdown(f"### 👉 [https://{ip}:8764](https://{ip}:8764)")
        st.caption("Tip: accept the certificate warning on first visit.")
        st.markdown("**Or use embedded view (desktop only):**")
        st.components.v1.iframe(f"https://{ip}:8764", height=520, scrolling=False)

    with col2:
        st.markdown("### How to start")
        st.code("""# In a separate terminal (conda activate german-agent first):
python german_vision_server.py""", language="bash")
        st.markdown("""
Then open the link above in **any browser on your WiFi**.

**Features:**
- YOLO-World detects 200+ everyday objects  
- Labels shown in German with correct article  
- 🔵 der · 🟣 die · 🟢 das colour coding on boxes  
- Tap **+ Deck** on any word to save it to your SRS flashcards  
- Works on your phone camera directly  
- No HTTPS setup needed — plain HTTP works fine for this approach
""")

    st.divider()
    st.markdown("### 📝 OCR Text Translation")
    st.caption("Upload a photo of German text — menus, signs, packaging — and get it translated.")

    deps = cv_module.check_dependencies()
    if not deps.get("easyocr"):
        st.warning("Install EasyOCR for text translation: ")

    ocr_col1, ocr_col2 = st.columns(2)
    with ocr_col1:
        ocr_input = st.radio("Source", ["📁 Upload image", "📸 Take photo"],
                            horizontal=True, label_visibility="collapsed")
        pil_ocr = None
        if ocr_input == "📁 Upload image":
            up = st.file_uploader("Upload", type=["jpg","jpeg","png","webp"],
                                 label_visibility="collapsed", key="ocr_up")
            if up:
                pil_ocr = cv_module.to_pil(up)
        else:
            snap = st.camera_input("Photo", label_visibility="collapsed", key="ocr_snap")
            if snap:
                pil_ocr = cv_module.to_pil(snap)

        if pil_ocr:
            st.image(pil_ocr, caption="Original", use_container_width=True)

    with ocr_col2:
        if pil_ocr:
            if not deps.get("easyocr"):
                st.error("Install: ")
            else:
                with st.spinner("Reading text..."):
                    texts, err = cv_module.read_text_from_image(pil_ocr)
                if err:
                    st.error(err)
                elif not texts:
                    st.info("No text detected. Ensure good lighting and focus.")
                else:
                    with st.spinner("Translating..."):
                        texts = cv_module.translate_texts(texts, llm)
                    annotated = cv_module.draw_ocr_boxes(pil_ocr, texts)
                    st.image(annotated, caption="With translations", use_container_width=True)

                    st.markdown("**Detected text:**")
                    for i, item in enumerate(texts):
                        translation = item.get("translation","")
                        c1, c2, c3 = st.columns([2,2,1])
                        with c1:
                            st.markdown(f"**{item['text']}**")
                            st.caption(f"{int(item['confidence']*100)}% confidence")
                        with c2:
                            st.markdown(f"→ *{translation}*")
                        with c3:
                            if st.button("+ Deck", key=f"ocr_{i}"):
                                db.add_word(item["text"], translation, topic="camera_ocr")
                                st.toast(f"Added: {item['text']}")
                        st.divider()

    with st.expander("💡 Tips"):
        st.markdown("""
**Live detection tips:**
- The server uses your existing  from agent 6 — no re-download
- 200+ object vocabulary — far beyond standard YOLO
- Article colour coding drawn directly on bounding boxes
- Tap **+ Deck** in the browser UI to save words to your SRS deck

**OCR works best on:** REWE/ALDI ingredient lists, restaurant menus, street signs, German books, product labels
        """)

# ── Page: Audio Translator ─────────────────────────────────────────────────────
elif st.session_state.page == "audio":
    try:
        import audio_translator as audio_mod
    except Exception as _e:
        st.error(f"Could not load audio_translator: {_e}")
        st.stop()

    st.markdown("# 🎙️ Audio Translator")
    st.caption("Speak in English → get German translation spoken back. Or speak German → get English. Push-to-talk.")

    # Dependency check
    deps = audio_mod.check_dependencies()
    missing = [k for k, v in deps.items() if not v]
    if missing:
        st.warning(f"⚠️ Missing packages: `{', '.join(missing)}`")
        st.code("pip install faster-whisper sounddevice gTTS pygame numpy", language="bash")
        st.caption("After installing, restart the app.")
        st.stop()

    st.divider()

    # Direction selector
    col_dir, col_info = st.columns([2, 3])
    with col_dir:
        direction = st.radio(
            "Translation direction",
            ["🇬🇧 English → German", "🇩🇪 German → English"],
            label_visibility="collapsed"
        )
        dir_code = "en→de" if direction.startswith("🇬🇧") else "de→en"

    with col_info:
        if dir_code == "en→de":
            st.info("🇬🇧 Speak English → translated to German and spoken back.\nGreat for learning how to say things.")
        else:
            st.info("🇩🇪 Speak German → translated to English and spoken back.\nGreat for understanding German you hear.")

    st.divider()

    # Recording duration
    duration = st.slider("Max recording duration (seconds)", 3, 15, 6)

    # Session state for results
    if "audio_result" not in st.session_state:
        st.session_state.audio_result = None
    if "audio_recording" not in st.session_state:
        st.session_state.audio_recording = False

    # Push-to-talk button
    col_btn, col_status = st.columns([1, 3])
    with col_btn:
        record_btn = st.button(
            "🎙️ Hold to Record",
            type="primary",
            use_container_width=True,
            disabled=st.session_state.audio_recording
        )
    with col_status:
        if st.session_state.audio_recording:
            st.markdown("🔴 **Recording...** speak now")
        elif st.session_state.audio_result:
            st.markdown("✅ Done — see results below")
        else:
            st.markdown("Press the button and speak")

    if record_btn:
        st.session_state.audio_recording = True
        st.session_state.audio_result = None
        st.rerun()

    if st.session_state.audio_recording:
        with st.spinner(f"🎙️ Recording for up to {duration} seconds... speak now!"):
            try:
                audio_array, sample_rate = audio_mod.record_audio(duration_seconds=duration)
            except Exception as e:
                st.error(f"Microphone error: {e}")
                st.caption("Make sure your microphone is connected and not blocked by another app.")
                st.session_state.audio_recording = False
                st.stop()

        st.session_state.audio_recording = False

        with st.spinner("Transcribing and translating..."):
            result = audio_mod.translate_speech(
                audio_array, sample_rate, dir_code, llm
            )

        st.session_state.audio_result = result
        st.rerun()

    # Results
    if st.session_state.audio_result:
        result = st.session_state.audio_result

        if result.get("error"):
            st.error(result["error"])
        else:
            st.divider()

            col_orig, col_trans = st.columns(2)

            with col_orig:
                src_flag = "🇬🇧" if dir_code == "en→de" else "🇩🇪"
                src_label = "English (you said)" if dir_code == "en→de" else "German (you said)"
                st.markdown(f"**{src_flag} {src_label}:**")
                st.markdown(f"""
                <div style="background:#1a1a24;border-left:3px solid #5b8dd9;
                            padding:16px;border-radius:0 12px 12px 0;
                            font-size:1.1rem;color:#d0d0f0;line-height:1.6">
                    {result['original']}
                </div>
                """, unsafe_allow_html=True)

            with col_trans:
                tgt_flag = "🇩🇪" if dir_code == "en→de" else "🇬🇧"
                tgt_label = "German translation" if dir_code == "en→de" else "English translation"
                st.markdown(f"**{tgt_flag} {tgt_label}:**")
                st.markdown(f"""
                <div style="background:#1a2418;border-left:3px solid #5b9e6a;
                            padding:16px;border-radius:0 12px 12px 0;
                            font-size:1.1rem;color:#c0e0c8;line-height:1.6">
                    {result['translated']}
                </div>
                """, unsafe_allow_html=True)

            st.divider()

            # Audio playback
            if result.get("audio_bytes"):
                st.markdown("**🔊 Listen to translation:**")
                st.audio(result["audio_bytes"], format="audio/mp3")
            elif result.get("tts_error"):
                st.warning(f"TTS unavailable: {result['tts_error']}")

            # Add to SRS deck
            col_add, col_clear = st.columns([2, 1])
            with col_add:
                if dir_code == "en→de":
                    german_word = result["translated"]
                    english_word = result["original"]
                else:
                    german_word = result["original"]
                    english_word = result["translated"]

                # Only offer add if it's a short phrase (likely a word/short phrase)
                if len(german_word.split()) <= 6:
                    if st.button("➕ Add to SRS flashcard deck", type="primary"):
                        db.add_word(german_word, english_word, topic="audio_translator")
                        st.success(f"Added: **{german_word}** = {english_word}")
                        st.toast(f"Added to deck: {german_word}")

            with col_clear:
                if st.button("🗑️ Clear"):
                    st.session_state.audio_result = None
                    st.rerun()

    st.divider()
    with st.expander("💡 Tips for best results"):
        st.markdown("""
**Recording tips:**
- Speak clearly and at a normal pace
- Hold your phone close to your mouth, or use a headset
- Reduce background noise if possible
- Whisper model downloads ~150MB on first use — this is normal

**English → German** is great for:
- Learning how to say something before going out
- Preparing for a bakery, supermarket, or Bürgeramt visit
- Practising phrases from your lessons

**German → English** is great for:
- Understanding something a German speaker just said
- Checking if your German pronunciation was understood correctly
- Translating overheard conversations or announcements

**Whisper model sizes** (edit `audio_translator.py` to change):
- `tiny` — fastest, less accurate (~75MB)
- `base` — good balance, default (~150MB)  
- `small` — more accurate, slower (~500MB)
        """)
