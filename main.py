import speech_recognition as sr   # Converts microphone voice into text | pip install SpeechRecognition
import os                         # Used for file handling, opening apps, folders, songs, etc.
import re                         # Used for pattern matching and cleaning text commands
import webbrowser                 # Opens websites directly in the default browser
import datetime                   # Gives current date, time, day, month, year, etc.
import google.generativeai as genai   # Gemini AI integration for AI chat features | pip install google-generativeai
import config                     # Stores secret data like API keys separately
import random                     # Used for random replies, songs, jokes, choices, etc.
import threading                  # Runs multiple tasks at the same time (multitasking)
import time                       # Used for adding delay between tasks
import win32com.client            # Windows built-in text to speech | pip install pywin32


# Windows built-in speaker — much more reliable than pyttsx3 on Windows
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# flag to cancel speaking mid-sentence
is_speaking = False

# flag to stop current AI speech instantly
stop_requested = False

# store chat history
chatStr = ""

# AI mode toggle
# Primary Mode  -> AI Enabled  (Gemini AI conversation mode)
# Secondary Mode -> AI Disabled (Normal command execution mode)
ai_enabled = False


# configure Gemini API using your key
genai.configure(api_key=config.API_KEY)

# create Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


# clean AI response so voice sounds natural
def clean_for_speech(text):
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)  # remove bold and italic
    text = re.sub(r'#{1,6}\s*', '', text)  # remove headings
    text = re.sub(r'`{1,3}.*?`{1,3}', '', text)  # remove code blocks
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # remove links
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # remove bullets
    text = re.sub(r'\n+', ' ', text)  # remove new lines
    text = re.sub(r'\s{2,}', ' ', text)  # remove extra spaces

    return text.strip()


# speak and WAIT until fully done before doing next action
# always use this before opening apps, songs, games, websites
def sayAndWait(text):
    global is_speaking
    global stop_requested

    text = clean_for_speech(text)

    # do not speak if stop was requested
    if stop_requested:
        return

    print("Jarvis:", text)

    is_speaking = True

    # split long text into smaller chunks
    sentences = re.split(r'(?<=[.!?]) +', text)

    for sentence in sentences:

        # instantly stop if user says stop
        if stop_requested:
            speaker.Speak("", 3)
            break

        speaker.Speak(sentence, 0)

    is_speaking = False
    stop_requested = False


# speak without waiting — used only for long AI replies
def say(text):
    threading.Thread(target=sayAndWait, args=(text,), daemon=True).start()


# stop speaking immediately — works even during AI long replies
def stopSpeaking():
    global is_speaking
    global stop_requested

    try:
        stop_requested = True
        is_speaking = False

        # SVSFPurgeBeforeSpeak flag (3) = clear queue and stop current speech instantly
        speaker.Speak("", 3)

        print("Jarvis stopped speaking")

    except Exception as e:
        print("Stop error:", e)


# clear chat memory
def clearChat():
    global chatStr

    chatStr = ""
    sayAndWait("Chat cleared")


# AI chat function using Gemini
def aiChat(query):
    global chatStr
    global stop_requested

    # reset stop flag before new AI reply
    stop_requested = False

    chatStr += f"Sam: {query}\nJarvis: "

    response = model.generate_content(chatStr)

    reply = response.text

    chatStr += f"{reply}\n"

    print(reply)

    # speak AI reply
    say(reply)

    # create Gemini folder if not present
    if not os.path.exists("Gemini"):
        os.mkdir("Gemini")

    # remove unwanted text from filename
    filename = query.replace("using artificial intelligence", "").strip()

    # remove invalid filename characters
    filename = re.sub(r'[\\/:*?"<>|]', '', filename).strip()

    # create random filename if query is empty
    if not filename:
        filename = f"chat-{random.randint(1, 9999999)}"

    # save AI response into text file
    with open(f"Gemini/{filename}.txt", "w", encoding="utf-8") as f:
        f.write(reply)


# control AI mode
def useAI(query):
    global ai_enabled

    # stop Jarvis voice immediately — checked FIRST so it always works
    if "stop" in query:
        stopSpeaking()
        return True

    # enable AI mode
    if "enable ai" in query:
        ai_enabled = True
        sayAndWait("AI enabled")
        return True

    # disable AI mode
    if "disable ai" in query:
        ai_enabled = False
        sayAndWait("AI disabled")
        return True

    # clear stored AI conversation memory
    if "clear chat" in query:
        clearChat()
        return True

    # if AI mode is enabled then use Gemini AI
    if ai_enabled:
        aiChat(query)
        return True

    return False


# find correct microphone (Auto selecting the microphone)
def get_mic_index():
    mic_list = sr.Microphone.list_microphone_names()

    for i, name in enumerate(mic_list):

        # check different Realtek microphone names
        if "Realtek HD Audio Mic Array" in name:
            return i

        if "Microphone Array (Realtek" in name:
            return i

        if "Realtek(R) Audio" in name:
            return i

    return None


