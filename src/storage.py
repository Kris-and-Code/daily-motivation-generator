import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
from typing import List, Tuple, Dict
import os
from dotenv import load_dotenv

class FirebaseStorage:
    def __init__(self):
        load_dotenv()
        # Initialize Firebase with your credentials
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.getenv('FIREBASE_CREDENTIALS_PATH'))
            firebase_admin.initialize_app(cred, {
                'databaseURL': os.getenv('FIREBASE_DATABASE_URL')
            })
        self.db_ref = db.reference('quotes')

    def save_quote(self, mood: str, quote: str, context: str = None, ai_generated: bool = True) -> str:
        """Save a quote to Firebase."""
        quote_data = {
            'timestamp': datetime.now().isoformat(),
            'mood': mood,
            'quote': quote,
            'context': context,
            'ai_generated': ai_generated
        }
        
        # Push the quote data and get the generated key
        new_quote_ref = self.db_ref.push(quote_data)
        return new_quote_ref.key

    def get_recent_quotes(self, limit: int = 5) -> List[Dict]:
        """Retrieve recent quotes from Firebase."""
        quotes = self.db_ref.order_by_child('timestamp').limit_to_last(limit).get()
        return self._format_quotes(quotes) if quotes else []

    def get_quotes_by_mood(self, mood: str) -> List[Dict]:
        """Retrieve quotes filtered by mood."""
        quotes = self.db_ref.order_by_child('mood').equal_to(mood).get()
        return self._format_quotes(quotes) if quotes else []

    def _format_quotes(self, quotes: Dict) -> List[Dict]:
        """Format quotes for consistent output."""
        return [
            {
                'id': quote_id,
                'timestamp': quote_data['timestamp'],
                'mood': quote_data['mood'],
                'quote': quote_data['quote'],
                'context': quote_data.get('context'),
                'ai_generated': quote_data.get('ai_generated', True)
            }
            for quote_id, quote_data in quotes.items()
        ]

    def delete_quote(self, quote_id: str) -> bool:
        """Delete a specific quote."""
        try:
            self.db_ref.child(quote_id).delete()
            return True
        except Exception as e:
            print(f"Error deleting quote: {e}")
            return False

    def update_quote(self, quote_id: str, updates: Dict) -> bool:
        """Update a specific quote."""
        try:
            self.db_ref.child(quote_id).update(updates)
            return True
        except Exception as e:
            print(f"Error updating quote: {e}")
            return False