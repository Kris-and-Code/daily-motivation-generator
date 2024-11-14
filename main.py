import datetime
import os
from typing import List, Tuple

class MotivationGenerator:
    def __init__(self):
        self.quotes_file = "quotes.txt"
        self.mood_quotes = {
            "happy": [
                "Keep spreading that joy! Your happiness lights up the world around you.",
                "The world is better with your smile in it. Keep shining!",
            ],
            "anxious": [
                "Take a deep breath. This moment shall pass, and you are stronger than you think.",
                "Small steps forward are still progress. You've got this!",
            ],
            "excited": [
                "Channel that energy into something amazing! The world is full of possibilities.",
                "Your enthusiasm is contagious! Use it to inspire others.",
            ],
            
        }

    def get_user_mood(self) -> str:
        """Prompt user for their current mood."""
        print("\nHow are you feeling today?")
        print("Suggested moods: happy, anxious, excited")
        return input("Your mood: ").lower().strip()

    def generate_quote(self, mood: str) -> str:
        """Generate a quote based on the user's mood."""
        if mood in self.mood_quotes:
            return self.mood_quotes[mood][0]
        return "Every day is a new opportunity to grow and learn."

    def save_quote(self, mood: str, quote: str):
        """Save the quote with timestamp to file."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.quotes_file, "a") as f:
            f.write(f"{timestamp} | Mood: {mood} | Quote: {quote}\n")

    def read_past_quotes(self) -> List[Tuple[str, str, str]]:
        """Read and return past quotes from file."""
        if not os.path.exists(self.quotes_file):
            return []
        
        quotes = []
        with open(self.quotes_file, "r") as f:
            for line in f:
                parts = line.strip().split(" | ")
                if len(parts) == 3:
                    quotes.append((parts[0], parts[1], parts[2]))
        return quotes

    def run(self):
        """Main program loop."""
        # Display past quotes
        past_quotes = self.read_past_quotes()
        if past_quotes:
            print("\nYour previous quotes:")
            for timestamp, mood, quote in past_quotes[-3:]:  # Show last 3 quotes
                print(f"{timestamp}: {quote}")

        # Get current mood and generate quote
        mood = self.get_user_mood()
        quote = self.generate_quote(mood)
        
        print(f"\nYour motivational quote for today:\n{quote}")
        self.save_quote(mood, quote)

        # Ask about daily reminders
        want_daily = input("\nWould you like to receive daily quotes? (yes/no): ").lower()
        if want_daily == "yes":
            print("Great! Remember to run this program daily for your motivation boost.")

if __name__ == "__main__":
    generator = MotivationGenerator()
    generator.run() 