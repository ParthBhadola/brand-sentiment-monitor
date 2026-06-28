import streamlit as st
import time
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from db import get_recent, get_sentiment_counts, get_companies

st.set_page_config(
    page_title="Pulse — Brand Sentiment",
    page_icon="◎",
    layout="wide"
)

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }

    .app-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #e8eaf0;
        margin: 0;
        letter-spacing: -0.4px;
    }

    .app-sub {
        font-size: 0.82rem;
        color: #4b5563;
        margin-top: 0.2rem;
        margin-bottom: 0;
    }

    .divider {
        border: none;
        border-top: 1px solid #1f2937;
        margin: 1.2rem 0;
    }

    .section-label {
        font-size: 0.7rem;
        font-weight: 600;
        color: #4b5563;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.6rem;
    }

    .score-block {
        padding: 0.4rem 0;
    }

    .score-number {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        line-height: 1;
        letter-spacing: -1px;
    }

    .score-label {
        font-size: 0.75rem;
        color: #4b5563;
        margin: 0.3rem 0 0;
    }

    .stat-number {
        font-size: 1.6rem;
        font-weight: 600;
        margin: 0;
        line-height: 1;
    }

    .stat-label {
        font-size: 0.72rem;
        color: #4b5563;
        margin: 0.2rem 0 0;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }

    .positive { color: #34d399; }
    .negative { color: #f87171; }
    .neutral { color: #6b7280; }

    .headline-item {
        padding: 0.75rem 0;
        border-bottom: 1px solid #1f2937;
    }

    .headline-text {
        font-size: 0.88rem;
        color: #d1d5db;
        margin: 0;
        line-height: 1.5;
    }

    .headline-meta {
        font-size: 0.72rem;
        color: #4b5563;
        margin: 0.25rem 0 0;
    }

    .sentiment-pill {
        display: inline-block;
        font-size: 0.65rem;
        font-weight: 600;
        padding: 2px 7px;
        border-radius: 20px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    .pill-positive {
        background: #052e16;
        color: #34d399;
    }

    .pill-negative {
        background: #2d1515;
        color: #f87171;
    }

    .pill-neutral {
        background: #1f2937;
        color: #6b7280;
    }

    .sidebar-label {
        font-size: 0.72rem;
        color: #4b5563;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.4rem;
    }

    div[data-testid="stSelectbox"] > div > div {
        background: #111827 !important;
        border: 1px solid #1f2937 !important;
        border-radius: 6px !important;
        color: #e8eaf0 !important;
    }

    div[data-testid="stButton"] button {
        background: transparent !important;
        color: #6b7280 !important;
        border: 1px solid #1f2937 !important;
        font-size: 0.78rem !important;
        border-radius: 6px !important;
        font-weight: 400 !important;
        width: 100% !important;
    }

    div[data-testid="stButton"] button:hover {
        border-color: #374151 !important;
        color: #d1d5db !important;
    }

    div[data-testid="stCheckbox"] label {
        font-size: 0.78rem !important;
        color: #4b5563 !important;
    }
</style>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 3], gap="large")

with col_left:
    st.markdown("<p class='app-title'>Pulse</p>", unsafe_allow_html=True)
    st.markdown("<p class='app-sub'>Brand sentiment intelligence</p>", unsafe_allow_html=True)
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    companies = get_companies()

    if not companies:
        st.markdown("<p style='font-size:0.82rem;color:#4b5563;'>No data yet. Run the worker first.</p>", unsafe_allow_html=True)
        st.stop()

    st.markdown("<p class='sidebar-label'>Company</p>", unsafe_allow_html=True)
    selected = st.selectbox("", companies, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    auto_refresh = st.checkbox("Auto-refresh", value=True)
    st.button("↻  Refresh", use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem;color:#374151;'>Powered by Groq LLaMA · NewsAPI · SQLite</p>", unsafe_allow_html=True)

with col_right:
    if selected:
        counts = get_sentiment_counts(selected)
        total = sum(counts.values())
        positive = counts.get("POSITIVE", 0)
        negative = counts.get("NEGATIVE", 0)
        neutral = counts.get("NEUTRAL", 0)

        if total > 0:
            score = round((positive - negative) / total * 100, 1)
        else:
            score = 0

        score_color = "#34d399" if score > 0 else "#f87171" if score < 0 else "#6b7280"
        score_class = "positive" if score > 0 else "negative" if score < 0 else "neutral"

        st.markdown(f"""
            <p class='section-label'>{selected} — Sentiment Overview</p>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns([2, 1, 1, 1])

        with m1:
            st.markdown(f"""
                <div class='score-block'>
                    <p class='score-number {score_class}'>{score:+.1f}</p>
                    <p class='score-label'>Sentiment score &nbsp;·&nbsp; {total} headlines analysed</p>
                </div>
            """, unsafe_allow_html=True)

        with m2:
            st.markdown(f"""
                <p class='stat-number positive'>{positive}</p>
                <p class='stat-label'>Positive</p>
            """, unsafe_allow_html=True)

        with m3:
            st.markdown(f"""
                <p class='stat-number negative'>{negative}</p>
                <p class='stat-label'>Negative</p>
            """, unsafe_allow_html=True)

        with m4:
            st.markdown(f"""
                <p class='stat-number neutral'>{neutral}</p>
                <p class='stat-label'>Neutral</p>
            """, unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(7, 1.6))
        fig.patch.set_facecolor("#0d1117")
        ax.set_facecolor("#0d1117")

        categories = ["Positive", "Negative", "Neutral"]
        values = [positive, negative, neutral]
        colors = ["#34d399", "#f87171", "#6b7280"]

        bars = ax.barh(categories, values, color=colors, height=0.3)
        ax.set_xlabel("Headlines", color="#374151", fontsize=8)
        ax.tick_params(colors="#4b5563", labelsize=8)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_color("#1f2937")
        ax.spines["left"].set_color("#1f2937")

        for bar, val in zip(bars, values):
            if val > 0:
                ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
                       str(val), va="center", color="#6b7280", fontsize=8)

        plt.tight_layout(pad=0.5)
        st.pyplot(fig)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown("<p class='section-label'>Recent Headlines</p>", unsafe_allow_html=True)

        headlines = get_recent(selected, limit=20)
        for row in headlines:
            headline, source, published_at, sentiment, confidence, scored_at = row
            pill_class = f"pill-{sentiment.lower()}"
            st.markdown(f"""
                <div class='headline-item'>
                    <p class='headline-text'>{headline}</p>
                    <p class='headline-meta'>
                        {source} &nbsp;·&nbsp;
                        <span class='sentiment-pill {pill_class}'>{sentiment}</span>
                        &nbsp;·&nbsp; {confidence:.0%} confidence &nbsp;·&nbsp; {scored_at[:16]}
                    </p>
                </div>
            """, unsafe_allow_html=True)

if auto_refresh:
    time.sleep(30)
    st.rerun()