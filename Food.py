from SpriteSheets import SpriteSheet
from random import random, uniform, randint

import pygame

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, Game):
        pygame.sprite.Sprite.__init__(self)

        self.X = x
        self.Y = y
        self.image = None
        self.react = None
        self.screen = Game.screen

    def blitme(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.X, self.Y
        self.screen.blit(self.image, self.rect)

class FoodSet:
    def __init__(self, game, foods):
        self.game = game
        self.pieces = []
        self._load_pieces(foods)

    def _load_pieces(self, foods):
        filename = 'images/food.png'
        piece_ss = SpriteSheet(filename)

        food_rect = (0, 0, 10, 10)
        food_image = piece_ss.image_at(food_rect)
        for food in foods:
            food.image = food_image
            food.rect = food_image.get_rect()
            self.game.food_group.add(food)
            self.pieces.append(food)
