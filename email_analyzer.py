import pandas as pd
import numpy as np
from typing import Dict, Any
from llm_handler import SimpleLLM

class PhishGuardAI:
    def __init__(self):
        self.llm = SimpleLLM()
    
    def _check_structure(self, email_content: str) -> Dict[str, Any]:
        """Step 1: Check email structure"""
        print("\n=== STEP 1: STRUCTURE ANALYSIS ===")
        
        checks = {
            "check_type": ["has_sender", "has_subject", "has_links", "has_urgency"],
            "result": [
                "from:" in email_content.lower(),
                "subject:" in email_content.lower(), 
                "http" in email_content.lower(),
                any(word in email_content.lower() for word in ["urgent", "immediately", "suspended"])
            ]
        }
        
        checks_df = pd.DataFrame(checks)
        suspicious_count = checks_df["result"].sum()
        structure_score = suspicious_count / len(checks_df)
        
        print("Structure Analysis:", str(suspicious_count) + "/" + str(len(checks_df)) + " indicators found")
        for i, check in enumerate(checks["check_type"]):
            status = "FOUND" if checks["result"][i] else "NOT FOUND"
            print(f"  - {check}: {status}")
        
        return {
            "structure_score": structure_score,
            "suspicious_count": suspicious_count,
            "checks_df": checks_df
        }
    
    def _check_content(self, email_content: str) -> Dict[str, Any]:
        """Step 2: Check content with AI"""
        print("\n=== STEP 2: AI CONTENT ANALYSIS ===")
        
        analysis = self.llm.analyze_email(email_content)
        
        if "PHISHING" in analysis.upper():
            content_score = 0.8
            classification = "PHISHING"
        else:
            content_score = 0.2  
            classification = "SAFE"
        
        print("AI Classification:", classification)
        print("Analysis:", analysis)
        
        return {
            "content_score": content_score,
            "classification": classification,
            "analysis": analysis
        }
    
    def _make_decision(self, structure_result: Dict, content_result: Dict) -> Dict[str, Any]:
        """Step 3: Make final decision"""
        print("\n=== STEP 3: FINAL DECISION ===")
        
        scores = np.array([structure_result["structure_score"], content_result["content_score"]])
        weights = np.array([0.3, 0.7])
        final_score = np.average(scores, weights=weights)
        
        if final_score > 0.5:
            decision = "PHISHING DETECTED"
            risk_level = "HIGH" if final_score > 0.7 else "MEDIUM"
        else:
            decision = "SAFE"
            risk_level = "LOW"
        
        confidence_percent = "{:.1%}".format(final_score)
        print("Structure Score:", "{:.1%}".format(structure_result["structure_score"]))
        print("Content Score:", "{:.1%}".format(content_result["content_score"]))
        print("Final Decision:", decision, "(" + confidence_percent + " confidence)")
        
        return {
            "final_score": final_score,
            "decision": decision,
            "risk_level": risk_level,
            "confidence": confidence_percent
        }
    
    def analyze_email(self, email_content: str) -> Dict[str, Any]:
        """Main analysis function - step by step"""
        print("Starting PhishGuard-AI Analysis Pipeline...")
        print("Email length:", len(email_content), "characters")
        
        # Step 1: Structure Analysis
        structure_result = self._check_structure(email_content)
        
        # Step 2: Content Analysis  
        content_result = self._check_content(email_content)
        
        # Step 3: Final Decision
        decision_result = self._make_decision(structure_result, content_result)
        
        return {
            "decision": decision_result["decision"],
            "confidence": decision_result["confidence"],
            "risk_level": decision_result["risk_level"],
            "explanation": content_result["analysis"]
        }
