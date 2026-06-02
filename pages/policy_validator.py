"""pages/policy_validator.py — AI Policy Validation feature."""

import streamlit as st
from utils.llm import validate_policy

SAMPLE_POLICY = """AI Usage Policy v1.2 — Acme Corp

Purpose: This policy governs the ethical and responsible use of AI systems across Acme Corp.

Scope: All employees, contractors, and third-party vendors deploying or using AI tools.

1. Prohibited Uses
   - AI shall not be used to make final decisions in hiring, termination, or performance reviews without human oversight.
   - Facial recognition is prohibited in employee monitoring.

2. Data Handling
   - Personal data used in AI models must be minimised and anonymised where possible.
   - Retention periods for training data are limited to 24 months.

3. Transparency
   - Users must be notified when interacting with an AI system.
   - Model cards must be maintained for all internally developed models.

4. Accountability
   - Each AI project requires a designated AI Responsible Owner.
   - Incident reporting procedures must be followed within 72 hours of detecting bias or harm.
"""


def _severity_badge(sev: str) -> str:
    cls = {"Low": "badge-low", "Medium": "badge-medium", "High": "badge-high"}.get(sev, "badge-low")
    return f"<span class='{cls}'>{sev}</span>"


def render():
    st.markdown("<h1 style='color:#00d4ff;'>📋 Policy Validator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7090b0;font-size:.85rem;'>Analyse AI policy documents against major governance frameworks and receive actionable findings.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns([3, 1])
    with col1:
        policy_type = st.selectbox("Policy Type", [
            "AI Usage Policy", "Data Governance Policy", "Model Development Policy",
            "Vendor AI Policy", "Ethics & Fairness Policy", "Other"
        ])
    with col2:
        if st.button("Load Sample", use_container_width=True):
            st.session_state["policy_text"] = SAMPLE_POLICY

    policy_text = st.text_area(
        "Paste your policy document",
        value=st.session_state.get("policy_text", ""),
        height=280,
        placeholder="Paste your AI policy document here...",
    )

    if st.button("🔍 Validate Policy", use_container_width=True):
        if not st.session_state.get("api_key"):
            st.error("Please enter your OpenAI API key in the sidebar.")
            return
        if not policy_text.strip():
            st.warning("Please paste a policy document to validate.")
            return

        with st.spinner("Analysing policy against EU AI Act, NIST AI RMF, ISO 42001 & GDPR..."):
            try:
                result = validate_policy(policy_text, policy_type)
                st.session_state["policy_result"] = result
            except Exception as e:
                st.error(f"Analysis failed: {e}")
                return

    result = st.session_state.get("policy_result")
    if not result:
        return

    st.markdown("---")
    st.markdown("<h3 style='color:#e0e6f0;'>Analysis Results</h3>", unsafe_allow_html=True)

    # ── Score + Risk Tier ────────────────────────────────────────────────────
    m1, m2 = st.columns(2)
    score = result.get("overall_score", 0)
    tier  = result.get("risk_tier", "Unknown")
    tier_colors = {"Minimal": "#00e676", "Limited": "#ffab40", "High": "#ff5252", "Unacceptable": "#ff1744"}
    t_color = tier_colors.get(tier, "#7090b0")

    with m1:
        st.markdown(f"""
        <div class='gov-card' style='text-align:center;'>
            <div style='font-size:3rem;font-weight:700;font-family:"IBM Plex Mono",monospace;color:#00d4ff;'>{score}</div>
            <div style='color:#7090b0;font-size:.8rem;'>Overall Compliance Score</div>
            <div style='margin-top:.5rem;'>
        """, unsafe_allow_html=True)
        st.progress(score / 100)
        st.markdown("</div></div>", unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class='gov-card' style='text-align:center;padding-top:1.8rem;'>
            <div style='font-size:1.6rem;font-weight:700;font-family:"IBM Plex Mono",monospace;color:{t_color};'>{tier}</div>
            <div style='color:#7090b0;font-size:.8rem;margin-top:.3rem;'>EU AI Act Risk Tier</div>
        </div>""", unsafe_allow_html=True)

    # ── Framework Coverage ───────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#e0e6f0;font-size:.9rem;'>Framework Coverage</h4>", unsafe_allow_html=True)
    fc = result.get("framework_coverage", {})
    for fw, pct in fc.items():
        c_a, c_b = st.columns([1, 4])
        with c_a:
            st.markdown(f"<span style='font-size:.8rem;color:#aabbcc;font-family:\"IBM Plex Mono\",monospace;'>{fw}</span>", unsafe_allow_html=True)
        with c_b:
            st.progress(int(pct) / 100)

    # ── Executive Summary ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    summary = result.get("executive_summary", "")
    st.markdown(f"""
    <div class='gov-card gov-card-accent'>
        <div style='font-size:.7rem;color:#7090b0;font-family:"IBM Plex Mono",monospace;margin-bottom:.5rem;'>EXECUTIVE SUMMARY</div>
        <p style='color:#e0e6f0;margin:0;line-height:1.7;'>{summary}</p>
    </div>""", unsafe_allow_html=True)

    # ── Findings ─────────────────────────────────────────────────────────────
    findings = result.get("findings", [])
    if findings:
        st.markdown("<h4 style='color:#e0e6f0;font-size:.9rem;margin-top:1.5rem;'>Findings</h4>", unsafe_allow_html=True)
        for f in findings:
            with st.expander(f"[{f.get('severity','?')}] {f.get('category','Finding')} — {f.get('description','')[:60]}..."):
                st.markdown(f"""
                <div style='line-height:1.8;'>
                    <b style='color:#7090b0;'>Severity:</b> {_severity_badge(f.get('severity',''))}
                    <br><b style='color:#7090b0;'>Category:</b> <span style='color:#e0e6f0;'>{f.get('category','')}</span>
                    <br><b style='color:#7090b0;'>Description:</b> <span style='color:#e0e6f0;'>{f.get('description','')}</span>
                    <br><b style='color:#7090b0;'>Recommendation:</b> <span style='color:#00d4ff;'>{f.get('recommendation','')}</span>
                </div>""", unsafe_allow_html=True)

    # ── Strengths & Gaps ─────────────────────────────────────────────────────
    sg1, sg2 = st.columns(2)
    with sg1:
        strengths = result.get("strengths", [])
        st.markdown("<h4 style='color:#00e676;font-size:.9rem;'>✅ Strengths</h4>", unsafe_allow_html=True)
        for s in strengths:
            st.markdown(f"<div style='color:#e0e6f0;font-size:.85rem;margin-bottom:.3rem;'>• {s}</div>", unsafe_allow_html=True)

    with sg2:
        gaps = result.get("gaps", [])
        st.markdown("<h4 style='color:#ff5252;font-size:.9rem;'>❌ Gaps</h4>", unsafe_allow_html=True)
        for g in gaps:
            st.markdown(f"<div style='color:#e0e6f0;font-size:.85rem;margin-bottom:.3rem;'>• {g}</div>", unsafe_allow_html=True)
