import speech_recognition as sr
import pyttsx3
import os
import datetime
import subprocess
import pywhatkit
import sys
import pyjokes
import ctypes
import requests
import time
import openai


from openai import OpenAI

client = OpenAI(api_key="sk-proj-FE1pCgRXXXXjApXS6rFXZ46xvbc-vFVfCgeTA2sgzf669V_C_U8fCocC1FiRk_w75MO1xEOyVNT3BlbkFJIlMp8BKiEnxxSEqZcYHR7lvYqq-o03_gpoQmCDFvru2TTvx8dq3WtAFIaj4ObESs797gluvEIA")

def smart_reply(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response.choices[0].message.content
        speak(reply)
    except Exception as e:
        speak("There was an error generating a smart reply.")
        print(f"Smart Reply Error: {e}")




engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

recognizer = sr.Recognizer()

def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning sir!")
    elif 12 <= hour < 18:
        speak("Good afternoon sir!")
    else:
        speak("Good evening sir!")
    speak("I am Jarvis, your assistant. How can I help you?")


def open_software(software_name):
    software_name = software_name.lower()
    if 'chrome' in software_name:
        speak('Opening Chrome...')
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
    elif 'edge' in software_name:
        speak('Opening Microsoft Edge...')
        subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])
    elif 'notepad' in software_name:
        speak('Opening Notepad...')
        subprocess.Popen(['notepad.exe'])
    elif 'calculator' in software_name:
        speak('Opening Calculator...')
        subprocess.Popen(['calc.exe'])
    elif 'camera' in software_name:
        speak('Opening Camera...')
        os.system("start microsoft.windows.camera:")
    elif 'youtube' in software_name or 'play' in software_name:
        song = software_name.replace('play', '').replace('youtube', '').strip()
        if song:
            speak(f'Playing {song} on YouTube')
            pywhatkit.playonyt(song)
        else:
            speak("Playing National Anthem on YouTube")
            pywhatkit.playonyt("National Anthem")
    else:
        speak(f"Sorry, I couldn't find software named {software_name}")

lyrics = {
    "shape of you": """The club isn't the best place to find a lover\nSo the bar is where I go""",
    "believer": """First things first\nI'ma say all the words inside my head""",
    "thunder": """Just a young gun with a quick fuse\nI was uptight, wanna let loose"""
}


def sing_song(song_name):
    if song_name in lyrics:
        speak(f"Here are two lines from {song_name}:")
        speak(lyrics[song_name])
    else:
        speak("Sorry, I don't have the lyrics for that song.")

def change_volume(command):
    devices = {
        "volume up": 0xA0000,
        "volume down": 0x90000,
        "mute": 0x80000
    }
    key = next((k for k in devices if k in command), None)
    if key:
        for _ in range(5):  
            ctypes.windll.user32.keybd_event(0xAF if key == "volume up" else 0xAE, 0, 0, 0)
        speak(f"{key.capitalize()} executed")
    else:
        speak("Volume command not recognized.")


def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)


def get_weather():
    try:
        city = "Chennai"
        url = f"http://wttr.in/{city}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            speak(f"The weather in {city} is: {response.text}")
        else:
            speak("Unable to fetch weather data right now.")
    except Exception as e:
        speak("Error fetching weather information.")

def set_reminder():
    speak("What should I remind you about?")
    reminder = input("Reminder: ")
    speak("After how many seconds should I remind you?")
    seconds = int(input("Seconds: "))
    speak(f"Okay, I will remind you in {seconds} seconds.")
    time.sleep(seconds)
    speak(f"Reminder: {reminder}")

def send_whatsapp():
    speak("Tell me the phone number with country code.")
    number = input("Number (with +91): ")
    speak("What should I say?")
    message = input("Message: ")
    speak("Sending message...")
    pywhatkit.sendwhatmsg_instantly(number, message)
    speak("Message sent.")


def system_control(command):
    if "shutdown" in command:
        speak("Shutting down...")
        os.system("shutdown /s /t 1")
    elif "restart" in command:
        speak("Restarting system...")
        os.system("shutdown /r /t 1")
    elif "lock" in command:
        speak("Locking system...")
        ctypes.windll.user32.LockWorkStation()


def process_command(command):
    if 'stop' in command or 'exit' in command:
        speak("Goodbye Sir. Have a nice day!")
        sys.exit()
    elif 'open' in command:
        software = command.replace('open', '').strip()
        open_software(software)
    elif 'play' in command:  # ➕ Add this block
        open_software(command)
    elif 'time' in command:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {time_now}")
    elif 'your name' in command:
        speak("My name is Jarvis, your personal assistant")
    elif 'who is god' in command:
        speak("Ajitheyyy Kadavuleyy")
    elif 'search' in command:
        query = command.replace('search', '').strip()
        speak(f"Searching for {query}")
        pywhatkit.search(query)
    elif 'sing' in command:
        song = command.replace('sing', '').strip()
        sing_song(song)
    elif 'volume' in command:
        change_volume(command)
    elif 'joke' in command:
        tell_joke()
    elif 'weather' in command:
        get_weather()
    elif 'remind' in command or 'reminder' in command:
        set_reminder()
    elif 'whatsapp' in command:
        send_whatsapp()
    elif 'shutdown' in command or 'restart' in command or 'lock' in command:
        system_control(command)
    elif 'chat' in command:
        prompt = command.replace('chat', '').strip()
        if prompt:
            smart_reply(prompt)
        else:
            speak("Please tell me what you want to chat about.")
    else:
        speak("I'm not sure how to handle that. Please try again.")




def main_input():
    while True:
        choice = input("Do you want to type a command or use voice input? (type/voice): ").lower()
        if choice == 'type':
            process_type_commands()
        elif choice == 'voice':
            process_voice_commands()

def process_type_commands():
    while True:
        command = input("Type your command: ").lower()
        process_command(command)

def process_voice_commands():
    listen_for_wake_word()  # Only once at the beginning
    while True:
        get_command()  # Continuously listen for commands


def listen_for_wake_word():
    with sr.Microphone() as source:
        print("Listening for wake word 'Jarvis'... Speak it to start.")
        recognizer.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                if 'jarvis' in command:
                    speak("Yes sir?")
                    greet_user()
                    break
            except:
                continue
        get_command()

def get_command():
    with sr.Microphone() as source:
        print("Listening for your command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        command = command.replace("jarvis", "").replace("please", "").strip()
        process_command(command)
        return
    except:
        speak("Sorry, I didn’t catch that.")


if __name__ == "__main__":
    main_input()
