import openai
import logging
from config import *

class Assistant:
    def __init__(self):
        openai.api_key = OPENAI_API_KEY
        self.context = []
        self.model = DEFAULT_MODEL
        logging.info(f"Assistant initialized with model: {self.model}")
    
    def start(self):
        logging.info(f"Starting {APP_NAME}")
        try:
            while True:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                response = self.process_input(user_input)
                print(f"Assistant: {response}")
        except KeyboardInterrupt:
            logging.info("Assistant stopped by user")
    
    def process_input(self, user_input):
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": user_input}],
                max_tokens=MAX_TOKENS
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error processing input: {e}")
            return "I apologize, but I encountered an error processing your request."