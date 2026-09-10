💜 KSR AI Assistant

Your Personal AI Voice Agent — Like JARVIS, but real.

KSR is a fully autonomous AI voice assistant built with Python. It listens, thinks, and acts — writing code, controlling your PC, reading your screen, browsing the web, and talking to you like a best friend.

🎥 Demo

Say "wake up KSR" → KSR wakes up Say "sleep" → KSR goes to background

✨ Features
Feature	Description
🎤 Voice Control	Wake word detection — say "wake up KSR"
🧠 AI Brain	Powered by Groq LLaMA — answers anything
💻 VS Code Agent	Opens VS Code, creates files, writes & runs code
🎮 Game Generator	Generates playable Python games by voice
🏗️ Project Builder	Builds entire project folders with all files
👁️ Screen Reader	Reads text from your screen using OCR
🌐 Web Agent	Controls Chrome — clicks, fills forms, searches
📅 Task Scheduler	Schedules daily routines by voice
🧠 Persistent Memory	Remembers your projects, habits, contacts
🔋 System Monitor	Battery alerts, CPU/RAM monitoring
🌤️ Weather	Real-time weather for any city
📰 News	Reads top headlines
🌐 Translate	Translates to 15+ languages
📝 Notes	Save and read notes by voice
⏰ Timer	Set timers and reminders by voice
🔊 Volume Control	Control volume by voice
💬 WhatsApp	Send WhatsApp messages by voice
🚀 Getting Started
Prerequisites
Python 3.11+
Windows 10/11
Google Chrome
VS Code (optional)
Tesseract OCR
Installation

1. Clone the repo:

bash
git clone https://github.com/karan-xsingh/KSR-AI-Assistant.git
cd KSR-AI-Assistant

2. Install dependencies:

bash
pip install speechrecognition pyttsx3 pyautogui pyperclip pywhatkit
pip install psutil requests deep-translator sounddevice numpy
pip install pystray pillow mss pytesseract selenium webdriver-manager
pip install apscheduler python-dotenv opencv-python pdfplumber

3. Install Tesseract OCR: Download from: https://github.com/UB-Mannheim/tesseract/wiki Install to default path: C:\Program Files\Tesseract-OCR\

4. Get FREE Groq API Key:

Go to https://console.groq.com
Create account → API Keys → Create key

5. Create .env file:

GROQ_API_KEY=your_groq_api_key_here

6. Run KSR:

bash
python KSR.py
🗣️ Voice Commands
General
Say	Action
wake up KSR	Wake KSR up
sleep	Put KSR to sleep
what time is it	Current time
weather in Mumbai	Weather for any city
today's news	Top headlines
Coding
Say	Action
open VS Code and make a file called main.py	Creates file in VS Code
write code for a calculator	Generates + opens code in VS Code
solve this coding question	Reads screen → solves → writes solution
run the file	Runs current Python file
build a flask API for todo list	Builds entire project
Web
Say	Action
open YouTube	Opens YouTube
search machine learning on YouTube	Searches YouTube
open LinkedIn	Opens LinkedIn
scroll down	Scrolls page
click on Submit	Clicks button
Productivity
Say	Action
set timer for 25 minutes	Pomodoro timer
take note buy groceries	Saves note
read my notes	Reads saved notes
every morning at 9 open VS Code	Schedules daily task
my projects	Lists saved projects
what's my next class	Next class from timetable
System
Say	Action
battery	Battery percentage
system status	CPU, RAM, disk info
volume up / volume down	Volume control
lock	Lock screen
take screenshot	Opens snipping tool
📁 Project Structure
KSR-AI-Assistant/
│
├── KSR.py              # Main agent — core brain
├── vision.py           # Screen reading + OCR
├── web_agent.py        # Selenium web automation
├── scheduler.py        # Task scheduling
├── memory.py           # Persistent memory
├── project_builder.py  # Auto project builder
├── face_auth.py        # Face unlock
├── gmail_agent.py      # Gmail control
├── pdf_agent.py        # PDF study agent
├── background_monitor.py # System monitoring
│
├── .env                # API keys (not uploaded)
├── .gitignore
└── README.md
🏗️ Architecture
Voice Input → Wake Word Detection
                    ↓
              Task Planner (Groq AI)
                    ↓
         ┌──────────┴──────────┐
         ↓                     ↓
    Action Engine         AI Response
    (execute steps)       (chat/answer)
         ↓
  ┌──────┴───────┐
  ↓              ↓
VS Code       Browser
Agent         Agent
🔧 Configuration

Edit these in KSR.py:

python
ASSISTANT_NAME = "KSR"
USER_NAME      = "Karan"      # Your name
YOUR_CITY      = "Dehradun"   # Your city
CHROME_PROFILE = "Default"    # Chrome profile
GROQ_MODEL     = "openai/gpt-oss-20b"  # AI model
🛡️ Security
API keys stored in .env file only
.env is gitignored — never pushed to GitHub
Each user must add their own Groq API key
🎓 About

Built by Karan Singh Rathore B.Tech CSE (AI/ML) — DBS Global University, Dehradun (2024-2028)

This project is part of my AI/ML research work exploring autonomous voice agents with multimodal capabilities.

Connect:

GitHub: @karan-xsingh
📄 License

MIT License — free to use, modify and distribute.

⭐ If you found this useful, please give it a star!
