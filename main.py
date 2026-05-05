import speech_recognition as sr
import os

def say(text):
    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; '  # Load speech lib
        f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '  # Create voice engine
        f'$speak.Volume = 75; '   # Set volume (0-100)
        f'$speak.Speak(\'{text}\')"'
    )

if __name__ == '__main__':
    print('PyCharm')  # Console test
    say('I am Jarvis AI made by Sam')  # Speak text