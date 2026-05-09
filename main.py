import speech_recognition as sr
import os
import webbrowser
import datetime
import google.generativeai as genai
import config
import random

def chat(query):
    pass

# Configure Gemini AI API
# API key is stored safely inside config.py
genai.configure(api_key=config.API_KEY)

# Create Gemini AI model
model = genai.GenerativeModel("gemini-2.5-flash")

# Global variable to store chat history
chatStr = ""

# Function to make Jarvis speak
def say(text):
    os.system(
        f'powershell -Command "Add-Type -AssemblyName System.Speech; '
        f'$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
        f'$speak.Volume = 75; '
        f'$speak.Speak(\'{text}\')"'
    )


# Function to talk with Gemini AI
def aiChat(query):
    global chatStr

    # Add user query into chat history
    chatStr += f"Sam: {query}\nJarvis: "

    # Generate Gemini response
    response = model.generate_content(chatStr)

    # Store AI reply
    reply = response.text

    # Add reply into chat history
    chatStr += f"{reply}\n"

    # Print AI response in terminal
    print(reply)

    # Speak AI response
    say(reply)

    # Save Gemini response into txt file

    # Create folder if not exists
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    # Create clean filename
    filename = query.replace("using artificial intelligence", "").strip()

    # Save response
    with open(f"Gemini/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(reply)


# Function to use Gemini AI only when requested
def useAI(query):

    # Check if user said "using artificial intelligence"
    if "using artificial intelligence" in query:

        # Remove trigger words from query
        clean_query = query.replace("using artificial intelligence", "")

        # Remove extra spaces
        clean_query = clean_query.strip()

        # Talk with Gemini AI
        aiChat(clean_query)

        return True

    return False


# Function to auto-pick correct microphone
def get_mic_index():
    mic_list = sr.Microphone.list_microphone_names()

    for i, name in enumerate(mic_list):
        if "Realtek HD Audio Mic Array" in name:
            return i
        if "Microphone Array (Realtek" in name:
            return i
        if "Realtek(R) Audio" in name:
            return i

    return None


# Function to take voice command from user
def takeCommand():

    r = sr.Recognizer()

    mic_index = get_mic_index()

    if mic_index is None:
        print("No Real microphone found!")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:

            r.adjust_for_ambient_noise(source, duration=0.5)

            print("Listening...")

            audio = r.listen(source, timeout=6, phrase_time_limit=6)

            print("Recognizing...")

            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query

    except sr.WaitTimeoutError:
        print("No speech detected (timeout)")
        return ""

    except Exception as e:
        print("Mic Error:", e)
        return ""


if __name__ == '__main__':

    print('PyCharm')
    say('I am Jarvis AI')

    # List of websites
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["google", "https://www.google.com"],
        ["github", "https://github.com/Sam-Dev-161127"],
        ["chatgpt", "https://chat.openai.com"],
        ["claude", "https://claude.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["gmail", "https://mail.google.com"],
        ["instagram", "https://www.instagram.com"],
        ["whatapps", "https://whatapps.com"],
        ["telegram", "https://telegram.com"],
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
        ["majboor", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Majboor.mp3"],
        ["cornfield", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Cornfield Chase.mp3"],
        ["downfall", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Downfall.mp3"]
    ]

    # List of games
    games = [
        ["valorant", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\VALORANT.lnk"],
        ["epic games", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Epic Games Launcher.lnk"],
        ["genshin impact", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Genshin Impact.lnk"],
        ["steam", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Steam.lnk"]
    ]

    # List of Apps
    Apps = [
        ["word", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Word.lnk"],
        ["powerpoint", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\powerpoint.lnk"],
        ["excel", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\excel.lnk"],
        ["opera", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\opera.lnk"]
    ]

    while True:

        query = takeCommand()

        query = query.lower()

        if query == "":
            continue

        if useAI(query):
            continue

        # Open websites
        for site in sites:
            if f"open {site[0]}" in query:
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])

        # Play songs
        for song in songs:
            if f"play {song[0]}" in query:
                say(f"Playing {song[0]}...")
                os.startfile(song[1])

        # Open games
        for game in games:
            if f"open {game[0]}" in query:
                say(f"Opening {game[0]}...")
                os.startfile(game[1])

        # Open App apps
        for App in Apps:
            if f"open {App[0]}" in query:
                say(f"Opening {App[0]}...")
                os.startfile(App[1])

        # Tell day, date, month, year and time
        if "the time" in query or "date" in query:

            now = datetime.datetime.now()

            day_name = now.strftime("%A")
            day = now.strftime("%d")
            month = now.strftime("%B")
            year = now.strftime("%Y")

            hour = now.strftime("%I")
            minute = now.strftime("%M")
            am_pm = now.strftime("%p")

            say(f"Today is {day_name}")
            say(f"The date is {day} {month} {year}")
            say(f"The time is {hour} bajke {minute} minute {am_pm}")