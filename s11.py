import pvporcupine
import pyaudio
import struct
import os
import json
import requests
from vosk import Model, KaldiRecognizer
from openai import OpenAI
from gtts import gTTS
from playsound import playsound
from langdetect import detect
import tempfile
from gnews import GNews
from datetime import datetime  # ✅ Added for real-time

# === CONFIGURATION ===
ACCESS_KEY = "access_key"
OPENAI_KEY = "OpenAI_key"
WEATHER_API_KEY = "API_key"
VOSK_PATH = "path"

# Initialize GNews
google_news = GNews(language='en', country='IN', period='1d', max_results=3)
client = OpenAI(api_key=OPENAI_KEY)

def speak(text):
    try:
        lang = detect(text)
        tts = gTTS(text=text, lang=lang)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            playsound(fp.name)
            os.remove(fp.name)
    except Exception as e:
        print(f"❌ TTS Error: {e}")
        print("📢 Assistant fallback:", text)

def recognize_speech_vosk():
    model = Model(VOSK_PATH)
    rec = KaldiRecognizer(model, 16000)
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000,
                      input=True, frames_per_buffer=4096)
    stream.start_stream()
    print("👂 Listening...")

    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            stream.stop_stream()
            stream.close()
            mic.terminate()
            return text.strip()

def get_location():
    try:
        res = requests.get("http://ip-api.com/json/").json()
        return res.get("city", "Delhi")
    except:
        return "Delhi"

def get_weather():
    city = get_location()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    try:
        res = requests.get(url).json()
        temp = res['main']['temp']
        desc = res['weather'][0]['description']
        return f"The current weather in {city} is {desc} with a temperature of {temp}°C."
    except:
        return "Sorry, I couldn't fetch the weather right now."

def get_datetime_info():
    now = datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %d %B %Y")
    return f"It is {time_str} on {date_str}."

def ask_gpt(prompt):
    try:
        print("🤔 Asking GPT...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Raspberry Pi assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"GPT error: {str(e)}"

def get_news():
    try:
        print("📰 Fetching news from GNews...")
        news = google_news.get_news(key="general")

        if not news:
            speak("Sorry, no news available right now.")
            return "No news available."

        headlines = []
        for item in news[:3]:
            title = item.get('title', '').strip()
            if title and title != '[Removed]':
                headlines.append(title)

        if not headlines:
            speak("No valid news headlines were found.")
            return "No valid headlines."

        response = "Here are the latest news headlines. " + ". ".join(headlines)
        speak(response)
        return "\n".join(headlines)

    except Exception as e:
        error_msg = f"News error: {str(e)}"
        print(error_msg)
        speak("There was an error getting the news.")
        return error_msg

def main():
    print("💬 Say 'Picovoice' to activate...")
    try:
        porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=["picovoice"])
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(rate=porcupine.sample_rate, channels=1,
                               format=pyaudio.paInt16, input=True,
                               frames_per_buffer=porcupine.frame_length)

        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("🚨 Hotword Detected!")
                speak("Yes? How can I help you?")
                command = recognize_speech_vosk()
                print("🧏 You said:", command)

                if not command:
                    speak("Sorry, I didn't catch that.")
                    continue

                cmd = command.lower()

                if "weather" in cmd or "मौसम" in cmd:
                    speak(get_weather())
                elif "news" in cmd or "headlines" in cmd:
                    get_news()
                elif any(word in cmd for word in ["time", "date", "clock", "समय", "तारीख", "वक्त", "दिन"]):
                    speak("Let me check the time for you.")
                    speak(get_datetime_info())
                elif "exit" in cmd or "goodbye" in cmd or "बंद" in cmd:
                    speak("Goodbye!")
                    break
                else:
                    reply = ask_gpt(command)
                    speak(reply)

    except KeyboardInterrupt:
        print("👋 Exiting Assistant...")

    finally:
        try:
            audio_stream.stop_stream()
            audio_stream.close()
            pa.terminate()
            porcupine.delete()
        except:
            pass

if __name__ == "__main__":
    main()
