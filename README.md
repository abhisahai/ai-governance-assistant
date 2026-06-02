# 🛡️ AI Governance Assistant

> An enterprise-grade AI risk and compliance platform built with Python, Streamlit, and the Anthropic Claude API.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=flat-square&logo=streamlit)
![Claude](https://img.shields.io/badge/Powered%20by-Claude%20API-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## Overview

The AI Governance Assistant helps organisations evaluate, score, plan, and audit their AI systems against major global compliance frameworks. It combines domain expertise in AI governance with large language model reasoning to produce structured, actionable outputs — not generic advice.

Built to demonstrate the intersection of **AI product thinking**, **GRC domain knowledge**, and **hands-on engineering capability**.

---

## Screenshots

### Policy Validator
![Policy Validator](assets/policy_validator.png)
*Paste any AI policy document and receive a compliance score, framework coverage breakdown, findings by severity, strengths, and gaps — all grounded in EU AI Act, NIST AI RMF, ISO 42001, and GDPR.*

### Risk Scorer
![Risk Scorer](assets/risk_scorer.png)
*Describe your AI system and deployment context to generate a multi-dimensional risk profile across five vectors, with EU AI Act classification and prioritised mitigations.*

### Compliance Workflow
![Compliance Workflow](assets/compliance_workflow.png)
*Generate a phase-gated compliance action plan with task ownership, framework mapping, status tracking, and key milestones — tailored to your organisation's maturity level.*

### Audit Summaries
![Audit Summaries](assets/audit_summaries.png)
*Produce structured audit reports with control-by-control assessments, evidence review, gap analysis, remediation deadlines, and exportable JSON output.*

---

## Features

| Feature | Description |
|---|---|
| **📋 Policy Validator** | Analyses AI policy documents against EU AI Act, NIST AI RMF, ISO/IEC 42001, and GDPR. Returns a compliance score, risk tier, framework coverage percentages, findings by severity, strengths, and gaps. |
| **⚠️ Risk Scorer** | Generates a composite risk score across five dimensions: technical, ethical, legal, operational, and reputational. Includes EU AI Act classification (Minimal / Limited / High / Unacceptable / Annex III) and prioritised mitigation actions. |
| **✅ Compliance Workflow** | Builds a phase-gated action plan with tasks assigned to owners (Legal, Engineering, Data Science, CISO), priority levels, framework tags, status tracking, quick wins, and milestone timeline. |
| **📊 Audit Summaries** | Produces structured audit reports with control IDs, pass/fail/partial status, evidence review, gap identification, remediation actions with due dates, and JSON export. |
| **🤖 Compliance Agent** | LangChain AgentExecutor powered by GPT-4o. Autonomously orchestrates all five assessment tools in sequence — risk scoring, EU AI Act classification, policy gap analysis, compliance planning, and unified report synthesis — in a single run with no user intervention between steps. |

---

## Supported Frameworks

- 🇪🇺 **EU AI Act** — Risk-tier classification (Minimal, Limited, High, Unacceptable) and Annex III high-risk system identification
- 🇺🇸 **NIST AI RMF** — Govern, Map, Measure, Manage function coverage
- 🌐 **ISO/IEC 42001** — AI management system standard requirements
- 🔒 **GDPR** — Data protection obligations including Article 22 (automated decisions) and Article 35 (DPIA)
- 🔐 **SOC 2** — Security, availability, and confidentiality control assessment

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit 1.35+ |
| AI / LLM | OpenAI API (GPT-4o, GPT-4-turbo, GPT-3.5-turbo) |
| Backend | Python 3.9+ |
| Prompt Design | Structured JSON output via system prompts |
| Agent Framework | LangChain AgentExecutor + ConversationBufferMemory |
| Agent Model | GPT-4o — optimal for LangChain tool-calling reliability |
| Styling | Custom CSS — dark navy theme with IBM Plex Mono |

---

## Project Structure

```
ai_governance_assistant/
├── app.py                      # Entry point, navigation, sidebar, CSS theme
├── requirements.txt            # Python dependencies
├── README.md
├── assets/                     # Screenshots for README
├── pages/
│   ├── dashboard.py            # Overview and getting started
│   ├── policy_validator.py     # Policy analysis feature
│   ├── risk_scorer.py          # Risk scoring feature
│   ├── compliance_workflow.py  # Compliance action plan generator
│   └── audit_summaries.py      # Audit report generator with JSON export
└── utils/
    ├── llm.py                  # All Claude API calls and prompt definitions
    └── agent.py                # LangChain AgentExecutor, 5 tool definitions, GPT-4o
```

---

## Quick Start

### Prerequisites

- Python 3.9 or higher
- An OpenAI API key — get one at [platform.openai.com](https://platform.openai.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-governance-assistant.git
cd ai-governance-assistant

# 2. Create a virtual environment
python -m venv venv

# Activate — Mac/Linux
source venv/bin/activate

# Activate — Windows
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

Enter your Anthropic API key in the sidebar to connect. Each page includes a **Load Sample** button so you can explore all features without your own data.

---

## Design Decisions

**Why these four features?**
They map directly to the four core functions any enterprise AI governance programme needs: policy definition, risk assessment, remediation planning, and compliance verification. This is not a demo — it is a working tool shaped by real GRC programme structure.

**Why Claude over other LLMs?**
Claude's instruction-following and structured output reliability make it well-suited for governance use cases where JSON schema conformance and reasoning quality directly affect output trustworthiness.

**Why Streamlit?**
Streamlit enables rapid prototyping of data and AI tools without frontend overhead, making it ideal for demonstrating AI product concepts to technical and non-technical stakeholders alike.

---

## Cost

All AI analysis runs via the Anthropic API. Approximate cost per action using Claude Sonnet:

| Action | Approx. cost |
|---|---|
| Policy Validation | ~$0.02 |
| Risk Scoring | ~$0.01 |
| Compliance Workflow | ~$0.03 |
| Audit Summary | ~$0.02 |

A $5 credit covers several hundred analyses.

---

## Disclaimer

This tool assists governance analysis and is intended for informational and portfolio purposes. It does not constitute legal or compliance advice. Always consult qualified legal and compliance professionals for binding decisions.

---

## Author

**Abhinav** · Senior Technical Program Manager  
AI · GRC · Enterprise SaaS · Product Management  

[LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN) · [GitHub](https://github.com/YOUR_USERNAME)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
