# 🎙️ Voice-Controlled Raspberry Pi Assistant for the Visually Impaired

An AI-powered voice assistant designed to help visually impaired users using Raspberry Pi. It recognizes voice commands, fetches real-time news, tells the time, and responds audibly using speech synthesis.

---

## 🚀 Features

- 🎧 Voice-controlled interaction
- 🗞️ Real-time news updates (NewsAPI / SerpAPI)
- 🕒 Voice-based time announcements
- 🗣️ Text-to-speech output using `gTTS` / `pyttsx3`
- 💻 Compatible with Raspberry Pi 3/4 (offline-capable)
- 🔊 Audible feedback and error handling

---

## 🔐 API Keys Used

| Service   | Purpose                | Where to Get It                            |
|-----------|------------------------|---------------------------------------------|
| **NewsAPI**   | Fetching live news articles | [https://newsapi.org/](https://newsapi.org/) |
| **SerpAPI**   | Alternative for news scraping via Google | [https://serpapi.com/](https://serpapi.com/) |
| *(Optional)* OpenAI | For future RAG/Q&A enhancement | [https://platform.openai.com/](https://platform.openai.com/) |

➡️ **Place your API keys in a file named `config.py`:**
```python
NEWS_API_KEY = "your_newsapi_key_here"
SERPAPI_KEY = "your_serpapi_key_here"
OPENAI_API_KEY = "your_openai_key_here"  # optional
