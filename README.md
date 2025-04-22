# Automated-Personal-Assistant-AI-
Personal Assistant AI 
# Personal Assistant AI

A versatile personal assistant that combines voice commands, AI responses, calendar management, weather updates, and reminders.

## Features

- Voice and text command support
- OpenAI GPT integration for AI responses
- Google Calendar integration
- Weather checking functionality
- Web search capability
- Reminders system
- Voice output option

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/personal-assistant-ai.git
cd personal-assistant-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```plaintext
OPENAI_API_KEY=your_openai_api_key
```

4. Set up Google Calendar credentials:
- Get your `credentials.json` from Google Cloud Console
- Place it in the project root directory

## Usage

Run the assistant:
```bash
python personal_assistant.py
```

### Available Commands:
- "ask ai [question]" - Get AI responses using GPT
- "remind me to [task] at [time]" - Set reminders
- "check reminders" - View current reminders
- "search for [query]" - Search the web
- "weather in [city]" - Check weather
- "list calendar events" - View calendar events
- "add calendar event [summary], [description], [start_time], [end_time]" - Add event
- "schedule [summary], [start_time], [end_time]" - Quick schedule event

## License

MIT License - See LICENSE file for details
