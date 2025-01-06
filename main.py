import  pyttsx3 #!pip install pyttsx3
import speech_recognition as sr
def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getproperty('voices')
    engine.setproperty('voice',voices[1].id)
    rate = engine.getproperty('rate')
    engine.setproperty('rate',rate-50)
    volume = engine.getproperty('volume')
    engine.setproperty('volume',volume+0.25)
    return engine


def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

    speak("hellow, iam nageswar")
