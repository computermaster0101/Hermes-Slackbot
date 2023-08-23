import os
import sys
from gtts import gTTS
import pygame

def text_to_speech(text):
    tts = gTTS(text)
    tts.save("output.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()
    pygame.mixer.music.load("output.mp3")

    # Play the audio
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(10)

    # Clean up: remove the generated audio file
    os.remove("output.mp3")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
        words = input_text.split(" ", 1)  # Split into two parts, at most 1 split
        if len(words) > 1:
            text_to_speech(words[1])  # Use the second part after the split
        else:
            print("Please provide a text to convert to speech (with at least two words).")
    else:
        print("Please provide a text to convert to speech.")
