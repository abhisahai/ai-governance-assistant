# ─────────────────────────────────────────────────────────────
# AI Governance Assistant
# Author: Abhinav Sahai | linkedin.com/in/absahai
# GitHub: github.com/abhisahai/ai-governance-assistant
# Licence: MIT © 2026
# ─────────────────────────────────────────────────────────────

"""
utils/agent.py
Multi-step Compliance Agent using LangGraph + LangChain 1.x + GPT-4o.

Architecture:
  User input → LangGraph ReAct agent → GPT-4o decides tool order
  → calls 5 tools sequentially → synthesises unified governance report

Tools (enforced execution order via tool descriptions):
  1. risk_score_tool        — multi-dimension risk scoring
  2. eu_ai_act_tool         — regulatory classification
  3. policy_gap_tool        — gap identification
  4. compliance_plan_tool   — action plan generation
  5. governance_report_tool — unified report synthesis
"""

import json
import re
from typing import Any

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_llm() -> ChatOpenAI:
    api_key = st.session_state.get("api_key", "")
    model   = st.session_state.get("model", "gpt-4o")
    if not api_key:
        raise ValueError("No OpenAI API key found. Please enter it in the sidebar.")
    return ChatOpenAI(model=model, temperature=0.2, openai_api_key=api_key)


def _parse_json(raw: str) -> Any:
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    return json.loads(clean)


def _llm_call(prompt: str) -> str:
    llm = _get_llm()
    return llm.invoke(prompt).content


# ── Tools ─────────────────────────────────────────────────────────────────────

@tool
def risk_score_tool(system_description: str) -> str:
    """
    STEP 1 — Always call this first.
    Scores an AI system across 5 risk dimensions: technical, ethical, legal,
    operational, and reputational. Returns composite risk score and red flags.
    Input: full plain-text description of the AI system.
    """
    prompt = f"""You are an AI risk assessment expert.
Analyse this AI system and return ONLY a JSON object:
{{
  "composite_score": <int 0-100>,
  "risk_level": "<Low|Medium|High|Critical>",
  "dimensions": {{
    "technical_risk":    {{"score": <int>, "rationale": "<string>"}},
    "ethical_risk":      {{"score": <int>, "rationale": "<string>"}},
    "legal_risk":        {{"score": <int>, "rationale": "<string>"}},
    "operational_risk":  {{"score": <int>, "rationale": "<string>"}},
    "reputational_risk": {{"score": <int>, "rationale": "<string>"}}
  }},
  "red_flags": ["<string>"],
  "top_mitigations": ["<string>"]
}}
AI System: {system_description}"""

    result = _parse_json(_llm_call(prompt))
    st.session_state["agent_risk"] = result
    dims = result.get("dimensions", {})
    return (
        f"RISK SCORE COMPLETE — {result.get('composite_score')}/100 "
        f"({result.get('risk_level')} risk) | "
        f"Ethical: {dims.get('ethical_risk',{}).get('score')}/100 | "
        f"Legal: {dims.get('legal_risk',{}).get('score')}/100 | "
        f"Red flags: {len(result.get('red_flags', []))}"
    )


@tool
def eu_ai_act_tool(system_description: str) -> str:
    """
    STEP 2 — Call after risk_score_tool.
    Classifies an AI system under EU AI Act risk tiers and Annex III.
    Returns risk tier, applicable articles, and conformity obligations.
    Input: full plain-text description of the AI system.
    """
    prompt = f"""You are an EU AI Act compliance expert.
Classify this AI system and return ONLY a JSON object:
{{
  "risk_tier": "<Minimal|Limited|High|Unacceptable>",
  "annex_classification": "<Annex III|Annex II|Not listed|Prohibited>",
  "applicable_articles": ["<Article X — description>"],
  "conformity_assessment_required": <true|false>,
  "key_obligations": ["<string>"],
  "classification_rationale": "<2 sentence explanation>"
}}
AI System: {system_description}"""

    result = _parse_json(_llm_call(prompt))
    st.session_state["agent_euact"] = result
    return (
        f"EU AI ACT COMPLETE — {result.get('risk_tier')} tier | "
        f"{result.get('annex_classification')} | "
        f"Conformity required: {result.get('conformity_assessment_required')} | "
        f"Articles: {len(result.get('applicable_articles', []))}"
    )


@tool
def policy_gap_tool(system_description: str) -> str:
    """
    STEP 3 — Call after eu_ai_act_tool.
    Identifies critical governance policy gaps against EU AI Act,
    NIST AI RMF, GDPR, and ISO 42001.
    Input: full plain-text description of the AI system.
    """
    prompt = f"""You are an AI governance policy analyst.
Identify critical policy gaps and return ONLY a JSON object:
{{
  "overall_policy_score": <int 0-100>,
  "critical_gaps": [
    {{"gap": "<string>", "framework": "<EU AI Act|NIST|GDPR|ISO 42001>",
      "severity": "<High|Medium|Low>", "recommendation": "<string>"}}
  ],
  "missing_policies": ["<string>"],
  "immediate_actions": ["<string>"]
}}
AI System: {system_description}"""

    result = _parse_json(_llm_call(prompt))
    st.session_state["agent_policy"] = result
    critical = [g for g in result.get("critical_gaps", []) if g.get("severity") == "High"]
    return (
        f"POLICY GAP COMPLETE — Score: {result.get('overall_policy_score')}/100 | "
        f"Critical gaps: {len(critical)} | "
        f"Missing policies: {len(result.get('missing_policies', []))}"
    )


