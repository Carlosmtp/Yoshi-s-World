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
        self.status = self.text_font.render("", True, (255, 255, 255))
        self.winner = self.text_font.render("", True, (255, 255, 255))
        self.player_score = self.text_font.render("Jugador: 0", True, (255, 255, 255))
        self.enemy_score = self.text_font.render("Enemigo: 0", True, (255, 255, 255))
        self.restart_button_same = pygame.Rect(680, 550, 165, 50)
        self.restart_button_initial = pygame.Rect(880, 550, 165, 50)
        self.restart_button_new = pygame.Rect(1080, 550, 165, 50)
        self.restart_button_new_color = (155, 196, 188)
        self.restart_button_color = (155, 196, 188)
        self.restart_button_same_color = (155, 196, 188)
        self.restart_button_text = self.small_font.render("posiciones actuales", True, (34, 31, 28))
        self.restart_button_same_text = self.small_font.render("posiciones iniciales", True, (34, 31, 28))
        self.restart_button_new_game = self.small_font.render("nuevas posiciones", True, (34, 31, 28))
        self.is_player_turn = False 

    def move_player_gui(self, move):
        if not self.is_player_turn:
            return
        mouse_pos = pygame.mouse.get_pos()
        for move in self.game.get_possible_moves(self.pos_jugador):
            move_rect = pygame.Rect(move[1] * 80, move[0] * 80, 80, 80)
            if move_rect.collidepoint(mouse_pos):
                self.game.move_player(move)
                self.current_cursor = move
                self.is_player_turn = False

    def move_enemy_gui(self):
        enemy_move = self.game.minimax(self.game.difficulty, False)[1]
        if enemy_move is not None:
            self.game.move_enemy(enemy_move)
            self.is_player_turn = True
        else:
            self.is_player_turn = True
    
    def update_board(self):
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
        self.screen.blit(self.difficulty, (700, 110))
    
    def update_scores(self):
        self.player_score = self.text_font.render("Jugador: " + str(self.game.player_score), True, (255, 255, 255))
        self.enemy_score = self.text_font.render("Enemigo: " + str(self.game.enemy_score), True, (255, 255, 255))
        self.screen.blit((pygame.transform.scale(pygame.image.load('images/red_yoshi.png'), (30, 30))), (700, 256))
        self.screen.blit((pygame.transform.scale(pygame.image.load('images/green_yoshi.png'), (30, 30))), (1000, 256))
        self.screen.blit(self.player_score, (740, 260))
        self.screen.blit(self.enemy_score, (1040, 260))
        
    def draw_actual_turn(self, player):
        if player:
            pygame.draw.rect(self.screen, (255,0,0), (680,180,240,130), 5)
            self.screen.blit(self.turn_text, (700, 200))
        else:
            pygame.draw.rect(self.screen, (0,255,0), (980,180,240,130), 5)
            self.screen.blit(self.turn_text, (1000, 200))
            
    def possible_moves_hover(self, possible_moves):
        mouse_pos = pygame.mouse.get_pos()
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
            
            
    def draw_board(self):
        while True:
            if self.game.enemy_score == self.game.player_score == 1:
                self.update_board()
                self.update_scores()
                self.draw_actual_turn(False)
                pygame.display.flip()
            pygame.display.set_caption('Yoshi\'s world')
            if self.is_player_turn == False:
                time.sleep(1)
                self.move_enemy_gui()
                pygame.event.clear()
                self.is_player_turn = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if (self.is_player_turn and self.game.get_possible_moves(self.pos_jugador) != []) or self.game.is_game_over() == True:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.restart_button_same.collidepoint(event.pos):
                            self.game = Game(self.game.difficulty, self.game.player_pos, self.game.enemy_pos)
                            self.is_player_turn = False
                            break
                        elif self.restart_button_initial.collidepoint(event.pos):
                            self.game = Game(self.game.difficulty, self.game.initial_player_pos, self.game.initial_enemy_pos)
                            self.is_player_turn = False
                            break
                        elif self.restart_button_new.collidepoint(event.pos):
                            self.game = Game(self.game.difficulty)
                            self.is_player_turn = False
                            break
                        elif (self.is_player_turn and (self.board.collidepoint(event.pos))):
                            self.move_player_gui(self.current_cursor)
                            break
                    if self.game.get_possible_moves(self.pos_enemigo) == []:
                        self.is_player_turn = True
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
                    
            self.update_board()
            possible_moves = self.game.get_possible_moves(self.pos_jugador)
            self.possible_moves_hover(possible_moves)
            self.game.update_scores()
            self.update_scores()
            if self.is_player_turn and self.game.get_possible_moves(self.pos_jugador) != []:
                self.draw_actual_turn(True)
            elif not self.is_player_turn and self.game.get_possible_moves(self.pos_enemigo) != []:
                self.draw_actual_turn(False)
            elif self.game.get_possible_moves(self.pos_enemigo) == [] and self.game.get_possible_moves(self.pos_jugador) != []:
                self.status = self.text_font.render("Enemigo sin movimientos, pasando turno...", True, (255, 255, 255))
                self.screen.blit(self.status, (680, 400))
                self.draw_actual_turn(True)
                pygame.display.flip()
                time.sleep(1)
                self.is_player_turn = True
            elif self.game.get_possible_moves(self.pos_jugador) == [] and self.game.get_possible_moves(self.pos_enemigo) != []:
                self.status = self.text_font.render("Jugador sin movimientos, pasando turno...", True, (255, 255, 255))
                self.screen.blit(self.status, (680, 400))
                self.draw_actual_turn(False)
                self.is_player_turn = False
            elif self.game.is_game_over:
                self.winner = self.text_font.render("Empate", True, (255, 255, 255))
                if self.game.player_score > self.game.enemy_score:
                    self.winner = self.text_font.render("¡Ganaste!", True, (255, 255, 255))
                elif self.game.player_score < self.game.enemy_score:
                    self.winner = self.text_font.render("¡Perdiste!", True, (255, 255, 255))
                self.status = self.text_font.render("¡Juego terminado!", True, (255, 255, 255))
                self.is_player_turn = True
                self.screen.blit(self.status, (680, 400))
                self.screen.blit(self.winner, (680, 450))
            self.update_scores()
            pygame.draw.rect(self.screen, self.restart_button_color, (680, 550, 165, 50))
            self.screen.blit(self.restart_button_text, (685, 565))
            pygame.draw.rect(self.screen, self.restart_button_same_color, (880, 550, 165, 50))
            self.screen.blit(self.restart_button_same_text, (885, 565))
            pygame.draw.rect(self.screen, self.restart_button_new_color, (1080, 550, 165, 50))
            self.screen.blit(self.restart_button_new_game, (1085, 565))
            pygame.display.flip()