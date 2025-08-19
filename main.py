from email_analyzer import PhishGuardAI

def main():
    print("PhishGuard-AI - FREE Phishing Detection")
    print("No API key required - Uses smart rule-based AI")
    print("=" * 50)
    
    print("Initializing PhishGuard-AI...")
    analyzer = PhishGuardAI()
    
    print("Testing with example phishing email...")
    with open("test_email.txt", "r") as f:
        email_content = f.read()
    
    result = analyzer.analyze_email(email_content)
    
    print("\n" + "="*50)
    print("FINAL RESULT:")
    print("Decision:", result["decision"])
    print("Confidence:", result["confidence"])  
    print("Risk Level:", result["risk_level"])
    print("Explanation:", result["explanation"])
    print("="*50)

if __name__ == "__main__":
    main()
