import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sentiment_engine import analyze_sentiment, generate_mock_data
import datetime

st.set_page_config(page_title="Sentiment Interaction Hub", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS to match the React dashboard
st.markdown("""
<style>
    /* Base theme colors */
    :root {
        --bg-color: #0f172a;
        --card-bg: #1e293b;
        --border-color: #334155;
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --accent-sky: #0ea5e9;
        --positive: #10b981;
        --negative: #f43f5e;
        --neutral: #475569;
    }

    /* Main background */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-main);
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Hide */
    header {visibility: hidden;}
    
    /* Custom Navbar */
    .custom-navbar {
        border-bottom: 1px solid var(--border-color);
        padding: 1rem 2rem;
        background-color: var(--card-bg);
        display: flex;
        align-items: center;
        gap: 2rem;
        margin-top: -60px;
        margin-bottom: 2rem;
        margin-left: -4rem;
        margin-right: -4rem;
    }
    .navbar-brand {
        font-size: 1.125rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .navbar-brand span { color: var(--accent-sky); font-weight: normal; font-size: 0.875rem;}
    .navbar-tab {
        color: var(--accent-sky);
        border-bottom: 2px solid var(--accent-sky);
        padding-bottom: 0.25rem;
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    /* Typography */
    h1 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.25rem !important;
    }
    .subtitle {
        color: var(--text-muted);
        font-size: 0.875rem;
        margin-bottom: 2rem;
    }
    
    /* Custom Cards for Metrics */
    .metric-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .metric-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-muted);
        font-weight: 600;
        margin-bottom: 0.25rem;
    }
    .metric-value {
        font-size: 1.875rem;
        font-weight: 700;
        color: var(--text-main);
    }
    .metric-icon-wrapper {
        width: 3rem;
        height: 3rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .icon-sky { background-color: rgba(14, 165, 233, 0.1); border: 1px solid rgba(14, 165, 233, 0.2); color: var(--accent-sky); }
    .icon-emerald { background-color: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); color: var(--positive); }
    .icon-rose { background-color: rgba(244, 63, 94, 0.1); border: 1px solid rgba(244, 63, 94, 0.2); color: var(--negative); }
    .icon-slate { background-color: rgba(71, 85, 105, 0.1); border: 1px solid rgba(71, 85, 105, 0.2); color: var(--neutral); }
    
    /* Live Model Testing Box */
    .card-box {
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        height: 100%;
    }
    .card-title {
        font-size: 0.875rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-desc {
        font-size: 0.75rem;
        color: var(--text-muted);
        font-family: monospace;
        margin-bottom: 1rem;
    }
    
    /* Streamlit overrides */
    .stTextArea textarea {
        background-color: #0f172a !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 0.5rem !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--accent-sky) !important;
        box-shadow: 0 0 0 1px var(--accent-sky) !important;
    }
    .stButton button {
        width: 100% !important;
        background-color: rgba(14, 165, 233, 0.2) !important;
        color: var(--accent-sky) !important;
        border: 1px solid rgba(14, 165, 233, 0.5) !important;
        border-radius: 0.5rem !important;
        padding: 0.5rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
    }
    .stButton button:hover {
        background-color: rgba(14, 165, 233, 0.3) !important;
        color: var(--accent-sky) !important;
    }

    /* Badges */
    .badge-platform {
        background-color: #334155;
        color: #cbd5e1;
        padding: 0.1rem 0.4rem;
        border-radius: 0.25rem;
        font-size: 0.6rem;
        border: 1px solid #475569;
    }
    .badge-sentiment {
        padding: 0.1rem 0.4rem;
        border-radius: 0.25rem;
        font-size: 0.6rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-width: 1px;
        border-style: solid;
        display: inline-block;
    }
    .badge-pos { color: #34d399; background-color: rgba(52, 211, 153, 0.1); border-color: rgba(52, 211, 153, 0.3); }
    .badge-neg { color: #fb7185; background-color: rgba(251, 113, 133, 0.1); border-color: rgba(251, 113, 133, 0.3); }
    .badge-neu { color: #94a3b8; background-color: rgba(148, 163, 184, 0.1); border-color: rgba(148, 163, 184, 0.3); }
    
    /* Hide index in DataFrame and style it */
    table { width: 100%; border-collapse: collapse; font-size: 0.75rem; }
    th { text-transform: uppercase; font-size: 0.65rem; letter-spacing: 0.05em; color: var(--text-muted); border-bottom: 1px solid var(--border-color); padding: 0.75rem 1.5rem; text-align: left; }
    td { padding: 1rem 1.5rem; border-bottom: 1px solid rgba(51, 65, 85, 0.5); color: #cbd5e1; font-family: monospace; }
    tr:hover { background-color: rgba(51, 65, 85, 0.3); }
    
</style>
""", unsafe_allow_html=True)

# App State
if 'data' not in st.session_state:
    st.session_state.data = generate_mock_data()

# Data Calculations
df = pd.DataFrame(st.session_state.data)
total = len(df)
pos_count = len(df[df['sentiment'] == 'Positive'])
neg_count = len(df[df['sentiment'] == 'Negative'])
neu_count = len(df[df['sentiment'] == 'Neutral'])

polarity_score = "0.0"
if total > 0:
    score = ((pos_count - neg_count) / total) * 100
    polarity_score = f"{'+' if score > 0 else ''}{score:.1f}%"

top_emotion = 'Neutral'
max_count = neu_count
if pos_count >= max_count:
    top_emotion = 'Positive'
    max_count = pos_count
if neg_count > max_count:
    top_emotion = 'Negative'
    max_count = neg_count

# Helper for colors
def get_emotion_color(emotion):
    if emotion == 'Positive': return 'emerald'
    if emotion == 'Negative': return 'rose'
    return 'slate'

# Navbar
st.markdown("""
<div class="custom-navbar">
    <div class="navbar-brand">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0ea5e9" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M7 15v2"/><path d="M12 11v6"/><path d="M17 13v4"/></svg>
        SentimentML <span>v1.0</span>
    </div>
    <div class="navbar-tab">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:inline; margin-right:4px;"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>
        Live Dashboard
    </div>
</div>
""", unsafe_allow_html=True)

# Main Header
st.markdown("<h1>Sentiment Interaction Hub</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A demonstration of the requested Streamlit dashboard logic, built interactively here in React. (Now replicated in Python!)</div>", unsafe_allow_html=True)

# Metrics Row
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Total Comments Analyzed</div>
            <div class="metric-value">{total}</div>
        </div>
        <div class="metric-icon-wrapper icon-sky">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    pol_color = "emerald" if "+" in polarity_score else "rose" if "-" in polarity_score else "sky"
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Overall Polarity Score</div>
            <div class="metric-value" style="color: var(--{'positive' if '+' in polarity_score else 'negative' if '-' in polarity_score else 'accent-sky'});">{polarity_score}</div>
        </div>
        <div class="metric-icon-wrapper icon-{pol_color}">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    emo_color = get_emotion_color(top_emotion)
    st.markdown(f"""
    <div class="metric-card">
        <div>
            <div class="metric-label">Top Detected Emotion</div>
            <div class="metric-value">{top_emotion}</div>
        </div>
        <div class="metric-icon-wrapper icon-{emo_color}">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/></svg>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.write("") # spacing

# Main content row
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("<div class='card-title'><svg xmlns='http://www.w3.org/2000/svg' width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='#0ea5e9' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><path d='M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z'/><path d='M9 13a4.5 4.5 0 0 0 3-4'/><path d='M6.003 5.125A3 3 0 0 0 6.401 6.5'/><path d='M3.477 10.896a4 4 0 0 1 .585-.396'/><path d='M6 18a4 4 0 0 1-1.968-3.645'/><path d='M20 11.5a6 6 0 1 0-8 5.66'/><path d='M20 11.5a6 6 0 1 1-8 5.66'/></svg> Live Model Testing</div>", unsafe_allow_html=True)
    st.markdown("<div class='card-desc'>Simulating Streamlit text_area input. Type a mock review or tweet below.</div>", unsafe_allow_html=True)
    
    live_input = st.text_area("Live Input", placeholder="Type 'This app crashes every time' or 'Fantastic update!'", label_visibility="collapsed", height=130)
    if st.button("Analyze Sentiment"):
        if live_input.strip():
            res = analyze_sentiment(live_input)
            st.session_state.data.insert(0, {
                "id": f"live-{datetime.datetime.now().timestamp()}",
                "text": live_input,
                "platform": "Twitter",
                "date": datetime.datetime.now().isoformat(),
                "sentiment": res
            })
            st.rerun()
            
    # Show last live prediction if it exists and is fresh
    # Just show latest if it matches the text area
    if live_input and len(st.session_state.data) > 0 and st.session_state.data[0]['text'] == live_input:
        latest = st.session_state.data[0]['sentiment']
        bg_col = "#10b981" if latest == 'Positive' else "#f43f5e" if latest == 'Negative' else "#475569"
        border_col = "var(--positive)" if latest == 'Positive' else "var(--negative)" if latest == 'Negative' else "var(--neutral)"
        st.markdown(f"""
        <div style="margin-top: 1rem; padding: 1rem; border-radius: 0.5rem; background-color: #0f172a; border-left: 4px solid {border_col}; display:flex; justify-content: space-between; align-items:center;">
            <div>
                <div style="font-size: 10px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 0.25rem;">Prediction Result</div>
                <div style="font-weight: bold; color: {border_col};">{latest}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <style>
        .chart-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Sentiment Distribution (Batch Analysis)</div>", unsafe_allow_html=True)
    
    # Charts
    chart_data = pd.DataFrame({
        'Sentiment': ['Positive', 'Neutral', 'Negative'],
        'Count': [pos_count, neu_count, neg_count]
    })
    
    colors = {'Positive': '#10b981', 'Neutral': '#475569', 'Negative': '#f43f5e'}
    
    fig_col1, fig_col2 = st.columns(2)
    
    with fig_col1:
        # Pie Chart
        fig_pie = px.pie(
            chart_data, 
            values='Count', 
            names='Sentiment', 
            hole=0.6,
            color='Sentiment',
            color_discrete_map=colors
        )
        fig_pie.update_layout(
            showlegend=True, 
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color='#94a3b8', size=12)),
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, width='stretch', config={'displayModeBar': False})
        
    with fig_col2:
        # Bar Chart
        fig_bar = px.bar(
            chart_data, 
            x='Sentiment', 
            y='Count',
            color='Sentiment',
            color_discrete_map=colors
        )
        fig_bar.update_layout(
            showlegend=False,
            margin=dict(t=10, b=10, l=10, r=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, title="", tickfont=dict(color='#94a3b8')),
            yaxis=dict(showgrid=False, title="", showticklabels=True, tickfont=dict(color='#94a3b8'))
        )
        st.plotly_chart(fig_bar, width='stretch', config={'displayModeBar': False})


