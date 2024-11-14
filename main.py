from src.quote_generator import MotivationGenerator
import schedule
import time
import argparse
import firebase_admin

def main():
    parser = argparse.ArgumentParser(description='Daily Motivation Generator')
    parser.add_argument('--history', action='store_true', help='View quote history')
    parser.add_argument('--mood', type=str, help='Filter history by mood')
    args = parser.parse_args()

    generator = MotivationGenerator()

    if args.history:
        generator.display_quote_history(args.mood)
        return

    # Get user input and generate quote
    # mood, context = generator.get_user_input()
    # quote = generator.generate_and_save_quote(mood, context)

    mood = input("How are you feeling today? (e.g., happy, sad, motivated, anxious): ").lower()
    context = input("Tell me about your day: ")

    quote = generator.generate_and_save_quote(mood, context)
    
    print(f"\nYour personalized motivational quote:\n{quote}")
    
    # Ask about scheduling
    if input("\nWould you like to schedule daily motivational quotes? (yes/no): ").lower() == 'yes':
        schedule_daily_quotes(generator)

def schedule_daily_quotes(generator):
    """Schedule daily quote generation at a specific time."""
    schedule.every().day.at("09:00").do(lambda: automated_quote_generation(generator))
    
    print("\nDaily quotes scheduled for 9:00 AM. Keep this program running to receive them.")
    print("Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nQuote scheduling cancelled.")

def automated_quote_generation(generator):
    """Automated quote generation for scheduled runs."""
    quote = generator.generate_and_save_quote("motivated")
    print(f"\n[Daily Quote] {quote}")

if __name__ == "__main__":
    main() 