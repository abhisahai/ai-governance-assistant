# ─────────────────────────────────────────────────────────────
# AI Governance Assistant
# Author: Abhinav Sahai | linkedin.com/in/absahai
# GitHub: github.com/abhisahai/ai-governance-assistant
# Licence: MIT © 2026
# ─────────────────────────────────────────────────────────────

import streamlit as st

st.set_page_config(
    page_title="AI Governance Assistant",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}
h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; }

.stApp { background: #0a0f1e; color: #e0e6f0; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1526;
    border-right: 1px solid #1e3a5f;
}

/* Cards */
.gov-card {
    background: #0d1a30;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.gov-card-accent {
    border-left: 4px solid #00d4ff;
}

/* Badges */
.badge-low    { background:#0a2e1a; color:#00e676; border:1px solid #00e676; padding:2px 10px; border-radius:20px; font-size:.75rem; font-family:'IBM Plex Mono',monospace; }
.badge-medium { background:#2e2000; color:#ffab40; border:1px solid #ffab40; padding:2px 10px; border-radius:20px; font-size:.75rem; font-family:'IBM Plex Mono',monospace; }
.badge-high   { background:#2e0a0a; color:#ff5252; border:1px solid #ff5252; padding:2px 10px; border-radius:20px; font-size:.75rem; font-family:'IBM Plex Mono',monospace; }

/* Metric tiles */
.metric-tile {
    background: #0d1a30;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.metric-tile .val { font-size:2rem; font-weight:700; font-family:'IBM Plex Mono',monospace; color:#00d4ff; }
.metric-tile .lbl { font-size:.75rem; color:#7090b0; margin-top:4px; }

/* Status dot */
.dot-green  { height:10px;width:10px;border-radius:50%;background:#00e676;display:inline-block;margin-right:6px; }
.dot-orange { height:10px;width:10px;border-radius:50%;background:#ffab40;display:inline-block;margin-right:6px; }
.dot-red    { height:10px;width:10px;border-radius:50%;background:#ff5252;display:inline-block;margin-right:6px; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #0066cc, #0044aa);
    color: white;
    border: none;
    border-radius: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: .85rem;
    padding: .5rem 1.2rem;
    transition: all .2s;
}
.stButton > button:hover { background: linear-gradient(135deg, #0088ff, #0066cc); transform: translateY(-1px); }

/* Text inputs */
.stTextArea textarea, .stTextInput input {
    background: #0d1a30 !important;
    border: 1px solid #1e3a5f !important;
    color: #e0e6f0 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    border-radius: 6px !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #0d1a30 !important;
    border: 1px solid #1e3a5f !important;
    color: #e0e6f0 !important;
}

/* Progress bar */
.stProgress > div > div > div { background: linear-gradient(90deg, #0066cc, #00d4ff) !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #0d1a30 !important;
    border: 1px solid #1e3a5f !important;
    border-radius: 6px !important;
    color: #e0e6f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
}
.streamlit-expanderContent { background: #0a1220 !important; border: 1px solid #1e3a5f !important; border-top: none !important; }

/* Tab labels */
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    color: #7090b0;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] { color: #00d4ff !important; border-bottom-color: #00d4ff !important; }

/* Divider */
hr { border-color: #1e3a5f !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 1.5rem'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;font-weight:600;color:#00d4ff;'>
            🛡️ AI Governance
        </div>
        <div style='font-size:.75rem;color:#7090b0;margin-top:4px;font-family:"IBM Plex Mono",monospace;'>
            v1.0.0 · Enterprise Edition
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.selectbox(
        "Navigation",
        ["🏠 Dashboard", "📋 Policy Validator", "⚠️ Risk Scorer", "✅ Compliance Workflow", "📊 Audit Summaries", "🤖 Compliance Agent"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("<div style='font-size:.7rem;color:#7090b0;font-family:\"IBM Plex Mono\",monospace;'>OPENAI MODEL</div>", unsafe_allow_html=True)
    model = st.selectbox("Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"], label_visibility="collapsed")
    st.session_state["model"] = model

    st.markdown("<div style='font-size:.7rem;color:#7090b0;font-family:\"IBM Plex Mono\",monospace;margin-top:1rem;'>API KEY</div>", unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", placeholder="sk-...", label_visibility="collapsed")
    if api_key:
        st.session_state["api_key"] = api_key
        st.markdown("<span class='dot-green'></span><span style='font-size:.75rem;color:#00e676;'>Connected</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='dot-orange'></span><span style='font-size:.75rem;color:#ffab40;'>No API Key</span>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:.7rem;color:#506070;line-height:1.6;font-family:"IBM Plex Mono",monospace;'>
    FRAMEWORK SUPPORT<br>
    ✓ EU AI Act<br>
    ✓ NIST AI RMF<br>
    ✓ ISO/IEC 42001<br>
    ✓ GDPR<br>
    ✓ SOC 2
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:.75rem;color:#506070;font-family:"IBM Plex Mono",monospace;margin-top:8px;'>
    Built by <a href='https://www.linkedin.com/in/absahai/' style='color:#00d4ff;'>Abhinav</a> - &copy; 2026 - MIT Licence
    </div>""", unsafe_allow_html=True)

# ── Page Routing ─────────────────────────────────────────────────────────────
if "🏠 Dashboard" in page:
    from pages.dashboard import render
elif "📋 Policy Validator" in page:
    from pages.policy_validator import render
elif "⚠️ Risk Scorer" in page:
    from pages.risk_scorer import render
elif "✅ Compliance Workflow" in page:
    from pages.compliance_workflow import render
elif "📊 Audit Summaries" in page:
    from pages.audit_summaries import render
elif "🤖 Compliance Agent" in page:
    from pages.compliance_agent import render

render()