@tool
def compliance_plan_tool(system_description: str) -> str:
    """
    STEP 4 — Call after policy_gap_tool.
    Generates a prioritised compliance action plan with ownership and deadlines.
    Input: full plain-text description of the AI system.
    """
    prompt = f"""You are an AI compliance programme manager.
Generate a prioritised action plan and return ONLY a JSON object:
{{
  "total_tasks": <int>,
  "estimated_weeks": <int>,
  "immediate_actions": [
    {{"task": "<string>", "owner": "<string>", "framework": "<string>", "deadline": "<string>"}}
  ],
  "short_term_actions": [
    {{"task": "<string>", "owner": "<string>", "framework": "<string>", "deadline": "<string>"}}
  ],
  "long_term_actions": [
    {{"task": "<string>", "owner": "<string>", "framework": "<string>", "deadline": "<string>"}}
  ],
  "quick_wins": ["<string>"]
}}
AI System: {system_description}"""

    result = _parse_json(_llm_call(prompt))
    st.session_state["agent_plan"] = result
    return (
        f"COMPLIANCE PLAN COMPLETE — {result.get('total_tasks')} tasks | "
        f"~{result.get('estimated_weeks')} weeks | "
        f"Immediate: {len(result.get('immediate_actions', []))} | "
        f"Quick wins: {len(result.get('quick_wins', []))}"
    )


@tool
def governance_report_tool(system_description: str) -> str:
    """
    STEP 5 — Call LAST, only after all four other tools are complete.
    Synthesises all prior assessments into a unified board-level governance report.
    Input: full plain-text description of the AI system.
    """
    risk   = st.session_state.get("agent_risk", {})
    euact  = st.session_state.get("agent_euact", {})
    policy = st.session_state.get("agent_policy", {})
    plan   = st.session_state.get("agent_plan", {})

    prompt = f"""You are a Chief AI Governance Officer writing a board-level report.
Synthesise these assessment results into a unified governance report.
Return ONLY a JSON object:
{{
  "report_title": "<string>",
  "overall_governance_score": <int 0-100>,
  "governance_rating": "<Red|Amber|Green>",
  "executive_summary": "<4-5 sentence board-level summary>",
  "audit_readiness_score": <int 0-100>,
  "top_3_risks": ["<string>"],
  "top_3_immediate_actions": ["<string>"],
  "regulatory_exposure": "<Low|Medium|High|Critical>",
  "recommendation": "<1 sentence clear recommendation for leadership>"
}}

Risk Assessment: {json.dumps(risk)}
EU AI Act Classification: {json.dumps(euact)}
Policy Gap Analysis: {json.dumps(policy)}
Compliance Action Plan: {json.dumps(plan)}
System Context: {system_description}"""

    result = _parse_json(_llm_call(prompt))
    st.session_state["agent_report"] = result
    return (
        f"GOVERNANCE REPORT COMPLETE — "
        f"Score: {result.get('overall_governance_score')}/100 | "
        f"Rating: {result.get('governance_rating')} | "
        f"Audit readiness: {result.get('audit_readiness_score')}/100"
    )


# ── Agent ─────────────────────────────────────────────────────────────────────

TOOLS = [
    risk_score_tool,
    eu_ai_act_tool,
    policy_gap_tool,
    compliance_plan_tool,
    governance_report_tool,
]

SYSTEM_PROMPT = """You are an expert AI Governance Agent with deep knowledge of EU AI Act,
NIST AI RMF, ISO/IEC 42001, and GDPR.

You MUST call all five tools in this exact order — no exceptions:
1. risk_score_tool
2. eu_ai_act_tool
3. policy_gap_tool
4. compliance_plan_tool
5. governance_report_tool

Pass the full AI system description to each tool.
Do not skip any tool. Do not call governance_report_tool before the other four are done.
When all five tools are complete, respond with: "Assessment complete."
"""


def run_agent(system_description: str) -> str:
    """Run the full LangGraph compliance agent."""
    for key in ["agent_risk", "agent_euact", "agent_policy", "agent_plan", "agent_report"]:
        st.session_state.pop(key, None)

    llm   = _get_llm()
    agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_PROMPT)

    result = agent.invoke({
        "messages": [HumanMessage(content=system_description)]
    })

    messages = result.get("messages", [])
    for msg in reversed(messages):
        if hasattr(msg, "content") and msg.content:
            return msg.content

    return "Assessment complete."
