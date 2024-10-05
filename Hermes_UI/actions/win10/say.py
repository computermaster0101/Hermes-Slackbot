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

    # Stop and close the mixer
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Clean up: remove the generated audio file
    os.remove("output.mp3")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
        if input_text.startswith('say '):
            input_text = input_text[4:]
        print(input_text)
        text_to_speech(input_text)
    else:
        print("Please provide a text to convert to speech.")
