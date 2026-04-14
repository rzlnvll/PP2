import pygame
import os

class MusicPlayer:
    def __init__(self, songs):
        pygame.mixer.init()
        self.songs = songs
        self.i = 0

    def play(self):
        pygame.mixer.music.load(self.songs[self.i])
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        self.i += 1
        if self.i == len(self.songs):
            self.i = 0
        self.play()

    def back(self):
        self.i -= 1
        if self.i < 0:
            self.i = len(self.songs) - 1
        self.play()

    def name(self):
        return os.path.basename(self.songs[self.i])

    def time(self):
        return pygame.mixer.music.get_pos() // 1000