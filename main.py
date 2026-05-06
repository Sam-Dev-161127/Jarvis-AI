import speech_recognition as sr
import os

def say(text):
    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        f'$speak.Volume = 75; '
        f'$speak.Speak(\'{text}\')"'
    )

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except Exception as e:   # ✅ FIXED INDENTATION
            return "Some Error Occured,Sorry from Jarvis"

if __name__ == '__main__':
    print('PyCharm')
    say('I am Jarvis AI made by Sam')
    while True:
        print("Listening...")
        text = takeCommand()
        say(text)