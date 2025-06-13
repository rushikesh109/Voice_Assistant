import google.generativeai as genai
import speech_recognition as sr
import os
import webbrowser
import requests
import urllib.parse
from datetime import date, datetime
import pygame
import sys
import platform
import re
from gtts import gTTS
import playsound

# ✅ Gemini API Setup
genai.configure(api_key="AIzaSyDIqMo_kDdPef6fIlFzqOKAHmRIgWAdcZc")
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ✅ OpenWeatherMap Setup
WEATHER_API_KEY = "d60071ca6916b9d6c78fe204c02811b9"
CITY = "Pune"

# ✅ Pygame Init
pygame.mixer.init()
today = str(date.today())

# ✅ Gemini Chat
def chatfun(talk):
    try:
        chat_history = [{'role': msg['role'], 'parts': [msg['content']]} for msg in talk]
        response = model.generate_content(chat_history)
        text_response = response.text if hasattr(response, 'text') and response.text else None
        print("[Gemini RAW Response]:", text_response)

        if not text_response or len(text_response.strip()) < 5:
            text_response = "I'm sorry, I didn't get that."

        talk.append({'role': 'model', 'content': text_response})
        return talk
    except Exception as e:
        print(f"[Gemini Error]: {e}")
        talk.append({'role': 'model', 'content': "Something went wrong with my brain!"})
        return talk

# ✅ TTS Speak with gTTS
def speak_text(text):
    try:
        text = re.sub(r'[^\w\s.,?!]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        print("AI:", text)
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        playsound.playsound("response.mp3")
    except Exception as e:
        print(f"[TTS Error]: {e}")

# ✅ Save Log
def append2log(text):
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a") as f:
        f.write(text + "\n")

# ✅ Weather Info
def get_weather():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url).json()
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"It's currently {temp}°C with {desc} in {CITY}."
    except Exception as e:
        return "I couldn't get the weather right now."

# ✅ Open Apps / Websites
def open_app_or_website(command):
    command = command.lower()
    try:
        if "play" in command and "youtube" in command:
            song = command.split("play", 1)[1].split("on youtube")[0].strip()
            if song:
                query = urllib.parse.quote(song)
                url = f"https://www.youtube.com/results?search_query={query}"
                webbrowser.open(url)
                return f"Playing {song} on YouTube"

        elif "youtube" in command:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube"
        elif "google" in command:
            webbrowser.open("https://www.google.com")
            return "Opening Google"
        elif "notepad" in command and platform.system() == "Windows":
            os.system("notepad")
            return "Opening Notepad"
        elif "calculator" in command and platform.system() == "Windows":
            os.system("calc")
            return "Opening Calculator"
        elif "command prompt" in command or "cmd" in command:
            if platform.system() == "Windows":
                os.system("start cmd")
                return "Opening Command Prompt"
        return None
    except Exception as e:
        print(f"[App Error]: {e}")
        return "Could not open the requested app."

# ✅ Main Loop
def main():
    global today
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400

    talk = []
    sleeping = True

    while True:
        with mic as source:
            rec.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")

            try:
                audio = rec.listen(source, timeout=10, phrase_time_limit=15)
                text = rec.recognize_google(audio)
                print(f"Heard: {text}")

                if sleeping:
                    if "alexa" in text.lower():
                        sleeping = False
                        today = str(date.today())
                        talk = []
                        speak_text("Hi there, how can I help?")
                        continue
                    else:
                        continue
                else:
                    request = text.lower()

                    if "that's all" in request or "stop" in request:
                        append2log(f"You: {request}\n")
                        speak_text("Bye now")
                        sleeping = True
                        continue

                    if "alexa" in request:
                        request = request.split("alexa", 1)[1].strip()

                    append2log(f"You: {request}\n")

                    if "time" in request:
                        now = datetime.now().strftime("%I:%M %p")
                        speak_text(f"The time is {now}")
                        continue

                    if "weather" in request:
                        weather = get_weather()
                        speak_text(weather)
                        continue

                    response = open_app_or_website(request)
                    if response:
                        speak_text(response)
                        continue

                    talk.append({'role': 'user', 'content': request})
                    talk = chatfun(talk)
                    response = talk[-1]['content'].strip()
                    append2log(f"AI: {response}\n")

                    # ✅ Speak only first 25 words of response
                    max_words = 25
                    words = response.split()
                    short_response = " ".join(words[:max_words])
                    if len(words) > max_words:
                        short_response += "... Let me know if you want to hear more."

                    speak_text(short_response)

            except sr.UnknownValueError:
                print("Didn't catch that.")
            except sr.RequestError as e:
                print(f"Google Speech Error: {e}")
            except Exception as e:
                print(f"[ERROR]: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[EXIT] Voice assistant terminated.")
        sys.exit(0)
