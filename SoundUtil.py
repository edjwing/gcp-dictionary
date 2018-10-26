import pygame


class PlaySound:

    def mp3_play(self, file, folder=''):

        # directory = str(os.curdir)
        # print('dir :', directory)
        # directory = directory + '\\' + self.path
        # print('dir :', directory)
        # os.chdir(directory)

        if folder != '':
            file = folder + '\\' + file

        if not str(file).endswith('.mp3'):
            file += '.mp3'

        print('Play :', file)
        pygame.mixer.init()
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()
