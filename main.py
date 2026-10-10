from logging import exception

import speech_recognition as sr
import os
import webbrowser
from openai import OpenAI
from config import apikey
import datetime
import subprocess
import random

MODEL = "gpt-6-luna"
client = OpenAI(api_key=apikey)

# git update

def chat(query, chatStr):
    prompt = f"""
You are Fiona, a personal AI voice assistant created by ASIF.
If asked your name, reply: "I am Jarvis, a personal AI assistant."
Never call yourself ChatGPT. Keep responses natural and concise.

Previous conversation:
{chatStr}

User's question: {query}
"""

    response = client.responses.create(model=MODEL, input=prompt)
    answer = response.output_text
    say(answer)
    return answer


def ai(prompt):
    response = client.responses.create(model=MODEL, input=prompt)
    answer = response.output_text
    print(answer)
    return answer


def say(text):
    subprocess.run(["say","-v","Fiona", text])


class Exceptionxc(Exception):
    pass


def takeCommand():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.pause_threshold = 2
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio, language="en-scotland")
        print(f"You said: {query}")
        return query
    except Exception:
        return "Sorry, I couldn't understand."


if __name__ == "__main__":
    chatStr = ""
    say("Hello, I am Fiona.")

    sites = {
        "youtube": "https://youtube.com",
        "wikipedia": "https://wikipedia.com",
        "google": "https://google.com",
    }

    while True:
        print("Listening...")
        query = takeCommand().lower()

        if "exit" in query:
            say("Logging off.")
            break

        elif "reset chat" in query:
            chatStr = ""

        elif "open whatsapp" in query:
            os.system("open /Applications/WhatsApp.app")

        elif "open calculator" in query:
            os.system("open /System/Applications/Calculator.app")

        elif "open chrome" in query:
            os.system("open /Applications/Google Chrome.app")

        elif "the time" in query:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"The time is {current_time}.")

        elif any(f"open {site}" in query for site in sites):
            for site, url in sites.items():
                if f"open {site}" in query:
                    say(f"Opening {site} sir...")
                    webbrowser.open(url)
                    break

        elif "generate" in query:
            ai(query)

        else:
            answer = chat(query, chatStr)
            chatStr += f"\nUser: {query}\nJarvis: {answer}"
