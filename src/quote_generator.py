from typing import Optional, Tuple, Dict
from .ai_service import AIService
from .storage import FirebaseStorage

class MotivationGenerator:
    def __init__(self):
        self.ai_service = AIService()
        self.storage = FirebaseStorage()
        self.valid_moods = ["happy", "anxious", "excited", "sad", "motivated", "tired"]

    def generate_and_save_quote(self, mood: str, context: Optional[str] = None) -> Dict:
        """Generate a quote using AI and save it to storage."""
        quote = self.ai_service.generate_quote(mood, context)
        quote_id = self.storage.save_quote(mood, quote, context)
        return {
            'id': quote_id,
            'quote': quote,
            'mood': mood,
            'context': context
        }

    def display_quote_history(self, mood: Optional[str] = None):
        """Display quote history, optionally filtered by mood."""
        quotes = (self.storage.get_quotes_by_mood(mood) if mood 
                 else self.storage.get_recent_quotes())
        
        if not quotes:
            print("\nNo quotes found.")
            return

        print("\nQuote History:")
        for quote in quotes:
            context_str = f" (Context: {quote['context']})" if quote.get('context') else ""
            print(f"\n{quote['timestamp']} | {quote['mood']}{context_str}\n{quote['quote']}")
            print(f"Quote ID: {quote['id']}")
