#!/usr/bin/env python3
"""
Test script for Gemini API integration
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_connection():
    """Test if Gemini API is working"""
    print("Testing Gemini API connection...")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ ERROR: No GEMINI_API_KEY found in .env file")
        print("Please create a .env file with: GEMINI_API_KEY=your_actual_key")
        return False
    
    print(f"✅ API key found: {api_key[:10]}...")
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Create model
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        print("✅ Model created successfully")
        
        # Test simple generation
        response = model.generate_content("Say 'Hello, world!' in a friendly way.")
        print(f"✅ Test response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_connection()
    if success:
        print("\n🎉 Gemini API is working correctly!")
    else:
        print("\n💥 Gemini API test failed. Check your setup.") 