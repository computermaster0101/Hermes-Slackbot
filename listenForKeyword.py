import speech_recognition as sr
import subprocess

def listen_for_keyword(keyword):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for keyword '" + keyword + "'...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        if keyword in text:
            print("Keyword '" + keyword + "' detected.")
            return text
        else:
            print("Keyword not detected, please try again.")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio.")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def write_to_file(text):
    with open("output.txt", "w") as f:
        f.write(text)
        print("Text written to output.txt.")

keyword = "computer"
text = listen_for_keyword(keyword)
if text:
    write_to_file(text)
