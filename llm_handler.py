import re

class SimpleLLM:
    def __init__(self):
        print("Using FREE rule-based AI detection")
        
        self.phishing_keywords = ["urgent", "immediately", "suspended", "verify", "confirm", "click here", "act now", "expires", "limited time"]
    
    def analyze_email(self, email_content):
        email_lower = email_content.lower()
        
        score = 0
        reasons = []
        
        urgent_count = sum(1 for word in self.phishing_keywords if word in email_lower)
        if urgent_count > 2:
            score += 3
            reasons.append("Contains " + str(urgent_count) + " urgency keywords")
        
        if "http" in email_lower and ("fake" in email_lower or "verify" in email_lower):
            score += 4
            reasons.append("Contains suspicious URL")
        
        if any(word in email_lower for word in ["verify", "confirm", "password"]):
            score += 2
            reasons.append("Requests verification")
        
        if score >= 4:
            return "PHISHING - This email is PHISHING because: " + ", ".join(reasons)
        else:
            return "SAFE - This email appears safe. Score: " + str(score) + "/10"
