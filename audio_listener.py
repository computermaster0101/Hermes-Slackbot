import speech_recognition as sr
import subprocess
import os
import json
from datetime import datetime

class audio_listener:
	def __init__(self,keyword="computer",system_name="computer"):
		self.keyword=keyword
		self.system_name=system_name
		self.message={}

	def __str__(self):
		return (f"system_name: {self.system_name}\nkeyword: {self.keyword}\nmessage: {json.dumps(self.message)}")

	def listen_for_keyword(self):
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print(f"\nListening for keyword '{self.keyword}'...")
			audio = r.listen(source)
		try:
			text = r.recognize_google(audio)
			if self.keyword in text:
				print(f"Keyword '{self.keyword}' detected.\n")
				self.remove_keyword(text)
			else:
				print(f"Keyword not detected, please try again.\n")
		except sr.UnknownValueError:
			print("Google Speech Recognition could not understand audio.")
		except sr.RequestError as e:
			print("Could not request results from Google Speech Recognition service; {0}".format(e))

	def remove_keyword(self,text):
		now = datetime.now()
		timestamp = now.strftime('"timestamp":"%B %d, %Y at %I:%M%p"')
		outputWords = text.split()
		if outputWords[0] == self.keyword:
			del outputWords[0]
		elif outputWords[-1] == self.keyword:
			del outputWords[-1]
		self.message = {"device":self.system_name,"message": " ".join(outputWords),"timestamp":timestamp}