# Table
st.write("")
html_output = """<div style="background-color: var(--card-bg); border: 1px solid var(--border-color); border-radius: 1rem; overflow: hidden; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
<div style="padding: 1rem; border-bottom: 1px solid var(--border-color); display: flex; justify-content: space-between; align-items: center; background-color: rgba(15, 23, 42, 0.5);">
<div style="font-size: 0.875rem; font-weight: 600;">Recent Predictions (Live Simulation)</div>
<div style="font-size: 0.6rem; background-color: rgba(14, 165, 233, 0.2); color: var(--accent-sky); padding: 0.2rem 0.5rem; border-radius: 0.25rem;">CSV Input active</div>
</div>
<div style="overflow-x: auto;">
<table>
<thead>
<tr>
<th>Text Comment</th>
<th>Platform</th>
<th>Predicted Sentiment</th>
</tr>
</thead>
<tbody>"""

# Output Table Rows
for idx, row in df.head(8).iterrows():
    badge_class = "badge-pos" if row['sentiment'] == 'Positive' else "badge-neg" if row['sentiment'] == 'Negative' else "badge-neu"
    html_output += f"""<tr>
<td>{row['text']}</td>
<td><span class="badge-platform">{row['platform']}</span></td>
<td><span class="badge-sentiment {badge_class}">{row['sentiment']}</span></td>
</tr>"""

html_output += """</tbody>
</table>
</div>
</div>"""

st.markdown(html_output, unsafe_allow_html=True)
