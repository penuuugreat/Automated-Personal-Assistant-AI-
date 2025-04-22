import datetime
import webbrowser
import random
import requests
import speech_recognition as sr
import pyttsx3
import time
from geopy.geocoders import Nominatim
from google_calendar import PersonalAssistant  
import openai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class PersonalAssistantAI:
    def __init__(self):
        self.reminders = []
        self.name = "Penuu"
        self.responses = {
            "greetings": ["Hello! How can I help you?", "Hi there!", "Greetings!"],
            "farewell": ["Goodbye!", "See you later!", "Have a nice day!"],
            "unknown": ["I'm not sure how to help with that.", "Could you rephrase that?", "I don't understand."]
        }
        self.weather_api_key = "393193db39520222f2ad22ad07c6d92b"
        self.calendar_assistant = PersonalAssistant("credentials.json") 
        self.openai = openai
        self.openai.api_key = os.getenv('OPENAI_API_KEY')
        if not self.openai.api_key:
            raise ValueError("OpenAI API key not found in environment variables")

    def greet(self):
        return random.choice(self.responses["greetings"])

    def farewell(self):
        return random.choice(self.responses["farewell"])

    def add_reminder(self, task, time):
        is_valid, result = self.validate_datetime(time)
        if not is_valid:
            return result
            
        self.reminders.append((task, result))
        return f"Reminder set: {task} at {result.strftime('%Y-%m-%d %H:%M')}"

    def check_reminders(self):
        now = datetime.datetime.now()
        due_reminders = [task for task, time in self.reminders if time <= now]
        if due_reminders:
           
            self.reminders = [(task, time) for task, time in self.reminders if task not in due_reminders]
            return f"Reminder: {', '.join(due_reminders)}"
        return "No reminders due right now."

    def list_calendar_events(self):
        return self.calendar_assistant.list_events()

    def add_calendar_event(self, summary, description, start_time, end_time):
      
        is_valid_start, start_result = self.validate_datetime(start_time)
        if not is_valid_start:
            return f"Invalid start time: {start_result}"
        
        is_valid_end, end_result = self.validate_datetime(end_time)
        if not is_valid_end:
            return f"Invalid end time: {end_result}"
        
        if end_result <= start_result:
            return "End time must be after start time"
        
        if (end_result - start_result) > timedelta(hours=24):
            return "Event duration cannot exceed 24 hours"
        
       
        start_time_str = start_result.strftime("%Y-%m-%d %H:%M")
        end_time_str = end_result.strftime("%Y-%m-%d %H:%M")
        
        return self.calendar_assistant.add_event(
            summary=summary,
            description=description,
            start_time=start_time_str,
            end_time=end_time_str
        )

    def search_web(self, query):
        try:
            formatted_query = "+".join(query.split())
            webbrowser.open(f"https://www.google.com/search?q={formatted_query}")
            return f"Searching Google for: {query}"
        except Exception as e:
            return "Sorry, I couldn't perform the search. Please try again."

    def get_current_location(self):
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            if data["status"] == "success":
                city = data["city"]
                return city
            else:
                return None
        except Exception as e:
            return None

    def check_weather(self, city=None):
        try:
            if not city:
                city = self.get_current_location()
                if not city:
                    return "Sorry, I couldn't determine your current location."
            
            url = f"https://api.openweathermap.org/data/2.5/weather?q=Kericho&units=metric&appid=393193db39520222f2ad22ad07c6d92b"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                weather = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                return f"The weather in {city} is {weather} with a temperature of {temperature}°C."
            else:
                return f"Sorry, I couldn't find weather information for {city}."
        except Exception as e:
            return f"Sorry, there was an error fetching the weather data: {str(e)}"

    def listen_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source)
                try:
                    return recognizer.recognize_google(audio)
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                except Exception as e:
                    print(f"Speech recognition error: {e}")
            except Exception as e:
                print(f"Error capturing audio: {e}")
            return ""

    def get_ai_response(self, prompt):
        try:
            response = self.openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error with OpenAI API: {str(e)}"

    def handle_command(self, command):
        command = command.lower()

        
        if "ask ai" in command or "ask gpt" in command:
            question = command.split("ask ai" if "ask ai" in command else "ask gpt")[1].strip()
            return self.get_ai_response(question)
        
       
        if any(word in command for word in ["hi", "hello", "hey"]):
            return self.greet()
        elif any(word in command for word in ["bye", "goodbye", "exit"]):
            return self.farewell()
        elif "remind me to" in command:
            task = command.split("remind me to")[1].split("at")[0].strip()
            time = command.split("at")[1].strip()
            return self.add_reminder(task, time)
        elif "check reminders" in command:
            return self.check_reminders()
        elif "search for" in command:
            query = command.split("search for")[1].strip()
            return self.search_web(query)
        elif "what is the weather in" in command or "weather in" in command:
            city = command.split("in")[-1].strip()
            return self.check_weather(city)
        elif "what is the weather now" in command:
            return self.check_weather()
        elif "list calendar events" in command:
            return self.list_calendar_events()
        elif "add calendar event" in command:
            try:
                parts = command.split("add calendar event")[1].strip().split(",")
                summary = parts[0].strip()
                description = parts[1].strip()
                start_time = parts[2].strip()
                end_time = parts[3].strip()
                return self.add_calendar_event(summary, description, start_time, end_time)
            except IndexError:
                return "Invalid format for adding a calendar event. Please provide summary, description, start time, and end time."
        elif "schedule" in command:
            try:
                parts = command.split("schedule")[1].strip().split(",")
                if len(parts) < 3:
                    return "Invalid format for scheduling. Please provide summary, start time, and end time."
                    
                summary = parts[0].strip()
                start_time = parts[1].strip()
                end_time = parts[2].strip()
                
                is_valid_start, start_result = self.validate_datetime(start_time)
                if not is_valid_start:
                    return f"Invalid start time: {start_result}"
                    
                is_valid_end, end_result = self.validate_datetime(end_time)
                if not is_valid_end:
                    return f"Invalid end time: {end_result}"
                
                events = self.list_calendar_events()
                for event in events:
                    event_start = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M")
                    event_end = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M")
                    if (event_start <= start_result <= event_end) or (event_start <= end_result <= event_end):
                        return f"Conflict detected with another event: {event['summary']} from {event['start_time']} to {event['end_time']}."
                
                return self.add_calendar_event(summary, "Scheduled via assistant", start_time, end_time)
            except IndexError:
                return "Invalid format for scheduling. Please provide summary, start time, and end time."
        else:
           
            return random.choice(self.responses["unknown"])

    def validate_datetime(self, date_str, time_format="%Y-%m-%d %H:%M"):
        try:
            
            date_str = date_str.strip()
            
           
            try:
                parsed_date = datetime.strptime(date_str, time_format)
            except ValueError:
                # Try alternate common formats
                alternate_formats = [
                    "%Y/%m/%d %H:%M",
                    "%d-%m-%Y %H:%M",
                    "%d/%m/%Y %H:%M"
                ]
                
                for fmt in alternate_formats:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    return False, f"Invalid date format. Please use {time_format} format (e.g., 2025-04-22 14:30)"
            
            
            if parsed_date < datetime.now():
                return False, "Date cannot be in the past"
                
            if parsed_date > datetime.now() + timedelta(days=365):
                return False, "Date cannot be more than 1 year in the future"
                
            return True, parsed_date
        except Exception as e:
            return False, f"Error parsing date: {str(e)}"

    def output_response(self, response, mode="text"):
        if mode == "voice":
            engine = pyttsx3.init()
            engine.say(response)
            engine.runAndWait()
        elif mode == "text":
            print(f"{self.name}: {response}")
        else:
            print("Invalid output mode selected. Defaulting to text.")
            print(f"{self.name}: {response}")


while True:
    output_mode = input("Would you like the output in 'voice' or 'text'? (default is 'text'): ").strip().lower()
    if output_mode in ["voice", "text", ""]:
        if output_mode == "":
            output_mode = "text"
        break
    else:
        print("Invalid input. Please enter 'voice' or 'text'.")

assistant = PersonalAssistantAI()
print(assistant.greet())
print("You can now use 'ask ai' followed by your question to get AI responses!")

while True:
    if output_mode == "voice":
        print(f"{assistant.name} is listening for a voice command...")

    user_input = assistant.listen_command() if output_mode == "voice" else input(f"{assistant.name}, your command: ").strip()

    if user_input.lower() in ["exit", "quit", "bye"]:
        farewell_message = assistant.farewell()
        assistant.output_response(farewell_message, mode=output_mode)
        break

    response = assistant.handle_command(user_input)
    assistant.output_response(response, mode=output_mode)