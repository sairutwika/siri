import speech_recognition as sr
from gtts import gTTS
import datetime
import webbrowser
import random
import wikipedia
import os
import tempfile
import streamlit as st

# ------------------ Speak Function ------------------
def speak(text):
    """Convert text to speech and play it in Streamlit."""
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, format='audio/mp3')
    except Exception as e:
        st.error(f"Error speaking: {e}")
    return text

# ------------------ Listen Function ------------------
def listen():
    """Listen to the user's voice and return recognized text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("🎧 Listening...")
        try:
            audio = r.listen(source, timeout=5)
            command = r.recognize_google(audio)
            print(f"🗣️ You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            return "Listening timeout."
        except sr.UnknownValueError:
            return "Sorry, I didn't catch that."
        except sr.RequestError:
            return "Network error."

# ------------------ Command Processor ------------------
def process_command(command):
    if 'what is time' in command or 'time now' in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return speak(f"The time is {now}")

    elif 'today date' in command or 'what is date' in command:
        today = datetime.date.today().strftime("%B %d, %Y")
        return speak(f"Today's date is {today}")

    elif 'open google' in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return "Opened Google"

    elif 'play music' in command or 'play song' in command:
        speak("Playing music on YouTube")
        webbrowser.open("https://www.youtube.com/results?search_query=top+music")
        return "Playing music"

    elif 'your name' in command or 'who are you' in command:
        return speak("I am your Baby Siri Voice Assistant")

    elif 'how are you' in command:
        return speak("I am feeling fantastic! Thanks for asking.")

    elif 'thank you' in command:
        return speak("You're welcome!")

    elif 'search for' in command:
        query = command.replace("search for", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return speak(f"Searching for {query}")

    elif 'search wikipedia for' in command:
        query = command.replace("search wikipedia for", "").strip()
        try:
            summary = wikipedia.summary(query, sentences=2)
            return speak(summary)
        except:
            return speak("Sorry, I couldn't find anything on Wikipedia.")

    elif 'joke' in command:
        jokes = [
            "Why don’t scientists trust atoms? Because they make up everything.",
            "Why did the computer go to therapy? It had too many bytes of emotional data.",
            "What do you call fake spaghetti? An impasta!"
        ]
        return speak(random.choice(jokes))

    elif 'motivate me' in command or 'quote' in command:
        quotes = [
            "Believe in yourself.",
            "Hard work beats talent when talent doesn't work hard.",
            "Stay focused and never give up!"
        ]
        return speak(random.choice(quotes))

    elif 'take a note' in command:
        speak("What should I write?")
        note = listen()
        try:
            with open("notes.txt", "a") as f:
                f.write(f"{datetime.datetime.now()}: {note}\n")
            return speak("Note saved.")
        except:
            return speak("Failed to save the note.")

    elif 'stop' in command or 'exit' in command or 'go to hell' in command:
        return speak("Bye Bye, You also go to hell")

    else:
        return speak("Sorry, I can't do this yet.")
