# ─────────────────────────────────────────────────────────────
# AI Governance Assistant
# Author: Abhinav Sahai | linkedin.com/in/absahai
# GitHub: github.com/abhisahai/ai-governance-assistant
# Licence: MIT © 2026
# ─────────────────────────────────────────────────────────────

"""
pages/compliance_agent.py
Multi-step Compliance Agent — powered by LangChain AgentExecutor + GPT-4o.

The agent autonomously decides tool call order, executes all 5 tools in sequence,
and synthesises a unified governance report without user intervention between steps.
"""

import streamlit as st
from utils.agent import run_agent

SAMPLE_INPUT = (
    "We are deploying a machine learning model that scores loan applications "
    "using applicants' financial history, employment data, credit scores, and "
    "demographic information to predict default risk. The system runs fully "
    "automated with no human review of individual decisions. It is customer-facing "
    "and processes personal data of EU residents. We operate in the UK financial "
    "services sector and are subject to FCA regulation."
)


def _rating_colour(rating: str) -> str:
    return {"Green": "#00e676", "Amber": "#ffab40", "Red": "#ff5252"}.get(rating, "#7090b0")


def _score_colour(score: int) -> str:
    if score >= 70: return "#00e676"
    if score >= 40: return "#ffab40"
    return "#ff5252"


def _render_step(number: str, label: str, status: str):
    colours = {
        "complete": ("#00e676", "✓", "#0a2e1a"),
        "running":  ("#00d4ff", "⟳", "#0a1e3a"),
        "pending":  ("#506070", "○", "#0d1a30"),
    }
    c, icon, bg = colours.get(status, colours["pending"])
    st.markdown(f"""
    <div style='background:{bg};border:1px solid {c};border-radius:6px;
                padding:8px 12px;margin-bottom:6px;display:flex;
                align-items:center;gap:10px;'>
        <span style='color:{c};font-size:14px;font-family:"IBM Plex Mono",monospace;
                     font-weight:700;'>{icon}</span>
        <span style='color:#e0e6f0;font-size:12px;'>
            <b style='font-family:"IBM Plex Mono",monospace;color:{c};'>
                Tool {number}</b> — {label}
        </span>
    </div>""", unsafe_allow_html=True)


