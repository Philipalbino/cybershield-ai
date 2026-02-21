# knowledge_base.py

CYBER_KB = {
    "fraud": {
        "definition": (
            "Fraud is a deliberate act of deception to obtain unfair or unlawful gain. "
            "It can target individuals or organizations and include identity theft, financial scams, social engineering, or online deception."
        ),
        "controls": [
            "Enable Multi-Factor Authentication (MFA) on all sensitive accounts",
            "Educate users on common fraud tactics and social engineering",
            "Monitor financial transactions for unusual activity",
            "Verify requests for money or personal data through official channels",
            "Report suspected fraud to authorities or internal security teams",
            "Use strong, unique passwords and avoid credential reuse",
        ]
    },
    "cyberbullying": {
        "definition": (
            "Cyberbullying is using digital platforms to harass, threaten, or humiliate someone. "
            "It can occur through social media, messaging apps, emails, or forums."
        ),
        "controls": [
            "Educate individuals on safe online behavior and respectful communication",
            "Monitor online interactions and report abusive content",
            "Use privacy settings to restrict who can contact you",
            "Avoid responding to cyberbullying messages",
            "Document and report incidents to platform moderators or authorities",
        ]
    },
    "identity theft": {
        "definition": (
            "Identity theft occurs when someone uses another person's personal information, "
            "such as social security number, bank account, or login credentials, to commit fraud."
        ),
        "controls": [
            "Monitor credit reports regularly",
            "Do not share sensitive personal information online",
            "Use strong passwords and MFA",
            "Shred physical documents containing sensitive information",
            "Report stolen identities immediately to authorities",
        ]
    },
    "online scams": {
        "definition": (
            "Online scams are schemes that trick individuals into giving money, data, or access to accounts. "
            "They often appear as fake websites, job offers, or fraudulent investment opportunities."
        ),
        "controls": [
            "Verify the legitimacy of websites and offers before engaging",
            "Be skeptical of unsolicited communications promising quick money",
            "Never share personal or financial information with unverified parties",
            "Report scam websites or communications to authorities",
            "Keep systems updated and protected with security software",
        ]
    },
    "social engineering": {
        "definition": (
            "Social engineering is the manipulation of people into performing actions or divulging confidential information, "
            "often by exploiting trust, fear, or urgency."
        ),
        "controls": [
            "Educate employees and users about social engineering tactics",
            "Verify the identity of individuals requesting sensitive information",
            "Implement strict policies for sharing data",
            "Encourage reporting of suspicious behavior immediately",
            "Use technical controls like MFA and access restrictions",
        ]
    },
    "financial scams": {
        "definition": (
            "Financial scams involve tricking individuals into transferring money or revealing financial details through deceitful schemes."
        ),
        "controls": [
            "Verify payment requests carefully",
            "Be cautious with unexpected financial solicitations",
            "Use secure and traceable payment methods",
            "Monitor bank statements for unauthorized transactions",
            "Educate users about common financial fraud tactics",
        ]
    },
    "data breach": {
        "definition": (
            "A data breach is unauthorized access, use, or disclosure of sensitive information from an organization or individual."
        ),
        "controls": [
            "Encrypt sensitive data at rest and in transit",
            "Limit access to sensitive information based on roles",
            "Keep systems and software updated",
            "Monitor network and system logs for unusual activity",
            "Have an incident response plan for breaches",
        ]
    },
    "cyber harassment": {
        "definition": (
            "Cyber harassment is repeated online behavior intended to intimidate, threaten, or distress a person or group."
        ),
        "controls": [
            "Block or restrict harassers on platforms",
            "Document all incidents for reporting purposes",
            "Report abusive content to platform moderators or authorities",
            "Educate users on recognizing and preventing harassment",
            "Encourage mental health support for victims",
        ]
    },
    "online fraud": {
        "definition": (
            "Online fraud refers to deceitful activity carried out through digital platforms to steal money, data, or personal information."
        ),
        "controls": [
            "Use secure websites with HTTPS for transactions",
            "Enable MFA on all online accounts",
            "Educate users about fake websites and scams",
            "Monitor accounts for unauthorized activity",
            "Report incidents promptly to authorities or platforms",
        ]
    },
    # Add more topics dynamically as needed
}

# Note: GPT-4 in ai_engine.py will handle any question beyond this KB.
# This makes the system "open-ended", like ChatGPT.
