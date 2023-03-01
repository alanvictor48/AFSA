import sys, pygame
from Fish import FishSet

from pygame.sprite import Group

from AFSA import AFSA


import numpy as np

class Game:

    def __init__(self, width, height):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
                (width, height), pygame.RESIZABLE)
        pygame.display.set_caption("AFSA")

        self.fish_group = Group()
        self.food_group = Group()

        self.afsa = AFSA(self, 3, 10)

        self.fish_set = self.afsa.fish_set
        self.food_set = self.afsa.food_set

    def run_game(self):
        while True:
            self.clock.tick(500)

            self._check_events()
            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        self.screen.fill((0, 255, 255))

        for fish in self.fish_set.pieces:
            result = pygame.sprite.spritecollideany(fish, self.food_group)
            if result:
                self.food_group.remove(result)
                self.food_set.pieces.remove(result)
                new_food = self.afsa.add_food()
                self.food_group.add(new_food)

        for fish in self.fish_set.pieces:
            fish.blitme()
            self.afsa.move()
        
        for food in self.food_set.pieces:
            food.blitme()

        pygame.display.flip()


if __name__ == '__main__':
    game = Game(600, 400)
    game.run_game()