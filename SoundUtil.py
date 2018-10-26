import pygame


class PlaySound:

    def mp3_play(self, file, folder=''):

        if folder != '':
            file = folder + '\\' + file

        if not str(file).endswith('.mp3'):
            file += '.mp3'

        print('Play :', file)
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
