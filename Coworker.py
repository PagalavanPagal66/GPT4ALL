from googletrans import Translator
from pyttsx3 import init
import speech_recognition as sr
import gtts as gt


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)

def takeCommand(lang):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        #st.write("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        #st.write("Recognizing......")
        query = r.recognize_google(audio, language=lang)
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Unable to Recognizing your voice.")
        #st.write("Unable to Recognizing your voice.")
        return "None"
    return query


langtocode = {
    "Bengali": "bn-IN",
    "English-Aus": "en-AU",
    "English-Can": "en-CA",
    "English-Ind": "en-IN",
    "English-US": "en-US",
    "French": "fr-FR",
    "German": "de-DE",
    "Gujarati": "gu-IN",
    "Hindi": "hi-IN",
    "Japanese": "ja-JP",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Marathi": "mr-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
}

def save(text,code):
    tts = gt.gTTS(text=text, lang=code)
    filename = "voicespeech.mp3"
    tts.save(filename)

def trans(statement,code):
    translator = Translator()
    return translator.translate(statement , dest= code)

