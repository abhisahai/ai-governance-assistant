"""pages/compliance_workflow.py — Compliance Action Plan Generator."""

import streamlit as st
from utils.llm import generate_compliance_workflow

PRIORITY_COLORS = {"Critical": "#ff5252", "High": "#ff9800", "Medium": "#ffeb3b", "Low": "#7090b0"}
OWNER_ICONS = {"Legal": "⚖️", "Engineering": "⚙️", "Data Science": "📊", "CISO": "🔐", "HR": "👥", "Compliance": "📋"}


def _priority_badge(p: str) -> str:
    cls = {"Critical": "badge-high", "High": "badge-high", "Medium": "badge-medium", "Low": "badge-low"}.get(p, "badge-low")
    return f"<span class='{cls}'>{p}</span>"


def render():
    st.markdown("<h1 style='color:#00d4ff;'>✅ Compliance Workflow</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7090b0;font-size:.85rem;'>Generate a phase-gated compliance action plan tailored to your organisation and target frameworks.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        org_name = st.text_input("Organisation Name", placeholder="Acme Corp")
        ai_use_cases = st.text_area(
            "AI Use Cases / Systems",
            height=120,
            placeholder="e.g. Customer churn prediction model, automated invoice processing, HR candidate screening tool, fraud detection system...",
        )
    with col2:
        frameworks = st.multiselect(
            "Target Compliance Frameworks",
            ["EU AI Act", "NIST AI RMF", "ISO 42001", "GDPR", "SOC 2"],
            default=["EU AI Act", "NIST AI RMF"],
        )
        maturity = st.select_slider(
            "Current AI Governance Maturity",
            options=["Initial", "Developing", "Defined", "Managed", "Optimising"],
            value="Developing",
        )

    if st.button("🗺️ Generate Compliance Workflow", use_container_width=True):
        if not st.session_state.get("api_key"):
            st.error("Please enter your OpenAI API key in the sidebar.")
            return
        if not org_name.strip() or not ai_use_cases.strip():
            st.warning("Please fill in organisation name and AI use cases.")
            return
        if not frameworks:
            st.warning("Please select at least one compliance framework.")
            return

        with st.spinner("Generating your personalised compliance roadmap..."):
            try:
                result = generate_compliance_workflow(org_name, ai_use_cases, frameworks, maturity)
                st.session_state["workflow_result"] = result
            except Exception as e:
                st.error(f"Workflow generation failed: {e}")
                return

    result = st.session_state.get("workflow_result")
    if not result:
        return

    st.markdown("---")
    st.markdown(f"<h3 style='color:#e0e6f0;'>Compliance Roadmap — {result.get('project_name','')}</h3>", unsafe_allow_html=True)

    # ── Summary Stats ────────────────────────────────────────────────────────
    s1, s2 = st.columns(2)
    with s1:
        st.markdown(f"""
        <div class='metric-tile'>
            <div class='val'>{result.get('total_tasks','—')}</div>
            <div class='lbl'>Total Tasks</div>
        </div>""", unsafe_allow_html=True)
    with s2:
        st.markdown(f"""
        <div class='metric-tile'>
            <div class='val'>{result.get('estimated_weeks','—')}</div>
            <div class='lbl'>Estimated Weeks</div>
        </div>""", unsafe_allow_html=True)

    # ── Quick Wins ───────────────────────────────────────────────────────────
    quick_wins = result.get("quick_wins", [])
    if quick_wins:
        st.markdown("<h4 style='color:#00e676;font-size:.9rem;margin-top:1.2rem;'>⚡ Quick Wins</h4>", unsafe_allow_html=True)
        for qw in quick_wins:
            st.markdown(f"<div style='color:#e0e6f0;font-size:.85rem;margin-bottom:.3rem;'>• {qw}</div>", unsafe_allow_html=True)

    # ── Phases ───────────────────────────────────────────────────────────────
    phases = result.get("phases", [])
    for phase in phases:
        phase_name = phase.get("phase", "Phase")
        duration   = phase.get("duration_weeks", "?")
        tasks      = phase.get("tasks", [])

        st.markdown(f"""
        <div style='margin-top:1.5rem;margin-bottom:.6rem;'>
            <span style='font-family:"IBM Plex Mono",monospace;font-size:.9rem;font-weight:700;color:#00d4ff;'>{phase_name}</span>
            <span style='color:#7090b0;font-size:.8rem;margin-left:.8rem;'>~{duration} weeks · {len(tasks)} tasks</span>
        </div>""", unsafe_allow_html=True)

        for task in tasks:
            tid    = task.get("id", "")
            title  = task.get("title", "")
            desc   = task.get("description", "")
            owner  = task.get("owner", "")
            prio   = task.get("priority", "Medium")
            fws    = task.get("frameworks", [])
            icon   = OWNER_ICONS.get(owner, "👤")

            fw_badges = " ".join([
                f"<span style='background:#0d2040;border:1px solid #1e3a5f;padding:1px 7px;border-radius:12px;font-size:.7rem;color:#7090b0;'>{f}</span>"
                for f in fws
            ])

            with st.expander(f"{tid} · {title}"):
                status_options = ["pending", "in_progress", "complete", "blocked"]
                status_key = f"task_status_{tid}"
                if status_key not in st.session_state:
                    st.session_state[status_key] = "pending"

                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"""
                    <div style='line-height:2;'>
                        <span style='color:#e0e6f0;'>{desc}</span><br>
                        <span style='color:#7090b0;font-size:.8rem;'>{icon} Owner: <b style='color:#aabbcc;'>{owner}</b></span>&nbsp;&nbsp;
                        {_priority_badge(prio)}&nbsp;&nbsp;{fw_badges}
                    </div>""", unsafe_allow_html=True)
                with col_b:
                    new_status = st.selectbox("Status", status_options,
                                              index=status_options.index(st.session_state[status_key]),
                                              key=f"sel_{tid}")
                    st.session_state[status_key] = new_status

    # ── Milestones ───────────────────────────────────────────────────────────
    milestones = result.get("key_milestones", [])
    if milestones:
        st.markdown("<h4 style='color:#e0e6f0;font-size:.9rem;margin-top:1.5rem;'>🏁 Key Milestones</h4>", unsafe_allow_html=True)
        for i, ms in enumerate(milestones, 1):
            st.markdown(f"""
            <div class='gov-card' style='padding:.7rem 1rem;margin-bottom:.4rem;'>
                <span style='color:#00d4ff;font-family:"IBM Plex Mono",monospace;font-size:.8rem;'>{i:02d}</span>
                <span style='color:#e0e6f0;margin-left:.6rem;font-size:.85rem;'>{ms}</span>
            </div>""", unsafe_allow_html=True)
