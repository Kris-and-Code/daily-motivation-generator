from openai import OpenAI
import os
from typing import Optional
from dotenv import load_dotenv

class AIService:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
    def generate_quote(self, mood: str, context: Optional[str] = None) -> str:
        """Generate a motivational quote using AI based on mood and optional context."""
        prompt = self._create_prompt(mood, context)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a motivational coach who provides personalized, 
                                    concise, and uplifting quotes. Keep responses under 100 
                                    characters and focus on actionable wisdom."""
                    },
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7,
                presence_penalty=0.6,  # Encourage more diverse responses
                frequency_penalty=0.3  # Reduce repetitive phrases
            )
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating AI quote: {e}")
            return self._get_fallback_quote(mood)
    
    def _create_prompt(self, mood: str, context: Optional[str] = None) -> str:
        base_prompt = f"Generate a motivational quote for someone feeling {mood}"
        if context:
            base_prompt += f" because {context}"
        return base_prompt
    
    def _get_fallback_quote(self, mood: str) -> str:
        """Provide a fallback quote if AI generation fails."""
        fallback_quotes = {
            "happy": "Your joy is contagious. Keep spreading happiness!",
            "sad": "Every storm runs out of rain. Better days are coming.",
            "anxious": "This too shall pass. Take one breath at a time.",
            "excited": "Channel your excitement into amazing achievements!",
            "tired": "Rest if you must, but don't quit. Tomorrow brings new energy.",
            "stressed": "You've overcome every challenge so far. This one too shall pass.",
            "motivated": "You're on the right path. Keep pushing forward!",
            "confused": "Clarity comes one step at a time. Trust the journey."
        }
        return fallback_quotes.get(mood.lower(), "Every moment is a fresh beginning.") 