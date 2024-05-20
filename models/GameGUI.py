import pygame
import os
import time
from models.Game import Game

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
        self.board = pygame.Rect(0, 0, 640, 640)
        self.screen.fill((255, 255, 255))
        self.pos_jugador = None
        self.pos_enemigo = None
        self.game = game
        self.current_cursor = None
        self.text_font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 24)
        self.difficulty = self.text_font.render("Dificultad: " + difficulty, True, (255, 255, 255))
        self.turn_text = self.text_font.render("Jugando...", True, (255, 255, 255))
        self.status = self.text_font.render("¡No hay movimientos posibles!", True, (255, 255, 255))
        self.player_score = self.text_font.render("Jugador: 0", True, (255, 255, 255))
        self.enemy_score = self.text_font.render("Enemigo: 0", True, (255, 255, 255))
        self.restart_button_same = pygame.Rect(680, 550, 165, 50)
        self.restart_button_initial = pygame.Rect(880, 550, 165, 50)
        self.restart_button_new = pygame.Rect(1080, 550, 165, 50)
        self.restart = pygame.Surface(self.text_font.render("Reiniciar:", True, (255, 255, 255)).get_size(), pygame.SRCALPHA);self.restart.blit(self.text_font.render("Reiniciar:", True, (255, 255, 255)), (0, 0));self.restart_button_color = (155, 196, 188)
        self.restart_button_new_color = (155, 196, 188)
        self.restart_button_color = (155, 196, 188)
        self.restart_button_same_color = (155, 196, 188)
        self.buttons_state = True
        self.restart_button_text = self.small_font.render("posiciones actuales", True, (34, 31, 28))
        self.restart_button_same_text = self.small_font.render("posiciones iniciales", True, (34, 31, 28))
        self.restart_button_new_game = self.small_font.render("nuevas posiciones", True, (34, 31, 28))
        self.is_player_turn = False  # Booleano para controlar el turno

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
    
    def activate_buttons(self):
        self.restart_button_color = (155, 196, 188)
        self.restart_button_new_color = (155, 196, 188)
        self.restart_button_same_color = (155, 196, 188)
        self.restart.set_alpha(255)
        self.buttons_state = True
        
    def deactivate_buttons(self):
        self.restart_button_color = (34, 31, 28)
        self.restart_button_new_color = (34, 31, 28)
        self.restart_button_same_color = (34, 31, 28)
        self.restart.set_alpha(0)
        self.buttons_state = False

    def draw_board(self):
        initial_move = True
        while True:
            pygame.display.set_caption('Yoshi\'s world')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button_same.collidepoint(event.pos):
                        self.game = Game(self.game.difficulty, self.game.player_pos, self.game.enemy_pos)
                        self.is_player_turn = False
                        initial_move = True
                        break
                    elif self.restart_button_initial.collidepoint(event.pos):
                        self.game = Game(self.game.difficulty, self.game.initial_player_pos, self.game.initial_enemy_pos)
                        self.is_player_turn = False
                        initial_move = True
                        break
                    elif self.restart_button_new.collidepoint(event.pos):
                        self.game = Game(self.game.difficulty)
                        self.is_player_turn = False
                        initial_move = True
                        break
                    elif (self.is_player_turn and (self.board.collidepoint(event.pos))):
                        self.deactivate_buttons()
                        self.move_player_gui(self.current_cursor)
                        
                        break
                if event.type == pygame.MOUSEBUTTONUP and self.board.collidepoint(event.pos):
                    if not self.is_player_turn:
                        time.sleep(1)
                        self.move_enemy_gui()
                        self.activate_buttons()
                        break
                if event.type == pygame.MOUSEMOTION:
                    if self.restart_button_same.collidepoint(event.pos):
                        self.restart_button_color = (211, 255, 233)
                    else:
                        self.restart_button_color = (155, 196, 188)
                    if self.restart_button_initial.collidepoint(event.pos):
                        self.restart_button_same_color = (211, 255, 233)
                    else:
                        self.restart_button_same_color = (155, 196, 188)
                    if self.restart_button_new.collidepoint(event.pos):
                        self.restart_button_new_color = (211, 255, 233)
                    else:
                        self.restart_button_new_color = (155, 196, 188)
                    

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
                            self.screen.blit(self.red_yoshi, (j * 80, i * 80))
                        elif self.game.world[i][j] == 2:
                            self.pos_enemigo = (i, j)
                            self.screen.blit(self.green_yoshi, (j * 80, i * 80))
                        elif self.game.world[i][j] == 3:
                            self.screen.blit(self.red_tile, (j * 80, i * 80))
                        elif self.game.world[i][j] == 4:
                            self.screen.blit(self.green_tile, (j * 80, i * 80))
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
            self.screen.blit((pygame.transform.scale(pygame.image.load('images/red_yoshi.png'), (30, 30))), (700, 256))
            self.screen.blit((pygame.transform.scale(pygame.image.load('images/green_yoshi.png'), (30, 30))), (1000, 256))
            if self.is_player_turn:
                pygame.draw.rect(self.screen, (255,0,0), (680,180,240,130), 5)
                self.screen.blit(self.turn_text, (700, 200))
            elif self.is_player_turn == False or initial_move:
                print("Enemy's turn")
                self.deactivate_buttons()
                pygame.draw.rect(self.screen, (0,255,0), (980,180,240,130), 5)
                self.screen.blit(self.turn_text, (1000, 200))
            self.screen.blit(self.player_score, (740, 260))
            self.screen.blit(self.enemy_score, (1040, 260))
            self.screen.blit(self.restart, (680, 480))
            pygame.draw.rect(self.screen, self.restart_button_color, (680, 550, 165, 50))
            self.screen.blit(self.restart_button_text, (685, 565))
            pygame.draw.rect(self.screen, self.restart_button_same_color, (880, 550, 165, 50))
            self.screen.blit(self.restart_button_same_text, (885, 565))
            pygame.draw.rect(self.screen, self.restart_button_new_color, (1080, 550, 165, 50))
            self.screen.blit(self.restart_button_new_game, (1085, 565))
            pygame.display.flip()
            if initial_move:
                time.sleep(1)
                self.move_enemy_gui()
                initial_move = False
