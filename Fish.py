import numpy as np
from random import random, uniform, randint
from SpriteSheets import SpriteSheet

import pygame

class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, Game):
        pygame.sprite.Sprite.__init__(self)

        self.image = None
        self.react = None
        self.screen = Game.screen
        self.S = np.array([x, y])

    def blitme(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.S[0], self.S[1]
        self.screen.blit(self.image, self.rect)

    def move(self, ds):
        t = self.S + ds
        width, height = self.screen.get_size()
        if t[1]>0 and t[1]<(height-20) and t[0]>0 and t[0]<(width-15):
            self.S += ds

class FishSet:
    def __init__(self, game, fishes):
        self.game = game
        self.pieces = []
        self._load_pieces(fishes)

    def _load_pieces(self, fish_list):
        filename = 'images/small_fish.png'
        piece_ss = SpriteSheet(filename)

        fish_rect = (0, 0, 20, 15)
        fish_image = piece_ss.image_at(fish_rect, -1)

        for fish in fish_list:
            fish.image = fish_image
            fish.rect = fish_image.get_rect()
            self.game.fish_group.add(fish)
            self.pieces.append(fish)