def render():
    st.markdown("<h1 style='color:#00d4ff;'>🤖 Compliance Agent</h1>",
                unsafe_allow_html=True)
    st.markdown("""
    <p style='color:#7090b0;font-size:.85rem;'>
    Describe your AI system in plain English. The agent autonomously runs all
    five assessment tools in sequence — risk scoring, EU AI Act classification,
    policy gap analysis, compliance planning, and report synthesis — without
    requiring any input between steps.
    </p>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:#0a1220;border:1px solid #1e3a5f;border-radius:8px;
                padding:10px 14px;margin-bottom:1rem;font-size:.78rem;
                color:#7090b0;font-family:"IBM Plex Mono",monospace;'>
        ⚙ Powered by&nbsp;
        <span style='color:#00d4ff;'>LangChain AgentExecutor</span>
        &nbsp;+&nbsp;
        <span style='color:#00d4ff;'>GPT-4o</span>
        &nbsp;·&nbsp;
        <span style='color:#aabbcc;'>5 tools · ConversationBufferMemory</span>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── Input ────────────────────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            "<div style='font-size:.75rem;color:#7090b0;margin-bottom:4px;'>"
            "Uses the OpenAI API key and model configured in the sidebar.</div>",
            unsafe_allow_html=True
        )
        key_status = "● Connected" if st.session_state.get("api_key") else "● No API key — enter it in the sidebar"
        key_colour = "#00e676" if st.session_state.get("api_key") else "#ffab40"
        st.markdown(
            f"<span style='font-size:.75rem;color:{key_colour};'>{key_status}</span>",
            unsafe_allow_html=True
        )
    with col2:
        if st.button("Load sample", use_container_width=True):
            st.session_state["agent_input"] = SAMPLE_INPUT

    system_desc = st.text_area(
        "Describe your AI system",
        value=st.session_state.get("agent_input", ""),
        height=160,
        placeholder=(
            "Describe your AI system — what it does, who it affects, "
            "what data it processes, how decisions are made, and the "
            "deployment context..."
        ),
    )

    # ── Agent tool pipeline diagram ───────────────────────────────────────────
    st.markdown("""
    <div style='background:#0d1a30;border:1px solid #1e3a5f;border-radius:8px;
                padding:12px 16px;margin:1rem 0;'>
        <div style='font-size:.7rem;color:#7090b0;font-family:"IBM Plex Mono",monospace;
                    margin-bottom:10px;'>AGENT TOOL EXECUTION PIPELINE</div>
        <div style='display:flex;align-items:center;gap:6px;flex-wrap:wrap;'>
            <span style='background:#0a1e3a;border:1px solid #00d4ff;color:#00d4ff;
                         font-size:.7rem;padding:3px 10px;border-radius:12px;
                         font-family:"IBM Plex Mono",monospace;'>1 · risk_score_tool</span>
            <span style='color:#1e3a5f;'>→</span>
            <span style='background:#0a1e3a;border:1px solid #00d4ff;color:#00d4ff;
                         font-size:.7rem;padding:3px 10px;border-radius:12px;
                         font-family:"IBM Plex Mono",monospace;'>2 · eu_ai_act_tool</span>
            <span style='color:#1e3a5f;'>→</span>
            <span style='background:#0a1e3a;border:1px solid #00d4ff;color:#00d4ff;
                         font-size:.7rem;padding:3px 10px;border-radius:12px;
                         font-family:"IBM Plex Mono",monospace;'>3 · policy_gap_tool</span>
            <span style='color:#1e3a5f;'>→</span>
            <span style='background:#0a1e3a;border:1px solid #00d4ff;color:#00d4ff;
                         font-size:.7rem;padding:3px 10px;border-radius:12px;
                         font-family:"IBM Plex Mono",monospace;'>4 · compliance_plan_tool</span>
            <span style='color:#1e3a5f;'>→</span>
            <span style='background:#0a2e1a;border:1px solid #00e676;color:#00e676;
                         font-size:.7rem;padding:3px 10px;border-radius:12px;
                         font-family:"IBM Plex Mono",monospace;'>5 · governance_report_tool</span>
        </div>
    </div>""", unsafe_allow_html=True)

    run = st.button("🚀 Run Compliance Agent", use_container_width=True)

    if run:
        if not st.session_state.get("api_key"):
            st.error("Please enter your OpenAI API key above.")
            return
        if not system_desc.strip():
            st.warning("Please describe your AI system.")
            return

        # ── Live progress tracker ─────────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            "<h3 style='color:#e0e6f0;font-size:1rem;'>Agent running...</h3>",
            unsafe_allow_html=True
        )

        steps = [
            ("1", "risk_score_tool — multi-dimension risk scoring"),
            ("2", "eu_ai_act_tool — regulatory classification"),
            ("3", "policy_gap_tool — gap identification"),
            ("4", "compliance_plan_tool — action plan generation"),
            ("5", "governance_report_tool — report synthesis"),
        ]

        step_placeholder = st.empty()

        def render_steps(current: int):
            with step_placeholder.container():
                for i, (num, label) in enumerate(steps):
                    if i < current:
                        _render_step(num, label, "complete")
                    elif i == current:
                        _render_step(num, label, "running")
                    else:
                        _render_step(num, label, "pending")

        render_steps(0)

        # ── Monkey-patch session state writes to update progress ──────────────
        original_setitem = type(st.session_state).__setitem__
        step_map = {
            "agent_risk":   1,
            "agent_euact":  2,
            "agent_policy": 3,
            "agent_plan":   4,
            "agent_report": 5,
        }

        def _tracking_setitem(self, key, value):
            original_setitem(self, key, value)
            if key in step_map:
                render_steps(step_map[key])

        type(st.session_state).__setitem__ = _tracking_setitem

        try:
            with st.spinner("Agent reasoning... this takes ~30–60 seconds"):
                run_agent(system_desc)
            render_steps(5)
        except Exception as e:
            st.error(f"Agent error: {e}")
            return
        finally:
            type(st.session_state).__setitem__ = original_setitem

    # ── Results ───────────────────────────────────────────────────────────────
    report = st.session_state.get("agent_report")
    if not report:
        return

    st.markdown("---")
    st.markdown(
        "<h3 style='color:#e0e6f0;'>Unified Governance Report</h3>",
        unsafe_allow_html=True
    )

    # Header scores
    gov_score  = report.get("overall_governance_score", 0)
    rating     = report.get("governance_rating", "Amber")
    audit_score = report.get("audit_readiness_score", 0)
    exposure   = report.get("regulatory_exposure", "Unknown")
    rc         = _rating_colour(rating)
    exposure_c = {"Low": "#00e676", "Medium": "#ffab40",
                  "High": "#ff5252", "Critical": "#ff1744"}.get(exposure, "#7090b0")

    h1, h2, h3, h4 = st.columns(4)
    for col, val, lbl, colour in [
        (h1, gov_score,   "Governance score",    _score_colour(gov_score)),
        (h2, rating,      "Governance rating",   rc),
        (h3, audit_score, "Audit readiness",     _score_colour(audit_score)),
        (h4, exposure,    "Regulatory exposure", exposure_c),
    ]:
        with col:
            st.markdown(f"""
            <div style='background:#0d1a30;border:1px solid #1e3a5f;border-radius:8px;
                        padding:1rem;text-align:center;'>
                <div style='font-size:1.6rem;font-weight:700;
                            font-family:"IBM Plex Mono",monospace;color:{colour};'>{val}</div>
                <div style='font-size:.75rem;color:#7090b0;margin-top:4px;'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    # Executive summary
    summary = report.get("executive_summary", "")
    st.markdown(f"""
    <div style='background:#0d1a30;border:1px solid #1e3a5f;border-left:3px solid #00d4ff;
                border-radius:0 8px 8px 0;padding:1rem 1.25rem;margin-top:1rem;'>
        <div style='font-size:.7rem;color:#7090b0;font-family:"IBM Plex Mono",monospace;
                    margin-bottom:.5rem;'>EXECUTIVE SUMMARY</div>
        <p style='color:#e0e6f0;margin:0;line-height:1.7;font-size:.88rem;'>{summary}</p>
    </div>""", unsafe_allow_html=True)

    # Recommendation
    rec = report.get("recommendation", "")
    st.markdown(f"""
    <div style='background:#0a1e3a;border:1px solid #00d4ff;border-radius:8px;
                padding:.9rem 1.25rem;margin-top:.8rem;'>
        <span style='font-size:.7rem;color:#7090b0;font-family:"IBM Plex Mono",monospace;'>
            LEADERSHIP RECOMMENDATION&nbsp;&nbsp;</span>
        <span style='color:#00d4ff;font-size:.88rem;'>{rec}</span>
    </div>""", unsafe_allow_html=True)

    # Top risks + actions
    left, right = st.columns(2)
    with left:
        risks = report.get("top_3_risks", [])
        st.markdown(
            "<h4 style='color:#ff5252;font-size:.9rem;margin-top:1.2rem;'>"
            "🚩 Top 3 risks</h4>",
            unsafe_allow_html=True
        )
        for r in risks:
            st.markdown(
                f"<div style='background:#1a0808;border-left:2px solid #ff5252;"
                f"border-radius:0 6px 6px 0;padding:8px 12px;margin-bottom:6px;"
                f"font-size:.83rem;color:#ffcdd2;'>⚠ {r}</div>",
                unsafe_allow_html=True
            )

    with right:
        actions = report.get("top_3_immediate_actions", [])
        st.markdown(
            "<h4 style='color:#00e676;font-size:.9rem;margin-top:1.2rem;'>"
            "⚡ Top 3 immediate actions</h4>",
            unsafe_allow_html=True
        )
        for i, a in enumerate(actions, 1):
            st.markdown(
                f"<div style='background:#0a2e1a;border-left:2px solid #00e676;"
                f"border-radius:0 6px 6px 0;padding:8px 12px;margin-bottom:6px;"
                f"font-size:.83rem;color:#e0e6f0;'>"
                f"<span style='color:#00e676;font-weight:700;'>{i}.</span> {a}</div>",
                unsafe_allow_html=True
            )

    # Detailed tool results in expanders
    st.markdown("---")
    st.markdown(
        "<h4 style='color:#e0e6f0;font-size:.9rem;'>Detailed assessment results</h4>",
        unsafe_allow_html=True
    )

    risk = st.session_state.get("agent_risk", {})
    if risk:
        with st.expander("⚠️ Risk Score — full dimension breakdown"):
            dims = risk.get("dimensions", {})
            dim_labels = {
                "technical_risk": "⚙️ Technical",
                "ethical_risk": "⚖️ Ethical",
                "legal_risk": "📜 Legal",
                "operational_risk": "🔧 Operational",
                "reputational_risk": "🌐 Reputational",
            }
            for key, label in dim_labels.items():
                d = dims.get(key, {})
                s = d.get("score", 0)
                c = _score_colour(s)
                st.markdown(
                    f"<div style='margin-bottom:.6rem;'>"
                    f"<span style='font-size:.8rem;color:#aabbcc;'>{label}</span>"
                    f"<span style='float:right;color:{c};font-weight:700;"
                    f"font-family:\"IBM Plex Mono\",monospace;'>{s}/100</span></div>",
                    unsafe_allow_html=True
                )
                st.progress(s / 100)
                st.markdown(
                    f"<p style='font-size:.78rem;color:#7090b0;margin-top:2px;'>"
                    f"{d.get('rationale','')}</p>",
                    unsafe_allow_html=True
                )
            if risk.get("red_flags"):
                st.markdown(
                    "<div style='font-size:.8rem;color:#ff5252;margin-top:.5rem;'>"
                    "🚩 Red flags</div>",
                    unsafe_allow_html=True
                )
                for rf in risk["red_flags"]:
                    st.markdown(
                        f"<div style='font-size:.8rem;color:#ffcdd2;margin-bottom:3px;'>"
                        f"• {rf}</div>",
                        unsafe_allow_html=True
                    )

    euact = st.session_state.get("agent_euact", {})
    if euact:
        with st.expander("🇪🇺 EU AI Act — classification & obligations"):
            st.markdown(
                f"<b style='color:#00d4ff;'>Risk tier:</b> "
                f"<span style='color:#e0e6f0;'>{euact.get('risk_tier')}</span>&nbsp;&nbsp;"
                f"<b style='color:#00d4ff;'>Classification:</b> "
                f"<span style='color:#e0e6f0;'>{euact.get('annex_classification')}</span>&nbsp;&nbsp;"
                f"<b style='color:#00d4ff;'>Conformity required:</b> "
                f"<span style='color:#ffab40;'>{euact.get('conformity_assessment_required')}</span>",
                unsafe_allow_html=True
            )
            if euact.get("applicable_articles"):
                st.markdown(
                    "<div style='font-size:.8rem;color:#7090b0;margin-top:.8rem;"
                    "margin-bottom:.4rem;'>Applicable articles</div>",
                    unsafe_allow_html=True
                )
                for a in euact["applicable_articles"]:
                    st.markdown(
                        f"<div style='font-size:.8rem;color:#aabbcc;margin-bottom:3px;'>"
                        f"• {a}</div>",
                        unsafe_allow_html=True
                    )
            if euact.get("key_obligations"):
                st.markdown(
                    "<div style='font-size:.8rem;color:#7090b0;margin-top:.8rem;"
                    "margin-bottom:.4rem;'>Key obligations</div>",
                    unsafe_allow_html=True
                )
                for o in euact["key_obligations"]:
                    st.markdown(
                        f"<div style='font-size:.8rem;color:#aabbcc;margin-bottom:3px;'>"
                        f"• {o}</div>",
                        unsafe_allow_html=True
                    )

    policy = st.session_state.get("agent_policy", {})
    if policy:
        with st.expander("📋 Policy gaps — critical findings"):
            for gap in policy.get("critical_gaps", []):
                sev = gap.get("severity", "Medium")
                sc  = {"High": "#ff5252", "Medium": "#ffab40", "Low": "#00e676"}.get(sev, "#7090b0")
                st.markdown(
                    f"<div style='background:#0a1220;border-radius:6px;padding:10px 12px;"
                    f"margin-bottom:8px;border-left:2px solid {sc};'>"
                    f"<span style='color:{sc};font-size:.75rem;font-weight:700;'>{sev}</span>"
                    f"<span style='color:#7090b0;font-size:.75rem;'> · {gap.get('framework')}</span>"
                    f"<div style='color:#e0e6f0;font-size:.83rem;margin-top:4px;'>{gap.get('gap')}</div>"
                    f"<div style='color:#00d4ff;font-size:.78rem;margin-top:4px;'>"
                    f"→ {gap.get('recommendation')}</div></div>",
                    unsafe_allow_html=True
                )

    plan = st.session_state.get("agent_plan", {})
    if plan:
        with st.expander("✅ Compliance plan — all actions"):
            for section, label, colour in [
                ("immediate_actions", "Immediate actions", "#ff5252"),
                ("short_term_actions", "Short-term actions", "#ffab40"),
                ("long_term_actions", "Long-term actions", "#00e676"),
            ]:
                tasks = plan.get(section, [])
                if tasks:
                    st.markdown(
                        f"<div style='font-size:.8rem;color:{colour};font-weight:700;"
                        f"margin-top:.8rem;margin-bottom:.4rem;'>{label}</div>",
                        unsafe_allow_html=True
                    )
                    for t in tasks:
                        st.markdown(
                            f"<div style='background:#0a1220;border-radius:6px;"
                            f"padding:8px 12px;margin-bottom:6px;font-size:.8rem;'>"
                            f"<span style='color:#e0e6f0;'>{t.get('task')}</span>"
                            f"<span style='color:#7090b0;'> · {t.get('owner')} · "
                            f"{t.get('framework')} · Due: {t.get('deadline')}</span></div>",
                            unsafe_allow_html=True
                        )
