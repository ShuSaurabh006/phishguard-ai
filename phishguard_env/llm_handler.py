"""
FREE LLM Handler for PhishGuard-AI
Uses smart rules instead of paid API - Works perfectly!
"""

import re
from typing import List

class SimpleLLM:
    def __init__(self):
        # No API key needed - we use smart rules!
        print("🆓 Using FREE rule-based AI detection!")
        
        # Phishing keywords and patterns
        self.phishing_keywords = [
            'urgent', 'immediately', 'suspended', 'verify', 'confirm',
            'click here', 'act now', 'expires', 'limited time', 'warning',
            'security alert', 'account locked', 'unusual activity'
        ]
        
        self.suspicious_domains = [
            '.tk', '.ml', '.cf', '.ga', 'bit.ly', 'tinyurl',
            'secure-bank', 'verify-account', 'bank-alert'
        ]
    
    def ask_llm(self, system_prompt, user_question):
        """Fake LLM that uses smart rules"""
        email_content = user_question.lower()
        
        # Count suspicious indicators
        phishing_score = 0
        reasons = []
        
        # Check for urgent language
        urgent_words = sum(1 for word in self.phishing_keywords if word in email_content)
        if urgent_words > 2:
            phishing_score += 3
            reasons.append(f"Contains {urgent_words} urgency keywords")
        
        # Check for suspicious links
        if 'http' in email_content:
            urls = re.findall(r'http[s]?://[^\s]+', email_content)
            for url in urls:
                if any(domain in url for domain in self.suspicious_domains):
                    phishing_score += 4
                    reasons.append("Contains suspicious URL")
        
        # Check for credential requests
        if any(word in email_content for word in ['password', 'login', 'verify', 'confirm']):
            phishing_score += 2
            reasons.append("Requests credentials/verification")
        
        # Check for generic greetings
        if 'dear customer' in email_content or 'dear user' in email_content:
            phishing_score += 1
            reasons.append("Uses generic greeting")
        
        # Make decision
        if phishing_score >= 4:
            decision = "PHISHING"
            explanation = f"This email is likely PHISHING because: {', '.join(reasons)}"
        else:
            decision = "SAFE"
            explanation = f"This email appears SAFE. Score: {phishing_score}/10"
        
        return f"{decision}\n{explanation}"
    
    def analyze_email(self, email_content):
        """Analyze if email is phishing using rules"""
        system_prompt = "You are a phishing detector"
        user_question = f"Analyze this email:\n\n{email_content}"
        
        return self.ask_llm(system_prompt, user_question)
