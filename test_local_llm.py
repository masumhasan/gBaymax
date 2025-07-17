"""
Test script for local Llama.cpp model

This script tests the local model functionality without the full agent.
"""

import asyncio
import logging
from local_llm import create_local_llm
from model_config import list_available_models, validate_model_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_local_model():
    """Test the local model functionality"""
    print("🧪 Testing Local LLM Model")
    print("=" * 40)
    
    # Check available models
    print("\n📋 Available Models:")
    models = list_available_models()
    for name, description, exists in models:
        status = "✅" if exists else "❌"
        print(f"  {status} {name}: {description}")
    
    # Find a valid model
    valid_model = None
    for name, _, exists in models:
        if exists:
            valid_model = name
            break
    
    if not valid_model:
        print("\n❌ No valid model found! Please check your models directory.")
        return False
    
    print(f"\n🎯 Using model: {valid_model}")
    
    try:
        # Create the model
        print("\n🔧 Loading model...")
        llm = create_local_llm(model_name=valid_model)
        print("✅ Model loaded successfully!")
        
        # Test basic generation
        print("\n🧪 Testing basic generation...")
        test_prompt = "Hello, I am Baymax. How can I help you today?"
        
        response = await llm.generate_response(test_prompt)
        print(f"📤 Prompt: {test_prompt}")
        print(f"📥 Response: {response}")
        
        # Test Baymax personality
        print("\n🧪 Testing Baymax personality...")
        baymax_prompt = """You are Baymax, the friendly healthcare companion from Big Hero 6.
        
User: Hello Baymax, how are you?

Baymax:"""
        
        response = await llm.generate_response(baymax_prompt)
        print(f"📤 Baymax test:")
        print(f"📥 Response: {response}")
        
        # Test multiple responses
        print("\n🧪 Testing multiple responses...")
        test_messages = [
            "What's the weather like?",
            "I'm feeling sad today",
            "Thank you for your help",
            "Can you search for something?"
        ]
        
        for msg in test_messages:
            prompt = f"""You are Baymax, a healthcare companion. Be helpful and caring.

User: {msg}

Baymax:"""
            response = await llm.generate_response(prompt)
            print(f"  👤 User: {msg}")
            print(f"  🤖 Baymax: {response}")
            print()
        
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing model: {e}")
        logger.error(f"Model test failed: {e}")
        return False

async def interactive_test():
    """Interactive test with the local model"""
    print("\n🎮 Interactive Test Mode")
    print("=" * 40)
    print("Type 'quit' to exit")
    
    try:
        llm = create_local_llm()
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                # Create Baymax-style prompt
                prompt = f"""You are Baymax, the friendly healthcare companion from Big Hero 6.

Your personality:
- Speak softly, politely, and helpfully
- Use humor from the movie
- Always offer support for physical or emotional health
- Be caring and gentle

User: {user_input}

Baymax:"""
                
                print("🤖 Baymax: ", end="", flush=True)
                response = await llm.generate_response(prompt)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to create model: {e}")

def main():
    """Main function"""
    print("🚀 Local LLM Test Suite")
    print("=" * 40)
    
    # Run basic tests
    success = asyncio.run(test_local_model())
    
    if success:
        print("\n🎉 Basic tests completed successfully!")
        
        # Ask if user wants interactive mode
        try:
            choice = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                asyncio.run(interactive_test())
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
    else:
        print("\n❌ Basic tests failed. Please check your setup.")

if __name__ == "__main__":
    main()
