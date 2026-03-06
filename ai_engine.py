import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_message(user_input, conversation_history):
    """
    Generates strictly structured cybersecurity responses.
    """

    system_prompt = """
You are CyberShield AI, a professional cybersecurity expert.

You MUST follow this structure EXACTLY:

Definition
Types
Example
Causes
Solutions
Prevention
Awareness

Formatting rules (STRICT):

1. Write the section title exactly as shown.
2. Leave one blank line after the title.
3. Write ONE short paragraph per section.
4. Each paragraph must contain 2–3 sentences only.
5. Do NOT use bullet points, numbering, symbols, markdown, or lists.
6. Do NOT add headings like ### or **.
7. Do NOT write long academic explanations.
8. Keep sentences clear, direct, and professional.

Writing style:

Explain like a cybersecurity professional speaking clearly to a user.
Use practical cybersecurity context such as phishing, malware, networks, data protection, or digital threats.
Avoid textbook language.

The final response must look like a clean ChatGPT-style explanation with short readable paragraphs.
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
