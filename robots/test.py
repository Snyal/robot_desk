
import speech_recognition as sr
listener = sr.Recognizer()
with sr.Microphone() as source:
    print(source)