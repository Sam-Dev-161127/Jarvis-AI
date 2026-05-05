import speech_recognition as sr
import os

def say(text):
    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; ' # For Window
        f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        f'$speak.Volume = 75; '   # 🔉 0 to 100 
        f'$speak.Speak(\'{text}\')"'
    )

if __name__ == '__main__':
    print('PyCharm')
    say('I am Jarvis AI made by Sam')