"""
Script to check available Gemini models for your API key
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in environment variables!")
    print("Please check your .env file.")
    exit(1)

genai.configure(api_key=api_key)

print("=" * 60)
print("CHECKING AVAILABLE GEMINI MODELS")
print("=" * 60)
print()

try:
    # List all available models
    print("Fetching available models...\n")
    models = genai.list_models()
    
    chat_models = []
    embedding_models = []
    
    for model in models:
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Supported Methods: {model.supported_generation_methods}")
        print()
        
        # Check if it supports generateContent (for chat)
        if 'generateContent' in model.supported_generation_methods:
            chat_models.append(model.name)
        
        # Check if it supports embedContent (for embeddings)
        if 'embedContent' in model.supported_generation_methods:
            embedding_models.append(model.name)
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print()
    
    print(f"✅ Models supporting CHAT (generateContent): {len(chat_models)}")
    for model in chat_models:
        print(f"   - {model}")
    print()
    
    print(f"✅ Models supporting EMBEDDINGS (embedContent): {len(embedding_models)}")
    for model in embedding_models:
        print(f"   - {model}")
    print()
    
    if chat_models:
        # Extract just the model name without 'models/' prefix
        recommended_chat = chat_models[0].replace('models/', '')
        print("=" * 60)
        print("RECOMMENDED CONFIGURATION")
        print("=" * 60)
        print()
        print(f"For config.py, use:")
        print(f"  GEMINI_MODEL = '{recommended_chat}'")
        if embedding_models:
            print(f"  GEMINI_EMBEDDING_MODEL = '{embedding_models[0]}'")
    else:
        print("⚠️  WARNING: No models support generateContent!")
        print("Your API key may not have access to Gemini models.")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    print()
    print("This could mean:")
    print("1. Your API key is invalid")
    print("2. Your API key doesn't have access to any models")
    print("3. There's a network/connectivity issue")
