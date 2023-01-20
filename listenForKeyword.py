import speech_recognition as sr
import subprocess
import os
import json
from datetime import datetime

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
	outputFile = os.path.expanduser("~\\OneDrive\\Apps\\Commands\computer0.txt")
	date_time = datetime.now()
	timestamp = date_time.strftime('"timestamp":"%B %d, %Y at %I:%M%p"')
	outputWords = text.split()
	if outputWords[0] == keyword:
		del outputWords[0]
	elif outputWords[-1] == keyword:
		del outputWords[-1]
	outputText = {"device":"computer0","message": " ".join(outputWords),"timestamp":timestamp}
	with open(outputFile, "w") as f:
		f.write(json.dumps(outputText))
		print(f"Text written to {outputFile}.")

keyword = "computer"
while(True):
	text = listen_for_keyword(keyword)
	if text:
		write_to_file(text)
