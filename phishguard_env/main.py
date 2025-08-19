"""
PhishGuard-AI - FREE Phishing Detection
No API key needed! Works with smart rules!
"""

from email_analyzer import PhishGuardAI
import os

def main():
    print("🛡️ PhishGuard-AI - FREE Phishing Detection")
    print("🆓 No API key required - Uses smart rule-based AI!")
    print("=" * 60)
    
    # Create analyzer (no API key needed!)
    print("🔧 Initializing PhishGuard-AI...")
    analyzer = PhishGuardAI()
    
    # Test with example email
    print("🧪 Testing with example phishing email...")
    with open("test_email.txt", "r") as f:
        email_content = f.read()
    
    result = analyzer.analyze_email(email_content)
    
    print("\n" + "="*60)
    print("🎯 FINAL RESULT:")
    print(f"Decision: {result['decision']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"\nExplanation: {result['explanation']}")
    print("="*60)
    
    # Let user test their own email
    print("\n" + "="*60)
    print("🧪 Test Your Own Email:")
    print("Enter an email to analyze (or press Enter to skip):")
    
    try:
        user_input = input(">>> ")
        if user_input.strip():
            print("\n🔄 Analyzing your email...")
            result = analyzer.analyze_email(user_input)
            print(f"\n🎯 Result: {result['decision']} ({result['confidence']} confidence)")
            print(f"Explanation: {result['explanation']}")
    except:
        print("Skipping custom email test")

if __name__ == "__main__":
    main()
