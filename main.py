import speech_recognition as sr  # do not remove the comment import speech_recognition as sr
import os
import re
import webbrowser
import datetime
import google.generativeai as genai
import config
import random
import openai
import pyttsx3  # pip install pyttsx3
import threading


# Global stop speaking flag
stop_speaking = False

# Global engine
engine = None


def chat(query):
    global chatStr

    print(chatStr)

    openai.api_key = config.API_KEY

    chatStr += f"Harry: {query}\n Jarvis: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # todo: Wrap this inside of a try catch block
    # print(response["choices"][0]["text"])

    chatStr += f"{response['choices'][0]['text']}\n"

    # Logic for saving the chat to a file as seen in Screenshot 2026-05-09 085914.png
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # Using the split logic from your screenshot
    filename = "".join(query.split('intelligence')[1:]).strip()

    if filename == "":
        filename = f"chat-{random.randint(1, 2343434356)}"

    # Remove illegal Windows filename characters
    filename = re.sub(r'[\\/:*?"<>|]', '', filename).strip()

    with open(f"Openai/{filename}.txt", "w") as f:
        f.write(response["choices"][0]["text"])

    return response["choices"][0]["text"]


# Configure Gemini AI API
# API key is stored safely inside config.py
genai.configure(api_key=config.API_KEY)

# Create Gemini AI model
model = genai.GenerativeModel("gemini-2.5-flash")

# Global variable to store chat history
chatStr = ""

# AI mode status
ai_enabled = False


# Function to clean markdown symbols from Gemini response before speaking
# Gemini often returns **bold**, *bullets*, ### headings etc. which sound terrible when read aloud
def clean_for_speech(text):
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)   # remove ** bold ** and * italic *
    text = re.sub(r'#{1,6}\s*', '', text)              # remove ### headings
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text)       # remove `code` blocks
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # remove [link](url) → keep label
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # remove bullet dashes
    text = re.sub(r'\n+', ' ', text)                   # collapse newlines into spaces
    text = re.sub(r'\s{2,}', ' ', text)                # collapse extra spaces

    return text.strip()


# Function to make Jarvis speak
def speak_thread(text):
    global engine
    global stop_speaking

    # Clean markdown before speaking so symbols like ** * # are not read aloud
    clean_text = clean_for_speech(text)

    try:
        engine = pyttsx3.init()

        engine.setProperty('volume', 1.0)   # 0.0 to 1.0
        engine.setProperty('rate', 170)     # words per minute

        engine.say(clean_text)

        engine.runAndWait()

        engine.stop()

    except Exception as e:
        print(f"Voice error: {e}")


def say(text):
    global stop_speaking

    stop_speaking = False

    print(f"Jarvis: {text}")

    threading.Thread(target=speak_thread, args=(text,)).start()


# Function to stop Jarvis speaking
def stopSpeaking():
    global engine

    try:
        if engine:
            engine.stop()

            print("Jarvis stopped speaking.")

    except Exception as e:
        print(f"Stop error: {e}")


# Function to clear memory/chat
def clearChat():
    global chatStr

    chatStr = ""

    say("Chat memory cleared")


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

    # Create clean filename — remove trigger words and illegal Windows filename characters
    filename = query.replace("using artificial intelligence", "").strip()

    filename = re.sub(r'[\\/:*?"<>|]', '', filename).strip()

    if not filename:
        filename = f"chat-{random.randint(1, 9999999)}"

    # Save response
    with open(f"Gemini/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(reply)


# Function to use Gemini AI only when requested
def useAI(query):
    global ai_enabled

    # Enable AI mode
    if "enable artificial intelligence" in query:
        ai_enabled = True

        say("Artificial intelligence enabled")

        return True

    # Disable AI mode
    if "disable artificial intelligence" in query:
        ai_enabled = False

        say("Artificial intelligence disabled")

        return True

    # Stop Jarvis speaking
    if "stop" in query:
        stopSpeaking()

        return True

    # Clear memory/chat
    if "clear chat" in query:
        clearChat()

        return True

    # If AI mode is enabled → use Gemini
    if ai_enabled:
        aiChat(query)

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
    #You can add your own website as your choice
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
    # Your path address will be different from my path address
    songs = [
        ["majboor", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Majboor.mp3"],
        ["cornfield", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Cornfield Chase.mp3"],
        ["downfall", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Downfall.mp3"]
    ]

    # List of games
    # Your game shortcut path will be different from my PC path
    games = [
        ["valorant", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\VALORANT.lnk"],
        ["epic games", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Epic Games Launcher.lnk"],
        ["genshin impact", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Genshin Impact.lnk"],
        ["steam", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Steam.lnk"]
    ]

    # List of Apps
    # Your app shortcut path will be different from my PC path
    Apps = [
        ["word", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Word.lnk"],
        ["powerpoint", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\powerpoint.lnk"],
        ["excel", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\excel.lnk"],
        ["opera", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Opera GX Browser .lnk"]
    ]

    while True:

        query = takeCommand()

        query = query.lower()

        if query == "":
            continue

        # Flag to track if any command was matched
        command_matched = False

        if useAI(query):
            continue

        # Open websites
        for site in sites:

            if f"open {site[0]}" in query:

                say(f"Opening {site[0]}...")

                webbrowser.open(site[1])

                command_matched = True

        # Play songs
        for song in songs:

            if f"play {song[0]}" in query:

                say(f"Playing {song[0]}...")

                os.startfile(song[1])

                command_matched = True

        # Open games
        for game in games:

            if f"open {game[0]}" in query:

                say(f"Opening {game[0]}...")

                os.startfile(game[1])

                command_matched = True

        # Open App apps
        for App in Apps:

            if f"open {App[0]}" in query:

                say(f"Opening {App[0]}...")

                os.startfile(App[1])

                command_matched = True

        # Tell day
        if "which day is it" in query:

            now = datetime.datetime.now()

            day_name = now.strftime("%A")

            say(f"Today is {day_name}")

            command_matched = True

        # Tell month
        if "which month is it" in query:

            now = datetime.datetime.now()

            month = now.strftime("%B")

            say(f"This month is {month}")

            command_matched = True

        # Tell year
        if "which year is it" in query:

            now = datetime.datetime.now()

            year = now.strftime("%Y")

            say(f"The year is {year}")

            command_matched = True

        # Tell date
        if "what date is it" in query or "tell me the date" in query:

            now = datetime.datetime.now()

            day = now.strftime("%d")

            month = now.strftime("%B")

            year = now.strftime("%Y")

            say(f"Today's date is {day} {month} {year}")

            command_matched = True

        # Tell time
        if "what time is it" in query or "the time" in query:

            now = datetime.datetime.now()

            hour = now.strftime("%I")

            minute = now.strftime("%M")

            am_pm = now.strftime("%p")

            say(f"The time is {hour} bajke {minute} minute {am_pm}")

            command_matched = True

        # Fallback — if no command matched, send the query to Gemini automatically
        # This handles casual questions like "how are you", "tell me a joke", etc.
        if not command_matched and ai_enabled:

            aiChat(query)