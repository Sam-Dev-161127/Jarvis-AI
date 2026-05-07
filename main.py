import speech_recognition as sr
import os
import webbrowser

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
        # r.pause_threshold = 0.6
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query

        except Exception as e:
            return "Some Error Occured, Sorry from Jarvis"

if __name__ == '__main__':
    print('PyCharm')
    say('I am Jarvis AI')

    sites = [
        ["youtube", "https://www.youtube.com"],
        ["google", "https://www.google.com"],
        ["github", "https://www.github.com"],
        ["chatgpt", "https://chat.openai.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["gmail", "https://mail.google.com"],
        ["instagram", "https://www.instagram.com"],
        ["x", "https://www.x.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["amazon", "https://www.amazon.in"],
        ["flipkart", "https://www.flipkart.com"],
        ["netflix", "https://www.netflix.com"],
        ["spotify", "https://www.spotify.com"],
        ["jiohotstar", "https://www.jiohotstar.com"],
        ["code with harry", "https://www.codewithharry.com"],
        ["geeksforgeeks", "https://www.geeksforgeeks.org"],
        ["w3schools", "https://www.w3schools.com"],
        ["leetcode", "https://leetcode.com"],
        ["hackerrank", "https://www.hackerrank.com"],
        ["stackoverflow", "https://stackoverflow.com"],
        ["canva", "https://www.canva.com"],
        ["replit", "https://replit.com"],
        ["coursera", "https://www.coursera.org"],
    ]

    while True:
        print("Listening...")
        query = takeCommand()

        for site in sites:
            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])