"""pages/dashboard.py — Overview dashboard."""

import streamlit as st


def render():
    st.markdown("""
    <h1 style='color:#00d4ff;margin-bottom:.25rem;'>AI Governance Assistant</h1>
    <p style='color:#7090b0;font-family:"IBM Plex Mono",monospace;font-size:.85rem;'>
    Enterprise AI Risk & Compliance Platform · Powered by OpenAI + LangChain
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ── KPI Row ──────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    tiles = [
        ("4", "Policies Analysed"),
        ("73", "Avg Compliance Score"),
        ("12", "Open Risk Items"),
        ("3", "Audits Generated"),
    ]
    for col, (val, lbl) in zip([c1, c2, c3, c4], tiles):
        with col:
            st.markdown(f"""
            <div class='metric-tile'>
                <div class='val'>{val}</div>
                <div class='lbl'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two-column layout ────────────────────────────────────────────────────
    left, right = st.columns([3, 2])

    with left:
        st.markdown("<h3 style='color:#e0e6f0;font-size:1rem;'>📌 Getting Started</h3>", unsafe_allow_html=True)

        steps = [
            ("1", "Enter your OpenAI API key in the sidebar", "Securely stored in session state only"),
            ("2", "Policy Validator — paste an AI policy or use cases document for instant compliance analysis", "Checks against EU AI Act, NIST AI RMF, ISO 42001 & GDPR"),
            ("3", "Risk Scorer — describe your AI system to get a multi-dimensional risk score", "5-dimension scoring with actionable mitigations"),
            ("4", "Compliance Workflow — generate a prioritised action plan for your organisation", "Phase-gated tasks with owner assignments"),
            ("5", "Audit Summaries — upload evidence to produce a structured audit report", "Exportable findings with remediation deadlines"),
        ]

        for num, title, sub in steps:
            st.markdown(f"""
            <div class='gov-card gov-card-accent' style='padding:1rem;margin-bottom:.6rem;'>
                <span style='color:#00d4ff;font-family:"IBM Plex Mono",monospace;font-weight:700;font-size:.9rem;'>STEP {num}</span>
                <span style='color:#e0e6f0;margin-left:.75rem;font-size:.9rem;'>{title}</span>
                <div style='color:#7090b0;font-size:.78rem;margin-top:.3rem;padding-left:3.5rem;'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    with right:
        st.markdown("<h3 style='color:#e0e6f0;font-size:1rem;'>📐 Supported Frameworks</h3>", unsafe_allow_html=True)

        frameworks = [
            ("EU AI Act", "Risk-based regulation for AI systems in the EU", "dot-red"),
            ("NIST AI RMF", "US National Institute framework for AI risk management", "dot-green"),
            ("ISO/IEC 42001", "International AI management system standard", "dot-green"),
            ("GDPR", "Data protection and privacy regulation", "dot-orange"),
            ("SOC 2", "Service organisation security & availability controls", "dot-green"),
        ]

        for name, desc, dot in frameworks:
            st.markdown(f"""
            <div class='gov-card' style='padding:.8rem 1rem;margin-bottom:.5rem;'>
                <span class='{dot}'></span>
                <span style='color:#e0e6f0;font-weight:600;font-size:.85rem;'>{name}</span>
                <div style='color:#7090b0;font-size:.75rem;margin-top:.3rem;margin-left:1rem;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:.75rem;color:#506070;text-align:center;font-family:"IBM Plex Mono",monospace;'>
    ⚠️ This tool assists governance analysis. Always consult qualified legal and compliance professionals for binding decisions.
    </div>""", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:.75rem;color:#506070;text-align:center;font-family:"IBM Plex Mono",monospace;margin-top:8px;'>
    Built by <a href='https://www.linkedin.com/in/absahai/' style='color:#00d4ff;'>Abhinav</a> - &copy; 2026 - MIT Licence
    </div>""", unsafe_allow_html=True)
