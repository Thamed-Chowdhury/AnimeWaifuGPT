# 🎌 AnimeWaifuGPT — Gemini-Powered Anime Assistant

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green?logo=pygame)
![License](https://img.shields.io/badge/License-MIT-orange)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## 🧬 Overview

**AnimeWaifyGPT** is an interactive anime-style AI assistant powered by **Google Gemini 2.5-Flash**, **Pygame**, and **Edge-TTS**.
You can chat with **GPT-chan**, an anime-inspired character who responds to your messages with both **voice and lip-synced animation**.

Type any message in the text box, and GPT-chan will “think,” respond aloud, and animate her sprite while speaking.
The program maintains full conversation history and a **memory capability**, allowing GPT-chan to remember previous exchanges and respond contextually to ongoing conversations — making interactions feel more natural and continuous.

---

## 🎮 Features

* 💬 Real-time interactive chat with Gemini 2.5-Flash
* 🕣 Edge-TTS voice synthesis for GPT-chan’s spoken replies
* 🎨 Anime-style sprite animation using Pygame
* 🧵 **Threaded architecture** ensures smooth animation even while the AI is generating responses
* 🧠 Persistent memory through conversation history for contextual replies
* 💾 Local `.exe` build (no Python installation needed)
* 🔐 Source code available (API keys removed for security)

---

## ⚙️ How It Works

1. **Frontend (Pygame)**
   Handles user input, renders GPT-chan sprites (idle/talking), and updates the interface in real time.
2. **Backend (Gemini API)**
   User messages are sent to Gemini 2.5-Flash; responses are appended to the conversation history, enabling short-term conversational memory.
3. **Speech Engine (Edge-TTS)**
   The text reply is converted to an MP3 voice file and played immediately.
4. **Threading Technique**
   The function handling Gemini and TTS runs in a **separate thread** (`threading.Thread`), allowing the **main Pygame loop** to continue refreshing the UI and sprite animation without freezing.

---

## 🧙🏻‍♂️ Installation

### 🅰️ Option 1 — Run the Executable (Recommended)

1. Download `AnimeWaifuGPT.exe`.
2. Run the file — no setup needed.
3. Type your message and press **Enter** to chat with GPT-chan.

### 🅱️ Option 2 — Run the Source Code

```bash
git clone https://github.com/<your-username>/AnimeWaifuGPT.git
cd AnimeWaifuGPT
pip install -r requirements.txt
python main.py
```

> ⚠️ **Note:** Add your own Google Gemini API keys in `main.py` before running.

---


## 🧑‍💻 Author

**MD Thamed Bin Zaman Chowdhury**
Department of Civil Engineering, BUET
GitHub: [Thamed-Chowdhury](https://github.com/Thamed-Chowdhury)

---

## 🦤 Credits

* [Pygame](https://www.pygame.org/) — 2D rendering and animation
* [Google Gemini API](https://ai.google.dev/) — AI text generation
* [Edge-TTS](https://pypi.org/project/edge-tts/) — speech synthesis
* [pygame_gui](https://pygame-gui.readthedocs.io/) — input and UI management

---

## 📜 License

This project is released under the **MIT License** — you are free to modify and distribute it for non-commercial or educational purposes.

---

## 🖼️ Screenshot

<img width="1004" height="468" alt="image" src="https://github.com/user-attachments/assets/5b50a850-d1c5-4054-8c90-8369b98caa3a" />

---

### 🌸 “Konnichiwa, senpai~! GPT-chan is ready to chat — and she remembers your past conversations!” 🌸
