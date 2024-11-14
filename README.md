# Personalized Daily Motivation Generator

A Python-based application that generates personalized motivational quotes based on your current mood and maintains a daily archive of your motivation journey.

## Features

- 🎯 Mood-based quote generation
- 📝 Daily quote archiving with timestamps
- 📖 Historical quote review
- ⏰ Daily reminder option
- 💾 Persistent storage in text file

daily-motivation-generator/
├── src/
│   ├── __init__.py
│   ├── quote_generator.py
│   ├── ai_service.py
│   └── storage.py
├── main.py
├── .env
├── quotes.txt
├── requirements.txt
└── README.md

## Prerequisites 🔧

Before running this project, make sure you have:

- Python 3.8 or higher
- Firebase Admin SDK credentials (for cloud features)
- Required Python packages

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up Firebase:
- Create a Firebase project
- Download your Firebase Admin SDK credentials JSON file
- Place it in the project root directory
- Update the path in `main.py`

```bash
python main.py

Follow the prompts to:
- Enter your current mood
- Provide context about your day
- Receive a personalized quote
- Choose whether to schedule daily quotes

### View Quote History
View all quotes:
```bash
python main.py --history
```

Filter quotes by mood:
```bash
python main.py --mood happy
```

Filter quotes by mood and view history:
```bash
python main.py --history --mood happy
```

### Example Interaction

How are you feeling today? (e.g., happy, sad, motivated, anxious): anxious
Tell me about your day: Have a big presentation tomorrow
Your personalized motivational quote:
Take a deep breath. This moment shall pass, and you are stronger than you think.
Would you like to schedule daily motivational quotes? (yes/no): yes