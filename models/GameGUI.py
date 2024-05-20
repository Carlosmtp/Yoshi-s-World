import pygame
import os
import time

class GameGUI:
    def __init__(self, game=None, difficulty=None):
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
        self.text_font = pygame.font.Font(None, 40)
        self.difficulty = self.text_font.render("Dificultad: " + difficulty, True, (255, 255, 255))
        self.turn_text = self.text_font.render("Jugando...", True, (255, 255, 255))
        self.status = self.text_font.render("¡No hay movimientos posibles!", True, (255, 255, 255))
        self.player_score = self.text_font.render("Jugador: 0", True, (255, 255, 255))
        self.enemy_score = self.text_font.render("Enemigo: 0", True, (255, 255, 255))
        self.restart = self.text_font.render("Reiniciar", True, (255, 255, 255))
        self.is_player_turn = True  # Booleano para controlar el turno

    def move_player_gui(self, move):
        mouse_pos = pygame.mouse.get_pos()
        for move in self.game.get_possible_moves(self.pos_jugador):
            move_rect = pygame.Rect(move[1] * 80, move[0] * 80, 80, 80)
            if move_rect.collidepoint(mouse_pos):
                self.game.move_player(move)
                self.current_cursor = move
                self.is_player_turn = False  # Cambia el turno al enemigo

    def move_enemy_gui(self):
        enemy_move = self.game.minimax(self.game.difficulty, False)[1]
        if enemy_move is not None:
            self.game.move_enemy(enemy_move)
            self.is_player_turn = True  # Cambia el turno al jugador


    def draw_board(self):
        while True:
            print(self.is_player_turn)
            pygame.display.set_caption('Yoshi\'s world')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.is_player_turn:
                        self.move_player_gui(self.current_cursor)
                        break
                if event.type == pygame.MOUSEBUTTONUP:
                    if not self.is_player_turn:
                        time.sleep(2)
                        self.move_enemy_gui()
                        break

            self.screen.fill((255, 255, 255))
            for i in range(8):
                for j in range(16):
                    if j > 7:
                        self.screen.blit(self.background, (j * 80, i * 80))
                    else:
                        if self.game.world[i][j] == 0:
                            self.screen.blit(self.empty, (j * 80, i * 80))
                        elif self.game.world[i][j] == 1:
                            self.pos_jugador = (i, j)
                            self.screen.blit(self.green_yoshi, (j * 80, i * 80))
                        elif self.game.world[i][j] == 2:
                            self.pos_enemigo = (i, j)
                            self.screen.blit(self.red_yoshi, (j * 80, i * 80))
                        elif self.game.world[i][j] == 3:
                            self.screen.blit(self.green_tile, (j * 80, i * 80))
                        elif self.game.world[i][j] == 4:
                            self.screen.blit(self.red_tile, (j * 80, i * 80))
            self.screen.blit(self.main_title, (700, 30))

            # Obtener movimientos posibles
            possible_moves = self.game.get_possible_moves(self.pos_jugador)

            # Dibujar movimientos posibles si el mouse está sobre ellos
            mouse_pos = pygame.mouse.get_pos()
            if possible_moves == []:
                self.screen.blit(self.status, (700, 400))
            if self.is_player_turn:
                for move in possible_moves:
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
            self.screen.blit(self.difficulty, (700, 110))
            self.game.update_scores()
            self.player_score = self.text_font.render("Jugador: " + str(self.game.player_score), True, (255, 255, 255))
            self.enemy_score = self.text_font.render("Enemigo: " + str(self.game.enemy_score), True, (255, 255, 255))
            self.screen.blit((pygame.transform.scale(pygame.image.load('images/green_yoshi.png'), (30, 30))), (700, 256))
            self.screen.blit((pygame.transform.scale(pygame.image.load('images/red_yoshi.png'), (30, 30))), (1010, 256))
            if self.is_player_turn:
                pygame.draw.rect(self.screen, (0,255,0), (680,180,230,130), 5)
                self.screen.blit(self.turn_text, (700, 200))
            else:
                pygame.draw.rect(self.screen, (255,0,0), (980,180,230,130), 5)
                self.screen.blit(self.turn_text, (1000, 200))
            self.screen.blit(self.player_score, (740, 260))
            self.screen.blit(self.enemy_score, (1050, 260))
            self.screen.blit(self.restart, (700, 550))
            pygame.display.flip()
