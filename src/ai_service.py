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
                    {"role": "system", "content": "You are a motivational coach who provides personalized, concise, and uplifting quotes. Keep responses under 100 characters."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
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
            "anxious": "This too shall pass. Take one breath at a time.",
            "excited": "Channel your excitement into amazing achievements!",
            # Add more fallback quotes...
        }
        return fallback_quotes.get(mood, "Every moment is a fresh beginning.") 