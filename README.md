# AutoMantis

A Telegram bot that sends aptitude questions to users, tracks their performance, and maintains answer streaks. The bot extracts and curates multiple-choice questions from PDF documents and delivers them via interactive Telegram polls.

**Access the bot**: https://t.me/automantis_bot

## Features

- **Interactive Telegram Polls**: Sends multiple-choice questions via Telegram polls
- **Question Extraction**: Automatically extracts questions from PDF and DOCX files
- **Smart Question Curation**: Cleans and normalizes questions, infers topics, and validates content
- **Streak Tracking**: Maintains user streaks and performance history
- **Question Bank Management**: Categorized questions across various topics:
  - Percentages
  - Time and Work
  - Time and Distance
  - Profit and Loss
  - Simple Interest
  - General Aptitude
- **State Persistence**: Saves poll data, user progress, and streak information

## Project Structure

```
AutoMantis/
├── mantis.py                      # Main Telegram bot application
├── extract_questions_from_pdfs.py # PDF/DOCX extraction and processing
├── curate_questions.py            # Question cleaning and normalization
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── data/
    ├── questions_from_pdf.json    # Extracted questions from PDFs
    └── questions.json             # Curated questions database
```

## Installation

1. **Clone the repository** (or set up the project directory)

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** - Create a `.env` file in the project root:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   QUESTION_COUNT=3
   QUESTION_DB_FILE=data/questions_from_pdf.json
   STREAK_STATE_FILE=streaks.json
   MAX_TRACKED_POLLS=300
   ```

   - `TELEGRAM_BOT_TOKEN`: Token from BotFather on Telegram
   - `TELEGRAM_CHAT_ID`: Your Telegram chat ID
   - `QUESTION_COUNT`: Number of questions to send per poll (default: 3)
   - `QUESTION_DB_FILE`: Path to the questions database
   - `STREAK_STATE_FILE`: File to store user streaks and poll data
   - `MAX_TRACKED_POLLS`: Maximum number of polls to track

## Usage

### Run the Bot
```bash
python mantis.py
```

### Extract Questions from PDFs
```bash
python extract_questions_from_pdfs.py
```

This will process PDF and DOCX files in the `data/` directory and extract questions into `questions_from_pdf.json`.

### Curate Questions
```bash
python curate_questions.py
```

This script cleans, normalizes, and validates questions, removing duplicates and fixing formatting issues.

## Dependencies

- `python-dotenv` - Load environment variables from `.env`
- `requests` - HTTP library for Telegram API calls
- `pypdf` - Extract text from PDF files
- `python-docx` - Extract text from DOCX files

## How It Works

1. **Question Loading**: The bot loads questions from the question database or built-in question bank
2. **Question Selection**: Randomly selects questions based on user preferences
3. **Poll Creation**: Sends interactive polls via Telegram
4. **Response Tracking**: Receives and stores user responses (via Telegram webhooks or polling)
5. **Streak Management**: Maintains user streaks based on correct/incorrect answers
6. **State Persistence**: Saves all progress to JSON files

## Configuration

All configuration is done through the `.env` file. The bot validates all required settings on startup.

## File Descriptions

- **mantis.py**: Main bot application with Telegram integration, poll management, and streak tracking
- **extract_questions_from_pdfs.py**: Extracts questions from PDF/DOCX files and saves to JSON
- **curate_questions.py**: Cleans question text, normalizes formats, removes duplicates
- **requirements.txt**: Python package dependencies

## Example Questions

The bot includes embedded question banks covering:
- **Percentages**: Percentage calculations, increases, discounts
- **Time and Work**: Work rates, combined work calculations
- **Time and Distance**: Speed, distance, relative motion
- **Profit and Loss**: Profit/loss calculations, pricing
- **Simple Interest**: Interest calculations with formulas

## Troubleshooting

- **Missing `.env` file**: Create a `.env` file with required variables
- **Telegram connection issues**: Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
- **PDF extraction issues**: Ensure files are in `data/` directory and readable
- **State file errors**: Delete `streaks.json` to reset user data

## Future Enhancements

- User leaderboards
- Difficulty levels
- Scheduled question delivery
- Question statistics and analytics
- Multiple language support

## License

[Add your license information here]

## Author

[Add author information here]" 
