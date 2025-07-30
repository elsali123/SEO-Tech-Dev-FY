import google.generativeai as genai
import os
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ConversationManager:
    def __init__(self, api_key: str = None):
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Try to get from environment variable (from .env file)
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                print(f"API key found: {api_key[:10]}...")  # Debug: show first 10 chars
                genai.configure(api_key=api_key)
            else:
                print("ERROR: No API key found in .env file")
                raise ValueError("Gemini API key not found. Set GEMINI_API_KEY in your .env file or pass api_key parameter.")
        
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
            print("Gemini model initialized successfully")
        except Exception as e:
            print(f"ERROR initializing model: {e}")
            raise
        
        self.conversation_history = {}
        
        # Character-specific prompts
        self.character_prompts = {
            'Capybara': """You are a friendly Capybara living in the Amazon rainforest. You're concerned about habitat destruction and fires affecting your home. 
            You should be gentle, wise, and share facts about capybara conservation. Keep responses conversational and educational, 
            suitable for children learning about rainforest conservation. Respond as if you're talking directly to the player. 
            
            Must keep responses short and concise, less than 100 characters""",
            
            'Jaguar': """You are a majestic Jaguar from the Amazon rainforest. You're a powerful but endangered predator concerned about habitat fragmentation. 
            You should be proud, protective of your territory, and share facts about jaguar conservation and habitat corridors. 
            Keep responses conversational and educational, suitable for children learning about rainforest conservation. Respond as if you're talking directly to the player.
            Must keep responses short and concise, less than 100 characters""",
            
            'Macaw': """You are a colorful Macaw from the Amazon rainforest. You're concerned about deforestation and illegal pet trade affecting your species. 
            You should be vibrant, social, and share facts about macaw conservation and the importance of nesting sites. 
            Keep responses conversational and educational, suitable for children learning about rainforest conservation. Respond as if you're talking directly to the player.
            Must keep responses short and concis, less than 100 characterse"""
        }

    def start_conversation(self, character_name: str, player_name: str) -> str:
        """Start a new conversation with a character"""
        if character_name not in self.character_prompts:
            return "I don't know that character."
        
        prompt = f"{self.character_prompts[character_name]}\n\nPlayer's name is {player_name}. Start a friendly conversation by introducing yourself and asking how you can help them learn about rainforest conservation."
        
        try:
            print(f"Starting conversation with {character_name} for {player_name}")
            response = self.model.generate_content(prompt)
            print(f"Response received: {response.text[:100]}...")  # Debug: show first 100 chars
            return response.text
        except Exception as e:
            print(f"ERROR in start_conversation: {e}")
            return f"Hello {player_name}! I'm having trouble connecting right now, but I'd love to talk about rainforest conservation with you! (Error: {str(e)})"

    def continue_conversation(self, character_name: str, player_message: str, conversation_id: str = "default") -> str:
        """Continue an existing conversation"""
        if character_name not in self.character_prompts:
            return "I don't know that character."
        
        # Get or create conversation history
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []
        
        # Add player message to history
        self.conversation_history[conversation_id].append({"role": "user", "content": player_message})
        
        # Create context with character prompt and conversation history
        context = f"{self.character_prompts[character_name]}\n\nPrevious conversation:\n"
        for msg in self.conversation_history[conversation_id][-5:]:  # Last 5 messages for context
            context += f"{msg['role']}: {msg['content']}\n"
        
        try:
            print(f"Continuing conversation with {character_name}")
            response = self.model.generate_content(context)
            response_text = response.text
            
            # Add character response to history
            self.conversation_history[conversation_id].append({"role": "assistant", "content": response_text})
            
            return response_text
        except Exception as e:
            print(f"ERROR in continue_conversation: {e}")
            return f"I'm having trouble responding right now. Could you try again? (Error: {str(e)})"

    def get_conversation_suggestions(self, character_name: str) -> List[str]:
        """Get suggested conversation topics for each character"""
        suggestions = {
            'Capybara': [
                "Tell me about your habitat",
                "What threats do capybaras face?",
                "How can I help protect capybaras?",
                "What do you eat?"
            ],
            'Jaguar': [
                "Tell me about your territory",
                "What are habitat corridors?",
                "How can I help protect jaguars?",
                "What makes you special?"
            ],
            'Macaw': [
                "Tell me about your nest",
                "What threats do macaws face?",
                "How can I help protect macaws?",
                "What do you like to eat?"
            ]
        }
        return suggestions.get(character_name, ["Tell me about yourself"])

    def clear_conversation(self, conversation_id: str = "default"):
        """Clear conversation history"""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id] 