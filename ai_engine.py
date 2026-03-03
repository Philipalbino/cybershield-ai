import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_message(user_input, conversation_history):
    """
    Generates strictly structured cybersecurity responses.
    """

    system_prompt = """
You are CyberShield AI, a professional cybersecurity expert.

Always respond using EXACTLY these section titles in this order:

Definition
Types
Example
Causes
Solutions
Prevention
Awareness

Respond in a clean ChatGPT style:
- Write the section title on its own line.
- Do NOT add symbols like ### or **.
- Do NOT use bullet points.
- Leave one blank line after each section title.
- Write 2–4 strong, well-structured sentences per section.
- Always include cybersecurity or digital context when relevant.
- Avoid generic academic tone.
- Avoid textbook style explanations.
- Write like a cybersecurity professional explaining clearly.
- Keep language precise and confident.
"""

    try:
        messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add previous conversation history
        messages.extend(conversation_history)

        # Add current user message
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.6,
            max_tokens=900
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ AI error: {str(e)}"
