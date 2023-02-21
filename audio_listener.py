import speech_recognition as sr


class AudioListener:
    def __init__(self, keyword="computer", system_name="computer"):
        self.keyword = keyword
        self.system_name = system_name
        self.message = ""

    def __str__(self):
        return self.message

    def get_message_from_audio(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(f"\nListening for keyword '{self.keyword}'...")
            audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            if self.keyword in text:
                print(f"Keyword '{self.keyword}' detected.\n")
                self.remove_keyword(text)
                return self.message
            else:
                print(f"Keyword not detected, please try again.\n")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    def remove_keyword(self, text):
        output_words = text.split()
        if output_words[0] == self.keyword:
            del output_words[0]
        elif output_words[-1] == self.keyword:
            del output_words[-1]
        self.message = " ".join(output_words)
