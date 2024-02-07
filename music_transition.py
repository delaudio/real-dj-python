import os
import pygame
import threading
from pydub import AudioSegment
from pydub.playback import play
import time

# Initialize pygame mixer
pygame.mixer.init()

def fade_volume(sound, start_volume, end_volume, duration):
    step = (end_volume - start_volume) / (duration * 1000) # volume change per millisecond
    for t in range(duration * 1000):
        volume = start_volume + step * t
        sound.set_volume(volume)
        time.sleep(0.001)

def play_with_transition(file_a, file_b, transition_duration=30):
    # Load files
    sound_a = AudioSegment.from_mp3(file_a)
    sound_b = AudioSegment.from_mp3(file_b)

    # Play sound A
    play(sound_a[:3*60*1000])  # Play first 3 minutes

    # Start fading out sound A and fading in sound B
    fade_thread_a = threading.Thread(target=fade_volume, args=(sound_a, 1, 0, transition_duration))
    fade_thread_b = threading.Thread(target=fade_volume, args=(sound_b, 0, 1, transition_duration))
    fade_thread_a.start()
    fade_thread_b.start()

    # Play sound B while fading
    play(sound_b[:3*60*1000 + transition_duration*1000])

    fade_thread_a.join()
    fade_thread_b.join()

def main():
    folder_path = "/Users/fdg/Documents/accurat-13-02"
    files = [file for file in os.listdir(folder_path) if file.endswith('.mp3')]

    while True:
        for i in range(0, len(files), 2):
            file_a = os.path.join(folder_path, files[i])
            file_b = os.path.join(folder_path, files[(i + 1) % len(files)])
            play_with_transition(file_a, file_b)

if __name__ == "__main__":
    main()
