import pygame
import os
import time

class GameGUI:
    def __init__(self, game):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.empty = pygame.transform.scale(pygame.image.load('images/empty_tile.png'), (100, 100))
        self.green_yoshi = pygame.transform.scale(pygame.image.load('images/green_yoshi.png'), (100, 100))
        self.red_yoshi = pygame.transform.scale(pygame.image.load('images/red_yoshi.png'), (100, 100))
        self.green_tile = pygame.transform.scale(pygame.image.load('images/green_tile.png'), (100, 100))
        self.red_tile = pygame.transform.scale(pygame.image.load('images/red_tile.png'), (100, 100))
        self.screen = pygame.display.set_mode((800, 800))
        self.screen.fill((255, 255, 255))
        self.game = game
        
    def draw_board(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.screen.fill((255, 255, 255))
            for i in range(8):
                for j in range(8):
                    if self.game[i][j] == 0:
                        self.screen.blit(self.empty, (j * 100, i * 100))
                    elif self.game[i][j] == 1:
                        self.screen.blit(self.green_yoshi, (j * 100, i * 100))
                    elif self.game[i][j] == 2:
                        self.screen.blit(self.red_yoshi, (j * 100, i * 100))
                    elif self.game[i][j] == 3:
                        self.screen.blit(self.green_tile, (j * 100, i * 100))
                    elif self.game[i][j] == 4:
                        self.screen.blit(self.red_tile, (j * 100, i * 100))
            pygame.display.flip()
            time.sleep(0.1)