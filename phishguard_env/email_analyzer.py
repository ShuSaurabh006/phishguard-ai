"""
PhishGuard-AI Core Analyzer
Uses LangGraph for step-by-step reasoning
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from llm_handler import SimpleLLM

class EmailState(dict):
    """Simple state for our analysis pipeline"""
    pass

class PhishGuardAI:
    def __init__(self):
        self.llm = SimpleLLM()
        self.graph = self._build_analysis_graph()
    
    def _build_analysis_graph(self):
        """Create simple LangGraph pipeline"""
        workflow = StateGraph(EmailState)
        
        # Add analysis steps
        workflow.add_node("check_structure", self._check_structure)
        workflow.add_node("check_content", self._check_content)  
        workflow.add_node("make_decision", self._make_decision)
        
        # Connect the steps
        workflow.set_entry_point("check_structure")
        workflow.add_edge("check_structure", "check_content")
        workflow.add_edge("check_content", "make_decision")
        workflow.add_edge("make_decision", END)
        
        return workflow.compile()
    
    def _check_structure(self, state: EmailState) -> EmailState:
        """Step 1: Check email structure"""
        email = state["email_content"]
        
        # Simple checks using pandas
        checks_data = {
            "check_type": ["has_sender", "has_subject", "has_links", "has_urgency"],
            "result": [
                "from:" in email.lower(),
                "subject:" in email.lower(), 
                "http" in email.lower(),
                any(word in email.lower() for word in ["urgent", "immediately", "suspended"])
            ]
        }
        
        checks_df = pd.DataFrame(checks_data)
        
        # Count suspicious indicators
        suspicious_count = checks_df["result"].sum()
        
        state["structure_score"] = suspicious_count / len(checks_df)
        state["structure_checks"] = checks_df
        
        print(f"📧 Structure Analysis: {suspicious_count}/{len(checks_df)} indicators")
        return state
    
    def _check_content(self, state: EmailState) -> EmailState:
        """Step 2: Check content with AI"""
        email = state["email_content"]
        
        # Use LLM to analyze content semantics
        analysis = self.llm.analyze_email(email)
        
        # Extract key info (simple parsing)
        if "PHISHING" in analysis.upper():
            content_score = 0.8
            classification = "PHISHING"
        else:
            content_score = 0.2  
            classification = "SAFE"
        
        state["content_score"] = content_score
        state["content_analysis"] = analysis
        state["ai_classification"] = classification
        
        print(f"🧠 AI Analysis: {classification}")
        return state
    
    def _make_decision(self, state: EmailState) -> EmailState:
        """Step 3: Make final decision"""
        
        # Simple scoring with numpy
        scores = np.array([
            state["structure_score"],
            state["content_score"]
        ])
        
        # Weight the scores (structure 30%, content 70%)
        weights = np.array([0.3, 0.7])
        final_score = np.average(scores, weights=weights)
        
        # Make decision
        if final_score > 0.5:
            decision = "🚨 PHISHING"
            risk_level = "HIGH" if final_score > 0.7 else "MEDIUM"
        else:
            decision = "✅ SAFE"
            risk_level = "LOW"
        
        state["final_score"] = final_score
        state["decision"] = decision
        state["risk_level"] = risk_level
        
        print(f"🎯 Final Decision: {decision} ({final_score:.1%} confidence)")
        return state
    
    def analyze_email(self, email_content: str) -> Dict[str, Any]:
        """Main function to analyze an email"""
        print("\n🔄 Starting Analysis Pipeline...")
        
        # Create initial state
        initial_state = EmailState({
            "email_content": email_content,
            "structure_score": 0,
            "content_score": 0,
            "final_score": 0
        })
        
        # Run the graph
        final_state = self.graph.invoke(initial_state)
        
        # Return simple result
        return {
            "decision": final_state["decision"],
            "confidence": f"{final_state['final_score']:.1%}",
            "risk_level": final_state["risk_level"],
            "explanation": final_state["content_analysis"]
        }
