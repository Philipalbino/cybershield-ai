# ai_engine.py
import os
import re
from dotenv import load_dotenv
from openai import OpenAI
from knowledge_base import CYBER_KB

# ===============================
# LOAD ENVIRONMENT VARIABLES
# ===============================
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===============================
# RISK SCORING FUNCTION
# ===============================
def calculate_risk(message: str):
    high_risk_keywords = [
        "bank password", "otp", "one time password", "credit card", "debit card",
        "wire transfer", "urgent payment", "click this link", "verify account",
        "bitcoin", "crypto investment", "lottery winner", "send money",
        "account suspended", "login immediately"
    ]

    score = 10
    for word in high_risk_keywords:
        if word.lower() in message.lower():
            score += 15
    if re.search(r"http[s]?://", message):
        score += 20

    # Cap score at 100
    score = min(score, 100)

    if score >= 75:
        level = "Critical"
    elif score >= 50:
        level = "High"
    elif score >= 30:
        level = "Medium"
    else:
        level = "Low"

    return score, level

# ===============================
# KNOWLEDGE BASE LOOKUP
# ===============================
def check_knowledge_base(message: str):
    """
    Looks for any topic in the KB inside the user message.
    Returns structured response if found.
    """
    message_lower = message.lower()
    for topic, data in CYBER_KB.items():
        if topic in message_lower:
            return f"""
📚 Knowledge Base Match: {topic.upper()}

Definition:
{data['definition']}

Prevention Controls:
- """ + "\n- ".join(data["controls"])
    return None

# ===============================
# MAIN AI ANALYSIS FUNCTION
# ===============================
def analyze_message(message: str):
    """
    Returns AI-generated response:
    - Uses knowledge base if topic matches
    - Falls back to GPT-4 for any free-form cybersecurity/fraud/cyberbullying question
    - Includes risk scoring and structured protection advice
    """
    # 1️ Check KB first
    kb_response = check_knowledge_base(message)
    score, level = calculate_risk(message)

    if kb_response:
        return f"""
Risk Level: {level}
Risk Score: {score}/100

{kb_response}

🛡 Awareness Advice:
Always verify suspicious communications, enable MFA, and never share sensitive credentials.
"""

    # 2️ GPT-4 system prompt
    system_prompt = """
You are CyberShield AI, a cybersecurity and fraud detection assistant.

For every response:
- Clearly explain the threat
- Identify attack type
- Explain why it is dangerous
- Provide technical prevention controls
- Provide user awareness advice
- Give step-by-step protection recommendations
- Keep response professional, structured, and actionable
"""

    # 3️ Call OpenAI GPT-4
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.3
    )

    ai_text = response.choices[0].message.content

    # 4️ Final structured response
    final_response = f"""
Risk Level: {level}
Risk Score: {score}/100

{ai_text}

🔐 General Protection Checklist:
• Enable Multi-Factor Authentication (MFA)
• Use strong unique passwords
• Keep systems updated
• Avoid suspicious links
• Verify sender identity before sharing data
"""
    return final_response
