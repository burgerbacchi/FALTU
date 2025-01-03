import os
import webbrowser
import datetime
import pyttsx3
import speech_recognition as sr
import subprocess
import platform

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speech rate
engine.setProperty('volume', 0.9)  # Volume

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
        except sr.WaitTimeoutError:
            speak("No command detected.")
        return ""

def open_website(url):
    """Open a website in the default browser."""
    webbrowser.open(url)
    speak(f"Opening {url}")

def tell_time():
    """Tell the current time."""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def open_application(app_name):
    """Open common applications."""
    system = platform.system()
    try:
        if "chrome" in app_name:
            subprocess.Popen("chrome" if system == "Windows" else "google-chrome")
        elif "notepad" in app_name:
            subprocess.Popen("notepad" if system == "Windows" else "gedit")
        elif "calculator" in app_name:
            subprocess.Popen("calc" if system == "Windows" else "gnome-calculator")
        else:
            speak("Sorry, I cannot open that application.")
    except Exception as e:
        speak(f"Failed to open {app_name}. Error: {str(e)}")

def search_google(query):
    """Perform a Google search."""
    url = f"https://www.google.com/search?q={query}"
    open_website(url)
    speak(f"Searching Google for {query}")

def process_command(command):
    """Process the given voice command."""
    if "time" in command:
        tell_time()
    elif "open" in command:
        if "website" in command or "google" in command:
            speak("What should I search for?")
            query = listen()
            if query:
                search_google(query)
        else:
            app_name = command.replace("open", "").strip()
            open_application(app_name)
    elif "exit" in command or "quit" in command or "stop" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I didn't understand that command.")
    return True

def main():
    """Main loop for the assistant."""
    speak("Hello, I am Jarvis. How can I assist you today?")
    while True:
        command = listen()
        if command:
            if not process_command(command):
                break

if __name__ == "__main__":
    main()
