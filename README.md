# Jarvis-AI 🤖

Jarvis-AI is a smart desktop voice assistant built using Python 🐍.  
It can listen to voice commands, understand user instructions, and perform different tasks on the computer like opening websites 🌐, launching apps 📂, playing songs 🎵, launching games 🎮, and having AI conversations using the Gemini API 🤖.

The assistant is designed to behave like a real desktop AI assistant with voice interaction, multitasking support, AI chat mode, speech interruption control, and automation features.

This project is modular and beginner-friendly, so you can easily add more features in the future like weather updates, news, GUI interface, automation tools, smart home integration, and more.

---

# ✨ Features

- 🎤 Voice command recognition  
- 🗣️ Windows built-in text-to-speech voice  
- 🤖 Gemini AI integration for smart conversations  
- 🔄 AI enable/disable mode system  
- 🌐 Open websites using voice commands  
- 🎵 Play local songs using voice  
- 🎮 Launch games from shortcuts  
- 📂 Open applications using voice  
- 📅 Tell current date and time  
- 🧠 Chat memory system  
- 💾 Save AI chat responses automatically  
- ⏹️ Stop Jarvis speech instantly using voice  
- 🧵 Multithreading for smoother performance  
- 🎙️ Automatic microphone detection  
- 🧩 Easy to customize and expand  

---

# 🛠️ Technologies Used

- Python  
- SpeechRecognition  
- Google Gemini API  
- PyWin32  
- Threading  
- OS Module  
- Webbrowser Module  
- Datetime Module  
- Regular Expressions (re)  

---

# ⚙️ System Requirements

## 💻 Operating System

This project is mainly designed for:

- ✅ Windows 10  
- ✅ Windows 11  

Because it uses:
- `win32com.client`
- Windows SAPI Voice System

Linux and macOS are not officially supported in the current version.

---

# 🐍 Python Version

## Recommended Python Version

```bash
Python 3.10
```

## Also Tested Working On

- Python 3.11
- Python 3.12

---

# ⚠️ Important Notes

## 🔹 Why Python 3.10 is Recommended

Some speech-related libraries work more reliably on Python 3.10.

Newer Python versions may sometimes cause:
- Microphone detection issues
- PyAudio installation errors
- SpeechRecognition dependency problems

So Python 3.10 is the safest choice for beginners.

---

# 📥 Installation Guide

## 1️⃣ Install Python

Download Python:

- Python Official Website:  
https://www.python.org/downloads/

### ⚠️ IMPORTANT
While installing Python:

✅ Tick this option:

```bash
Add Python to PATH
```

Otherwise Python commands will not work in terminal.

---

## 2️⃣ Clone the Repository

```bash
git clone https://github.com/Sam-Dev-161127/Jarvis-AI.git
cd Jarvis-AI
```

Or download ZIP manually from GitHub.

---

# 📦 Install Required Libraries

## Install Main Libraries

```bash
pip install SpeechRecognition
pip install google-generativeai
pip install pywin32
pip install pyaudio
```

---

# ⚠️ PyAudio Installation Problem Fix

Sometimes `pyaudio` fails to install normally.

If you get errors:

## Solution 1 (Recommended)

Install using wheel file:

1. Open:
https://www.lfd.uci.edu/~gohlke/pythonlibs/

2. Download PyAudio wheel matching your:
- Python version
- Windows version

Example:

```bash
PyAudio-0.2.11-cp310-cp310-win_amd64.whl
```

3. Install it:

```bash
pip install filename.whl
```

---

# 🔑 Gemini API Setup

## 1️⃣ Get Gemini API Key

Open:

https://aistudio.google.com/

Create API key.

---

## 2️⃣ Create `config.py`

Inside project folder create:

```python
API_KEY = "YOUR_GEMINI_API_KEY"
```

---

# 📂 Project Structure

```bash
Jarvis-AI/
│
├── Gemini/          # Stores AI chat responses
├── Song/            # Local songs folder
├── Game/            # Game shortcuts
├── App/             # App shortcuts
│
├── config.py        # Gemini API key
├── main.py          # Main Jarvis program
└── README.md
```

---

# ▶️ Running Jarvis

Open terminal inside project folder:

```bash
python main.py
```

If everything works correctly:

```bash
Jarvis started
```

Jarvis will say:

```bash
I am Jarvis AI
```

---

# 🎤 Example Voice Commands

## 🌐 Website Commands

- "Open YouTube"
- "Open Google"
- "Open GitHub"
- "Open ChatGPT"

---

## 🎵 Music Commands

- "Play Majboor"
- "Play Cornfield"
- "Play Downfall"

---

## 🎮 Game Commands

- "Open Valorant"
- "Open Steam"
- "Open Epic Games"

---

## 📂 Application Commands

- "Open Word"
- "Open PowerPoint"
- "Open Excel"

---

## 📅 Utility Commands

- "What time is it"
- "What date is it"

---

# 🤖 AI Commands

| Command | Action |
|---|---|
| Enable AI | Turns ON Gemini AI mode |
| Disable AI | Turns OFF AI mode |
| Clear Chat | Clears AI memory |
| Stop | Stops Jarvis speaking instantly |

---

# 🧠 How AI Mode Works

Jarvis supports two modes:

## 🤖 Primary Mode
Gemini AI conversation enabled.

Jarvis behaves like an AI chatbot.

---

## ⚙️ Secondary Mode
Normal command execution mode.

Jarvis only performs programmed commands.

---

# 💾 AI Chat Saving Feature

Every AI response is automatically saved inside:

```bash
Gemini/
```

as a `.txt` file.

This helps keep conversation history safely stored.

---

# 🛑 Stop Speaking Feature

Jarvis supports instant speech interruption.

Simply say:

```bash
Stop
```

Jarvis immediately stops speaking even during long AI responses.

---

# 🎙️ Microphone Detection

Jarvis automatically detects:

- Realtek microphones
- Realtek microphone arrays

You can modify microphone names inside:

```python
get_mic_index()
```

if your microphone name is different.

---

# ⚡ Performance Notes

## Recommended For Smooth Performance

- At least 4GB RAM
- Internet connection for Gemini AI
- Good microphone quality
- Quiet room for better speech recognition

---

# 🚀 Future Improvements

- 🌦️ Weather updates  
- 📰 News API support  
- 🖥️ GUI desktop interface  
- 🎯 Better voice accuracy  
- 🧠 Personal memory system  
- 🏠 Smart home integration  
- 📱 Mobile control support  
- ⚡ Advanced automation system  
- 🎧 Wake word support ("Hey Jarvis")  
- 🔊 Custom AI voices  

---

# 👨‍💻 Author

## Sameer Patra

🎓 Student  
🤖 Tech Enthusiast  
🐍 Python Learner  

### 🌍 From
Odisha, India 🇮🇳

### 🚀 Interests
- Artificial Intelligence
- Robotics
- Automation
- Python Development

GitHub:  
https://github.com/Sam-Dev-161127

---

# 📌 Final Note

This project is still under development 🚧.

New features, improvements, optimizations, and smarter AI capabilities will continue to be added over time.

Feel free to fork the project, customize it, and build your own advanced version of Jarvis AI 🤖✨