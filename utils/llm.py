# ─────────────────────────────────────────────────────────────
# AI Governance Assistant
# Author: Abhinav Sahai | linkedin.com/in/absahai
# GitHub: github.com/abhisahai/ai-governance-assistant
# Licence: MIT © 2026
# ─────────────────────────────────────────────────────────────

"""
utils/llm.py
Centralised OpenAI helpers for the AI Governance Assistant.
All 4 main pages use this — same API key and model as the Compliance Agent.
"""

import json
import re
from typing import Any

from langchain_openai import ChatOpenAI
import streamlit as st


# ── LLM Factory ──────────────────────────────────────────────────────────────

def get_llm(temperature: float = 0.2) -> ChatOpenAI:
    api_key = st.session_state.get("api_key", "")
    model   = st.session_state.get("model", "gpt-4o")
    if not api_key:
        raise ValueError("No OpenAI API key found. Please enter your key in the sidebar.")
    return ChatOpenAI(model=model, temperature=temperature, openai_api_key=api_key)


def _call(system: str, user: str, temperature: float = 0.2) -> str:
    llm = get_llm(temperature)
    from langchain_core.messages import HumanMessage, SystemMessage
    messages = [SystemMessage(content=system), HumanMessage(content=user)]
    return llm.invoke(messages).content


def _parse_json(raw: str) -> Any:
    clean = re.sub(r"```(?:json)?|```", "", raw).strip()
    return json.loads(clean)


# ── Feature: Policy Validation ───────────────────────────────────────────────

POLICY_SYSTEM = """You are an expert AI governance and compliance analyst specialising in
EU AI Act, NIST AI RMF, ISO/IEC 42001, GDPR, and SOC 2.
Analyse AI policy documents and return ONLY a JSON object with this exact structure:
{
  "overall_score": <int 0-100>,
  "risk_tier": "<Minimal|Limited|High|Unacceptable>",
  "framework_coverage": {
    "EU AI Act": <int 0-100>,
    "NIST AI RMF": <int 0-100>,
    "ISO 42001": <int 0-100>,
    "GDPR": <int 0-100>
  },
  "findings": [
    {"category": "<string>", "severity": "<Low|Medium|High>", "description": "<string>", "recommendation": "<string>"}
  ],
  "strengths": ["<string>"],
  "gaps": ["<string>"],
  "executive_summary": "<2-3 sentence plain-English summary>"
}"""


def validate_policy(policy_text: str, policy_type: str) -> dict:
    user = f"Policy Type: {policy_type}\n\nPolicy Document:\n{policy_text}"
    raw  = _call(POLICY_SYSTEM, user)
    return _parse_json(raw)


# ── Feature: Risk Scoring ─────────────────────────────────────────────────────

RISK_SYSTEM = """You are an AI risk assessment expert. Given a description of an AI system,
return ONLY a JSON object:
{
  "composite_score": <int 0-100>,
  "risk_level": "<Low|Medium|High|Critical>",
  "dimensions": {
    "technical_risk": {"score": <int 0-100>, "rationale": "<string>"},
    "ethical_risk": {"score": <int 0-100>, "rationale": "<string>"},
    "legal_risk": {"score": <int 0-100>, "rationale": "<string>"},
    "operational_risk": {"score": <int 0-100>, "rationale": "<string>"},
    "reputational_risk": {"score": <int 0-100>, "rationale": "<string>"}
  },
  "red_flags": ["<string>"],
  "mitigations": [{"risk": "<string>", "action": "<string>", "priority": "<Immediate|Short-term|Long-term>"}],
  "eu_ai_act_classification": "<string>",
  "summary": "<2-3 sentence plain-English summary>"
}"""


def score_risk(system_description: str, deployment_context: str, data_types: list[str]) -> dict:
    user = f"""AI System Description: {system_description}
Deployment Context: {deployment_context}
Data Types Processed: {', '.join(data_types)}"""
    raw = _call(RISK_SYSTEM, user)
    return _parse_json(raw)


# ── Feature: Compliance Workflow ──────────────────────────────────────────────

COMPLIANCE_SYSTEM = """You are an AI compliance specialist. Generate a structured compliance
action plan and return ONLY a JSON object:
{
  "project_name": "<string>",
  "total_tasks": <int>,
  "estimated_weeks": <int>,
  "phases": [
    {
      "phase": "<string>",
      "duration_weeks": <int>,
      "tasks": [
        {
          "id": "<string e.g. T1.1>",
          "title": "<string>",
          "description": "<string>",
          "owner": "<string e.g. Legal|Engineering|Data Science|CISO>",
          "priority": "<Critical|High|Medium|Low>",
          "frameworks": ["<EU AI Act|NIST|ISO 42001|GDPR|SOC 2>"],
          "status": "pending"
        }
      ]
    }
  ],
  "key_milestones": ["<string>"],
  "quick_wins": ["<string>"]
}"""


def generate_compliance_workflow(org_name: str, ai_use_cases: str, frameworks: list[str], maturity: str) -> dict:
    user = f"""Organisation: {org_name}
AI Use Cases: {ai_use_cases}
Target Frameworks: {', '.join(frameworks)}
Current Maturity Level: {maturity}"""
    raw = _call(COMPLIANCE_SYSTEM, user, temperature=0.3)
    return _parse_json(raw)


# ── Feature: Audit Summaries ──────────────────────────────────────────────────

AUDIT_SYSTEM = """You are an AI governance auditor. Analyse audit evidence and logs and
return ONLY a JSON object:
{
  "audit_id": "<AUDIT-YYYY-NNN format>",
  "audit_date": "<today's date>",
  "overall_status": "<Compliant|Partially Compliant|Non-Compliant>",
  "compliance_percentage": <int 0-100>,
  "executive_summary": "<3-4 sentence summary>",
  "controls_assessed": <int>,
  "controls_passed": <int>,
  "controls_failed": <int>,
  "controls_not_applicable": <int>,
  "findings": [
    {
      "control_id": "<string>",
      "control_name": "<string>",
      "status": "<Pass|Fail|Partial|N/A>",
      "evidence": "<string>",
      "gap": "<string or null>",
      "remediation": "<string or null>",
      "due_date": "<YYYY-MM-DD or null>"
    }
  ],
  "trend": "<Improving|Stable|Declining>",
  "next_audit_recommendation": "<string>"
}"""


def generate_audit_summary(audit_scope: str, evidence: str, framework: str) -> dict:
    user = f"""Audit Scope: {audit_scope}
Compliance Framework: {framework}
Evidence / System Description:\n{evidence}"""
    raw = _call(AUDIT_SYSTEM, user)
    return _parse_json(raw)
