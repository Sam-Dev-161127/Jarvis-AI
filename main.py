import speech_recognition as sr
import os
import webbrowser


# Function to make Jarvis speak
def say(text):
    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        f'$speak.Volume = 75; '
        f'$speak.Speak(\'{text}\')"'
    )


# Function to take voice command from user
def takeCommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        # r.pause_threshold controls how long Jarvis waits after you stop speaking
        # Smaller value = faster response but may cut your voice
        # Bigger value = waits more before recognizing
        # You can uncomment and change the value if needed

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

    # List of websites
    sites = [

        # You can add your own websites here
        # These are the websites from my choice

        ["youtube", "https://www.youtube.com"],
        ["google", "https://www.google.com"],
        ["github", "https://github.com/Sam-Dev-161127"],
        ["chatgpt", "https://chat.openai.com"],
        ["claude", "https://claude.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["gmail", "https://mail.google.com"],
        ["instagram", "https://www.instagram.com"],
        ["whatapps", "https://whatapps.com"],
        ["telegram","https://telegram.com"],
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

    # List of songs
    songs = [

        # You can add your own songs here
        # Note: Your song path and my song path will be different

        ["majboor", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Majboor.mp3"],
        ["cornfield", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Cornfield Chase.mp3"],
        ["downfall", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Downfall.mp3"]
    ]

    # List of games
    games = [

        # You can add your own games here
        # Note: Your game path and my game path will be different

        ["valorant", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\VALORANT.lnk"],
        ["epic games", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Epic Games Launcher.lnk"],
        ["genshin impact", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Genshin Impact.lnk"],
        ["steam", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Steam.lnk"]
    ]

    while True:

        query = takeCommand()

        # Open websites
        for site in sites:

            if f"open {site[0]}" in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        # Play songs
        for song in songs:

            if f"play {song[0]}" in query.lower():
                say(f"Playing {song[0]}...")
                os.startfile(song[1])

        # Open games
        for game in games:

            if f"open {game[0]}" in query.lower():
                say(f"Opening {game[0]}...")
                os.startfile(game[1])

        # Repeat what user said
        # say(query)