# 🎙️ Voice-Controlled Raspberry Pi Assistant for the Visually Impaired

An AI-powered voice assistant designed to assist visually impaired users using a Raspberry Pi. It responds to voice commands, fetches live news and weather, announces time, and speaks back to the user using speech synthesis.

---

## 🚀 Features

- 🎧 Voice-controlled interaction
- 🗞️ Real-time news updates (NewsAPI / SerpAPI)
- 🌦️ Live weather updates (OpenWeatherMap API)
- 🕒 Tells current time
- 🗣️ Text-to-speech output (using `gTTS` / `pyttsx3`)
- 💻 Lightweight: Runs on Raspberry Pi 3/4

---

## 🔐 API Keys Used

| Service             | Purpose                    | Get API Key From                             |
|---------------------|-----------------------------|-----------------------------------------------|
| **NewsAPI**         | Fetching live news articles | [newsapi.org](https://newsapi.org/)           |
| **SerpAPI**         | Google-based news fallback  | [serpapi.com](https://serpapi.com/)           |
| **OpenWeatherMap**  | Fetching weather info       | [openweathermap.org](https://openweathermap.org/) |
| *(Optional)* OpenAI | Future RAG/Q&A integration  | [platform.openai.com](https://platform.openai.com/) |

➡️ **Place your keys in a `config.py` file:**
```python
NEWS_API_KEY = "your_newsapi_key"
SERPAPI_KEY = "your_serpapi_key"
WEATHER_API_KEY = "your_openweather_api_key"
OPENAI_API_KEY = "your_openai_key"  # optional

Tech Stack
Language: Python 3

Libraries: speech_recognition, gTTS, pyttsx3, requests, playsound

Platform: Raspberry Pi

Setup Instructions
Clone the Repository
git clone https://github.com/yourusername/raspberry-voice-assistant.git
cd raspberry-voice-assistant

Install Dependencies
pip install -r requirements.txt

Add API Keys
Create a config.py with your keys (see above).

Run the Assistant
python main.py

