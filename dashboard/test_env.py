from dotenv import load_dotenv
import os

load_dotenv()

def test_env():
    required_vars = [
        'OPENAI_API_KEY',
        'METALS_API_KEY',
        'TELEGRAM_BOT_TOKEN',
        'MANAGER_BOT_TOKEN'
    ]
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
            
    if missing:
        print(f"❌ Missing variables: {', '.join(missing)}")
    else:
        print("✅ All required variables are set!")

if __name__ == "__main__":
    test_env()