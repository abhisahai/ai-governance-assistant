"""pages/risk_scorer.py — Multi-dimensional AI Risk Scoring."""

import streamlit as st
from utils.llm import score_risk


def _risk_colour(level: str) -> str:
    return {"Low": "#00e676", "Medium": "#ffab40", "High": "#ff5252", "Critical": "#ff1744"}.get(level, "#7090b0")


def _priority_badge(p: str) -> str:
    cls = {"Immediate": "badge-high", "Short-term": "badge-medium", "Long-term": "badge-low"}.get(p, "badge-low")
    return f"<span class='{cls}'>{p}</span>"


def render():
    st.markdown("<h1 style='color:#00d4ff;'>⚠️ Risk Scorer</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7090b0;font-size:.85rem;'>Get a multi-dimensional risk score for your AI system across technical, ethical, legal, operational, and reputational dimensions.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        system_desc = st.text_area(
            "Describe your AI system",
            height=160,
            placeholder="e.g. A machine learning model that scores loan applications using applicant financial history, employment data, and demographic information to predict default risk...",
        )
        deployment = st.selectbox("Deployment Context", [
            "Customer-facing product",
            "Internal tool",
            "Automated decision-making (no human review)",
            "Decision-support (human in the loop)",
            "Research / experimental",
            "Third-party integration",
        ])

    with col2:
        data_options = [
            "Personal / PII data",
            "Financial data",
            "Health / medical data",
            "Biometric data",
            "Location data",
            "Behavioural data",
            "Publicly available data",
            "Synthetic / anonymised data",
        ]
        data_types = st.multiselect("Data Types Processed", data_options, default=["Personal / PII data"])
        industry = st.selectbox("Industry Sector", [
            "Financial Services", "Healthcare", "Retail / E-commerce",
            "Government / Public Sector", "Education", "HR / Recruitment",
            "Legal", "Insurance", "Technology", "Other",
        ])

    if st.button("🔬 Score Risk", use_container_width=True):
        if not st.session_state.get("api_key"):
            st.error("Please enter your OpenAI API key in the sidebar.")
            return
        if not system_desc.strip():
            st.warning("Please describe your AI system.")
            return

        context = f"{deployment} — Industry: {industry}"
        with st.spinner("Calculating multi-dimensional risk profile..."):
            try:
                result = score_risk(system_desc, context, data_types)
                st.session_state["risk_result"] = result
            except Exception as e:
                st.error(f"Risk scoring failed: {e}")
                return

    result = st.session_state.get("risk_result")
    if not result:
        return

    st.markdown("---")
    st.markdown("<h3 style='color:#e0e6f0;'>Risk Assessment Results</h3>", unsafe_allow_html=True)

    # ── Composite Score ──────────────────────────────────────────────────────
    score = result.get("composite_score", 0)
    level = result.get("risk_level", "Unknown")
    rc    = _risk_colour(level)

    head1, head2, head3 = st.columns(3)
    with head1:
        st.markdown(f"""
        <div class='gov-card' style='text-align:center;'>
            <div style='font-size:2.8rem;font-weight:700;font-family:"IBM Plex Mono",monospace;color:{rc};'>{score}</div>
            <div style='color:#7090b0;font-size:.8rem;'>Composite Risk Score</div>
        </div>""", unsafe_allow_html=True)
    with head2:
        st.markdown(f"""
        <div class='gov-card' style='text-align:center;padding-top:1.5rem;'>
            <div style='font-size:1.5rem;font-weight:700;font-family:"IBM Plex Mono",monospace;color:{rc};'>{level}</div>
            <div style='color:#7090b0;font-size:.8rem;margin-top:.3rem;'>Risk Level</div>
        </div>""", unsafe_allow_html=True)
    with head3:
        eu_class = result.get("eu_ai_act_classification", "—")
        st.markdown(f"""
        <div class='gov-card' style='text-align:center;padding-top:1.5rem;'>
            <div style='font-size:1rem;font-weight:600;color:#e0e6f0;'>{eu_class}</div>
            <div style='color:#7090b0;font-size:.8rem;margin-top:.3rem;'>EU AI Act Classification</div>
        </div>""", unsafe_allow_html=True)

    # ── Summary ──────────────────────────────────────────────────────────────
    summary = result.get("summary", "")
    st.markdown(f"""
    <div class='gov-card gov-card-accent' style='margin-top:1rem;'>
        <div style='font-size:.7rem;color:#7090b0;font-family:"IBM Plex Mono",monospace;margin-bottom:.5rem;'>RISK SUMMARY</div>
        <p style='color:#e0e6f0;margin:0;line-height:1.7;'>{summary}</p>
    </div>""", unsafe_allow_html=True)

    # ── Dimensions ───────────────────────────────────────────────────────────
    st.markdown("<h4 style='color:#e0e6f0;font-size:.9rem;margin-top:1.5rem;'>Risk Dimensions</h4>", unsafe_allow_html=True)
    dims = result.get("dimensions", {})
    dim_labels = {
        "technical_risk": "⚙️ Technical",
        "ethical_risk": "⚖️ Ethical",
        "legal_risk": "📜 Legal",
        "operational_risk": "🔧 Operational",
        "reputational_risk": "🌐 Reputational",
    }
    for key, label in dim_labels.items():
        dim = dims.get(key, {})
        ds  = dim.get("score", 0)
        dr  = dim.get("rationale", "")
        dc  = _risk_colour("Critical" if ds >= 75 else "High" if ds >= 50 else "Medium" if ds >= 25 else "Low")
        with st.expander(f"{label} — Score: {ds}/100"):
            st.markdown(f"""
            <div style='margin-bottom:.5rem;'>
                <span style='color:{dc};font-size:1.5rem;font-weight:700;font-family:"IBM Plex Mono",monospace;'>{ds}</span>
                <span style='color:#7090b0;font-size:.8rem;'>/100</span>
            </div>""", unsafe_allow_html=True)
            st.progress(ds / 100)
            st.markdown(f"<p style='color:#aabbcc;font-size:.85rem;margin-top:.5rem;'>{dr}</p>", unsafe_allow_html=True)

    # ── Red Flags ────────────────────────────────────────────────────────────
    red_flags = result.get("red_flags", [])
    if red_flags:
        st.markdown("<h4 style='color:#ff5252;font-size:.9rem;margin-top:1.5rem;'>🚩 Red Flags</h4>", unsafe_allow_html=True)
        for rf in red_flags:
            st.markdown(f"<div class='gov-card' style='padding:.7rem 1rem;margin-bottom:.4rem;border-left:3px solid #ff5252;'><span style='color:#ffcdd2;font-size:.85rem;'>⚠ {rf}</span></div>", unsafe_allow_html=True)

    # ── Mitigations ──────────────────────────────────────────────────────────
    mitigations = result.get("mitigations", [])
    if mitigations:
        st.markdown("<h4 style='color:#e0e6f0;font-size:.9rem;margin-top:1.5rem;'>🛡️ Recommended Mitigations</h4>", unsafe_allow_html=True)
        for m in mitigations:
            st.markdown(f"""
            <div class='gov-card' style='padding:.8rem 1rem;margin-bottom:.4rem;display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                    <span style='color:#ffab40;font-size:.8rem;font-weight:600;'>{m.get('risk','')}</span>
                    <br><span style='color:#e0e6f0;font-size:.85rem;'>{m.get('action','')}</span>
                </div>
                <div style='margin-left:1rem;white-space:nowrap;'>{_priority_badge(m.get('priority',''))}</div>
            </div>""", unsafe_allow_html=True)
