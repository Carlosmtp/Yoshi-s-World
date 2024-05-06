import pygame
import os

class GameGUI:
    def __init__(self, game=None):
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.init()
        self.empty = pygame.transform.scale(pygame.image.load('images/empty_tile.png'), (80, 80))
        self.green_yoshi = pygame.transform.scale(pygame.image.load('images/green_yoshi.png'), (80, 80))
        self.red_yoshi = pygame.transform.scale(pygame.image.load('images/red_yoshi.png'), (80, 80))
        self.green_tile = pygame.transform.scale(pygame.image.load('images/green_tile.png'), (80, 80))
        self.red_tile = pygame.transform.scale(pygame.image.load('images/red_tile.png'), (80, 80))
        self.brush_tile = pygame.transform.scale(pygame.image.load('images/brush_tile.png'), (80, 80))
        self.background = pygame.transform.scale(pygame.image.load('images/game_background.png'), (80, 80))
        self.main_title = pygame.transform.scale(pygame.image.load('images/game_title.png'), (511, 80))
        self.screen = pygame.display.set_mode((1280, 640))
        self.screen.fill((255, 255, 255))
        self.pos_jugador = None
        self.pos_enemigo = None
        self.game = game
        self.current_cursor = None
        text_font = pygame.font.Font(None, 40)
        self.title = text_font.render("¡No hay movimientos posibles!", True, (0, 255, 0))
        
            
    def get_posible_moves(self):
        posible_moves = []
        if self.pos_jugador is not None:
            i, j = self.pos_jugador
            moves = [(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1),
                     (i+1, j+2), (i+1, j-2), (i-1, j+2), (i-1, j-2)]
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8 and self.game[move[0]][move[1]] == 0:
                    posible_moves.append(move)
        return posible_moves
    
    def draw_board(self):
        while True:
            pygame.display.set_caption('Yoshi\'s world')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for move in self.get_posible_moves():
                        move_rect = pygame.Rect(move[1] * 80, move[0] * 80, 80, 80)
                        if move_rect.collidepoint(mouse_pos):
                            self.game[self.pos_jugador[0]][self.pos_jugador[1]] = 3
                            self.game[move[0]][move[1]] = 1
                            self.pos_jugador = (move[0], move[1])
                            self.current_cursor = move
                            break
                            

            self.screen.fill((255, 255, 255))
            for i in range(8):
                for j in range(16):
                    if j>7:
                        self.screen.blit(self.background, (j * 80, i * 80))
                    else:
                        if self.game[i][j] == 0:
                            self.screen.blit(self.empty, (j * 80, i * 80))
                        elif self.game[i][j] == 1:
                            self.pos_jugador = (i, j)
                            self.screen.blit(self.green_yoshi, (j * 80, i * 80))
                        elif self.game[i][j] == 2:
                            self.pos_enemigo = (i, j)
                            self.screen.blit(self.red_yoshi, (j * 80, i * 80))
                        elif self.game[i][j] == 2:
                            self.screen.blit(self.red_yoshi, (j * 80, i * 80))
                        elif self.game[i][j] == 3:
                            self.screen.blit(self.green_tile, (j * 80, i * 80))
                        elif self.game[i][j] == 4:
                            self.screen.blit(self.red_tile, (j * 80, i * 80))
            self.screen.blit(self.main_title, (700, 30))

            
            # Obtener movimientos posibles
            posible_moves = self.get_posible_moves()
            
            # Dibujar movimientos posibles si el mouse está sobre ellos
            mouse_pos = pygame.mouse.get_pos()
            if posible_moves == []:
                self.screen.blit(self.title, (700, 150))
            for move in posible_moves:
                move_rect = pygame.Rect(move[1] * 80, move[0] * 80, 80, 80)
                if move_rect.collidepoint(mouse_pos):
                    self.screen.blit(self.brush_tile, (move[1] * 80, move[0] * 80))
                    if move[0] < self.pos_jugador[0]:
                        if move[1] > self.pos_jugador[1] - 2 and move[1] < self.pos_jugador[1] + 2:
                            pygame.draw.circle(self.screen, (201, 201, 201), (self.pos_jugador[1] * 80 + 40, (self.pos_jugador[0] - 1) * 80 + 40), 20)
                            pygame.draw.circle(self.screen, (201, 201, 201), (self.pos_jugador[1] * 80 + 40, (self.pos_jugador[0] - 2) * 80 + 40), 20)
                    elif move[0] > self.pos_jugador[0]:
                        if move[1] > self.pos_jugador[1] - 2 and move[1] < self.pos_jugador[1] + 2:
                            pygame.draw.circle(self.screen, (201, 201, 201), (self.pos_jugador[1] * 80 + 40, (self.pos_jugador[0] + 1) * 80 + 40), 20)
                            pygame.draw.circle(self.screen, (201, 201, 201), (self.pos_jugador[1] * 80 + 40, (self.pos_jugador[0] + 2) * 80 + 40), 20)
                    if move[1] < self.pos_jugador[1]:
                        if move[0] > self.pos_jugador[0] - 2 and move[0] < self.pos_jugador[0] + 2:
                            pygame.draw.circle(self.screen, (201, 201, 201), ((self.pos_jugador[1] - 1) * 80 + 40, self.pos_jugador[0] * 80 + 40), 20)
                            pygame.draw.circle(self.screen, (201, 201, 201), ((self.pos_jugador[1] - 2) * 80 + 40, self.pos_jugador[0] * 80 + 40), 20)
                    elif move[1] > self.pos_jugador[1]:
                        if move[0] > self.pos_jugador[0] - 2 and move[0] < self.pos_jugador[0] + 2:
                            pygame.draw.circle(self.screen, (201, 201, 201), ((self.pos_jugador[1] + 1) * 80 + 40, self.pos_jugador[0] * 80 + 40), 20)
                            pygame.draw.circle(self.screen, (201, 201, 201), ((self.pos_jugador[1] + 2) * 80 + 40, self.pos_jugador[0] * 80 + 40), 20)
            pygame.display.flip()
