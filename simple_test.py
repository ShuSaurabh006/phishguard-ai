from llm_handler import SimpleLLM

def simple_test():
    print("=== SIMPLE TEST ===")
    
    # Read the email
    with open("test_email.txt", "r") as f:
        email_content = f.read()
    
    print("Email content:")
    print(repr(email_content))  # This will show exactly what's in the file
    print("\nEmail content readable:")
    print(email_content)
    
    # Test the LLM directly
    llm = SimpleLLM()
    result = llm.analyze_email(email_content)
    print("\nLLM Result:")
    print(result)
    
    # Test structure checks
    email_lower = email_content.lower()
    print("\nStructure checks:")
    print("Has 'from:':", "from:" in email_lower)
    print("Has 'subject:':", "subject:" in email_lower)
    print("Has 'http':", "http" in email_lower)
    print("Has urgency words:", any(word in email_lower for word in ["urgent", "immediately", "suspended"]))

if __name__ == "__main__":
    simple_test()