# take voice command
def takeCommand():
    r = sr.Recognizer()

    # energy threshold — lower = picks up quieter voices
    # increase this number (e.g. 400) if background noise triggers false detection
    # decrease this number (e.g. 200) if Jarvis is not hearing you clearly
    r.energy_threshold = 300

    # disable auto energy adjustment so manual threshold above is always used
    r.dynamic_energy_threshold = False

    mic_index = get_mic_index()

    # return empty string if no microphone found
    if mic_index is None:
        print("No microphone found")
        return ""

    try:
        with sr.Microphone(device_index=mic_index) as source:

            # noise calibration duration in seconds
            # increase (e.g. 1.5) if room is noisy, decrease (e.g. 0.5) for quieter rooms
            r.adjust_for_ambient_noise(source, duration=1)

            print("Listening...")

            # ── LISTENING TIME SETTINGS ──────────────────────────────────────────#
            # timeout          → seconds Jarvis waits for you to START speaking    #
            #                    increase if you need more time before you begin   #
            # phrase_time_limit → seconds Jarvis listens after you START speaking  #
            #                    increase if your commands are long                #
            #                    decrease if you want faster response              #
            audio = r.listen(source, timeout=4, phrase_time_limit=5)               #
            # ─────────────────────────────────────────────────────────────────────#

            print("Recognizing...")

            # convert voice into text
            query = r.recognize_google(audio, language='en-in')

            print("User said:", query)

            return query.lower()

    except sr.WaitTimeoutError:
        print("Listening timeout")
        return ""

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""

    except Exception as e:
        print("Mic error:", e)
        return ""


# start program
if __name__ == '__main__':

    print("Jarvis started")

    sayAndWait("I am Jarvis AI")


    # websites list (you can add more sites)
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["google", "https://www.google.com"],
        ["github", "https://github.com/Sam-Dev-161127"],
        ["chatgpt", "https://chat.openai.com"],
        ["claude", "https://claude.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["gmail", "https://mail.google.com"],
        ["instagram", "https://www.instagram.com"],
        ["whatsapp", "https://web.whatsapp.com/"],
        ["telegram", "https://web.telegram.org/a/"],
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


    # Songs List
    # Note: Your song file path/address will be different from my PC path.
    # Change the path according to where your songs are stored on your computer.

    songs = [
        ["majboor", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Majboor.mp3"],
        ["cornfield", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Cornfield Chase.mp3"],
        ["downfall", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Song\Downfall.mp3"]
    ]


    # Games List
    # Note: Your game shortcut path/address will be different from my PC path.
    # Change the path according to where your games or shortcuts are stored.

    games = [
        ["valorant", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\VALORANT.lnk"],
        ["epic games", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Epic Games Launcher.lnk"],
        ["genshin impact", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Genshin Impact.lnk"],
        ["steam", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\Game\Steam.lnk"]
    ]


    # Apps List
    # Note: Your application shortcut path/address will be different from my PC path.
    # Change the path according to where your apps or shortcuts are stored.

    Apps = [
        ["word", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Word.lnk"],
        ["powerpoint", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\powerpoint.lnk"],
        ["excel", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\excel.lnk"],
        ["opera", r"C:\Users\Sam-Dev-161127\PycharmProjects\Jarvis AI\App\Opera GX Browser .lnk"]
    ]


    # infinite loop for continuous listening
    while True:

        query = takeCommand()

        if query == "":
            continue

        command_matched = False


        # handle AI commands first
        if useAI(query):
            continue


        # open websites — sayAndWait so Jarvis finishes speaking before browser opens
        for site in sites:
            if f"open {site[0]}" in query:
                sayAndWait("Opening " + site[0])
                webbrowser.open(site[1])
                command_matched = True


        # play songs — sayAndWait so voice fully finishes before song starts playing
        for song in songs:

            if f"play {song[0]}" in query:

                # speak song name and wait until fully done
                sayAndWait("Playing " + song[0])

                # open song file after speech is done
                os.startfile(song[1])

                command_matched = True


        # open games — sayAndWait so Jarvis finishes speaking before game launches
        for game in games:
            if f"open {game[0]}" in query:
                sayAndWait("Opening " + game[0])
                os.startfile(game[1])
                command_matched = True


        # open apps — sayAndWait so Jarvis finishes speaking before app launches
        for app in Apps:
            if f"open {app[0]}" in query:
                sayAndWait("Opening " + app[0])
                os.startfile(app[1])
                command_matched = True


        # tell current time
        if "what time is it" in query:

            now = datetime.datetime.now()

            hour = now.strftime("%I")
            minute = now.strftime("%M")
            am_pm = now.strftime("%p")

            sayAndWait(f"The time is {hour}:{minute} {am_pm}")

            command_matched = True


        # tell current date
        if "what date is it" in query:

            now = datetime.datetime.now()

            day_name = now.strftime("%A")
            day = now.strftime("%d")
            month = now.strftime("%B")
            year = now.strftime("%Y")

            sayAndWait(f"Today is {day_name}, {day} {month} {year}")

            command_matched = True

        # fallback AI if AI mode is enabled
        if not command_matched and ai_enabled:
            aiChat(query)

# Follow Me