# ─────────────────────────────────────────────────────────────
# AI Governance Assistant
# Author: Abhinav Sahai | linkedin.com/in/absahai
# GitHub: github.com/abhisahai/ai-governance-assistant
# Licence: MIT © 2026
# ─────────────────────────────────────────────────────────────

"""pages/audit_summaries.py — AI Audit Report Generator."""

import json
import streamlit as st
from utils.llm import generate_audit_summary

STATUS_ICONS = {"Pass": "✅", "Fail": "❌", "Partial": "⚠️", "N/A": "➖"}
STATUS_COLORS = {"Pass": "#00e676", "Fail": "#ff5252", "Partial": "#ffab40", "N/A": "#7090b0"}

SAMPLE_EVIDENCE = """System: Automated loan approval AI
Evidence collected during Q2 2025 internal audit:
- Model card exists but was last updated 14 months ago
- Fairness testing was conducted on gender and race dimensions; results show <2% disparity
- No formal bias monitoring in production; alerts are manual
- Data lineage documented in Confluence but not linked to model registry
- Human override mechanism exists but used in <0.3% of cases
- DPIA completed for GDPR; last reviewed 2 years ago
- Incident log maintained; 2 incidents reported in last 12 months, both resolved within SLA
- Model explainability: SHAP values available internally but not surfaced to applicants
- Third-party vendor contract includes AI-specific clauses
- No automated drift detection; model performance reviewed quarterly
"""


