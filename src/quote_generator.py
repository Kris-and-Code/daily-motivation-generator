from typing import Optional, Tuple, Dict
from .ai_service import AIService
from .storage import FirebaseStorage
import difflib
import string

class MotivationGenerator:
    def __init__(self):
        self.ai_service = AIService()
        self.storage = FirebaseStorage()
        self.valid_moods = ["happy", "anxious", "excited", "sad", "motivated", "tired"]

    def is_quote_unique(self, new_quote: str, mood: str) -> bool:
        """Check if the quote is unique for the given mood."""
        existing_quotes = self.storage.get_quotes_by_mood(mood)
        
        # Convert to lowercase for comparison and remove punctuation
        new_quote_normalized = new_quote.lower().translate(str.maketrans('', '', string.punctuation))
        
        for quote in existing_quotes:
            existing_quote_normalized = quote['quote'].lower().translate(
                str.maketrans('', '', string.punctuation)
            )
            
            # Check for similarity using difflib
            similarity = difflib.SequenceMatcher(
                None, new_quote_normalized, existing_quote_normalized
            ).ratio()
            
            if similarity > 0.7:  # 70% similarity threshold
                return False
        
        return True

    def generate_and_save_quote(self, mood: str, context: Optional[str] = None) -> Dict:
        """Generate a unique quote using AI and save it to storage."""
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            quote = self.ai_service.generate_quote(mood, context)
            
            if self.is_quote_unique(quote, mood):
                quote_id = self.storage.save_quote(mood, quote, context)
                return {
                    'id': quote_id,
                    'quote': quote,
                    'mood': mood,
                    'context': context,
                    'is_unique': True
                }
            
            attempts += 1
        
        # If we couldn't generate a unique quote after max attempts
        return {
            'error': 'Could not generate a unique quote after multiple attempts',
            'is_unique': False
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
