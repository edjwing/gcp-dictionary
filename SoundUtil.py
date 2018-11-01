import pygame
import time

class PlaySound:

    def mp3_play(self, file):
        print('Play :', file)
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        time.sleep(1)