def render():
    st.markdown("<h1 style='color:#00d4ff;'>📊 Audit Summaries</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#7090b0;font-size:.85rem;'>Generate structured audit reports with control assessments, findings, and remediation plans.</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        audit_scope = st.text_input(
            "Audit Scope",
            placeholder="e.g. Q2 2025 AI Governance Audit — Lending Division",
        )
        framework = st.selectbox("Compliance Framework", [
            "EU AI Act", "NIST AI RMF", "ISO/IEC 42001", "GDPR", "SOC 2", "Combined (EU AI Act + GDPR)"
        ])
    with col2:
        if st.button("Load Sample Evidence", use_container_width=True):
            st.session_state["audit_evidence"] = SAMPLE_EVIDENCE

    evidence = st.text_area(
        "Evidence / System Description",
        value=st.session_state.get("audit_evidence", ""),
        height=220,
        placeholder="Describe the AI system and paste any audit evidence, logs, documentation, or interview notes...",
    )

    if st.button("📝 Generate Audit Report", use_container_width=True):
        if not st.session_state.get("api_key"):
            st.error("Please enter your OpenAI API key in the sidebar.")
            return
        if not audit_scope.strip() or not evidence.strip():
            st.warning("Please fill in audit scope and evidence.")
            return

        with st.spinner("Generating audit report..."):
            try:
                result = generate_audit_summary(audit_scope, evidence, framework)
                st.session_state["audit_result"] = result
            except Exception as e:
                st.error(f"Audit generation failed: {e}")
                return

    result = st.session_state.get("audit_result")
    if not result:
        return

    st.markdown("---")

    # ── Audit Header ─────────────────────────────────────────────────────────
    audit_id = result.get("audit_id", "AUDIT-XXXX")
    status   = result.get("overall_status", "Unknown")
    pct      = result.get("compliance_percentage", 0)
    trend    = result.get("trend", "Stable")
    trend_arrow = {"Improving": "↑", "Stable": "→", "Declining": "↓"}.get(trend, "→")
    trend_color = {"Improving": "#00e676", "Stable": "#ffab40", "Declining": "#ff5252"}.get(trend, "#7090b0")
    status_color = {"Compliant": "#00e676", "Partially Compliant": "#ffab40", "Non-Compliant": "#ff5252"}.get(status, "#7090b0")

    st.markdown(f"""
    <div class='gov-card' style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;'>
        <div>
            <div style='font-family:"IBM Plex Mono",monospace;font-size:.75rem;color:#7090b0;'>AUDIT REPORT</div>
            <div style='font-size:1.2rem;font-weight:700;color:#e0e6f0;font-family:"IBM Plex Mono",monospace;'>{audit_id}</div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:2rem;font-weight:700;color:#00d4ff;font-family:"IBM Plex Mono",monospace;'>{pct}%</div>
            <div style='color:#7090b0;font-size:.75rem;'>Compliance</div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:1.2rem;font-weight:700;color:{status_color};'>{status}</div>
            <div style='color:#7090b0;font-size:.75rem;'>Overall Status</div>
        </div>
        <div style='text-align:center;'>
            <div style='font-size:1.5rem;font-weight:700;color:{trend_color};'>{trend_arrow} {trend}</div>
            <div style='color:#7090b0;font-size:.75rem;'>Trend</div>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Control Stats ────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    ca = result.get("controls_assessed", 0)
    cp = result.get("controls_passed", 0)
    cf = result.get("controls_failed", 0)
    cn = result.get("controls_not_applicable", 0)

    sc1, sc2, sc3, sc4 = st.columns(4)
    for col, val, lbl, clr in zip([sc1, sc2, sc3, sc4],
                                   [ca, cp, cf, cn],
                                   ["Assessed", "Passed", "Failed", "N/A"],
                                   ["#00d4ff", "#00e676", "#ff5252", "#7090b0"]):
        with col:
            st.markdown(f"""
            <div class='metric-tile'>
                <div class='val' style='color:{clr};'>{val}</div>
                <div class='lbl'>{lbl}</div>
            </div>""", unsafe_allow_html=True)

    if ca > 0:
        st.progress(cp / max(ca, 1))

    # ── Executive Summary ────────────────────────────────────────────────────
    summary = result.get("executive_summary", "")
    st.markdown(f"""
    <div class='gov-card gov-card-accent' style='margin-top:1rem;'>
        <div style='font-size:.7rem;color:#7090b0;font-family:"IBM Plex Mono",monospace;margin-bottom:.5rem;'>EXECUTIVE SUMMARY</div>
        <p style='color:#e0e6f0;margin:0;line-height:1.7;'>{summary}</p>
    </div>""", unsafe_allow_html=True)

    # ── Findings Table ───────────────────────────────────────────────────────
    findings = result.get("findings", [])
    if findings:
        st.markdown("<h4 style='color:#e0e6f0;font-size:.9rem;margin-top:1.5rem;'>Control Findings</h4>", unsafe_allow_html=True)

        # Filter
        filter_status = st.multiselect("Filter by status", ["Pass", "Fail", "Partial", "N/A"], default=["Fail", "Partial"])
        shown = [f for f in findings if not filter_status or f.get("status") in filter_status]

        for f in shown:
            s   = f.get("status", "N/A")
            sc  = STATUS_COLORS.get(s, "#7090b0")
            si  = STATUS_ICONS.get(s, "")
            cid = f.get("control_id", "")
            cn_ = f.get("control_name", "")

            with st.expander(f"{si} [{cid}] {cn_}"):
                st.markdown(f"""
                <div style='line-height:2;font-size:.85rem;'>
                    <b style='color:#7090b0;'>Status:</b> <span style='color:{sc};font-weight:700;'>{s}</span><br>
                    <b style='color:#7090b0;'>Evidence:</b> <span style='color:#e0e6f0;'>{f.get('evidence','—')}</span><br>
                """, unsafe_allow_html=True)
                if f.get("gap"):
                    st.markdown(f"<b style='color:#7090b0;'>Gap:</b> <span style='color:#ffcdd2;'>{f['gap']}</span><br>", unsafe_allow_html=True)
                if f.get("remediation"):
                    st.markdown(f"<b style='color:#7090b0;'>Remediation:</b> <span style='color:#00d4ff;'>{f['remediation']}</span><br>", unsafe_allow_html=True)
                if f.get("due_date"):
                    st.markdown(f"<b style='color:#7090b0;'>Due Date:</b> <span style='color:#ffab40;'>{f['due_date']}</span>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # ── Next Audit Recommendation ─────────────────────────────────────────────
    next_rec = result.get("next_audit_recommendation", "")
    if next_rec:
        st.markdown(f"""
        <div class='gov-card' style='margin-top:1rem;border-left:4px solid #ffab40;'>
            <div style='font-size:.7rem;color:#7090b0;font-family:"IBM Plex Mono",monospace;margin-bottom:.4rem;'>NEXT AUDIT RECOMMENDATION</div>
            <p style='color:#e0e6f0;margin:0;font-size:.85rem;'>{next_rec}</p>
        </div>""", unsafe_allow_html=True)

    # ── Export ────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "⬇️ Export Audit Report (JSON)",
        data=json.dumps(result, indent=2),
        file_name=f"{audit_id}_report.json",
        mime="application/json",
        use_container_width=True,
    )
