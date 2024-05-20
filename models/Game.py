import random

class Game:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.world = [[0] * 8 for _ in range(8)]
        self.player_pos = random.randrange(8), random.randrange(8)
        self.enemy_pos = random.randrange(8), random.randrange(8)
        self.player_score = 0
        self.enemy_score = 0    
        while self.player_pos == self.enemy_pos:
            self.enemy_pos = random.randrange(8), random.randrange(8)
        for i in range(8):
            for j in range(8):
                if (i, j) == self.player_pos:
                    self.world[i][j] = 1
                elif (i, j) == self.enemy_pos:
                    self.world[i][j] = 2
                else:
                    self.world[i][j] = 0
                    
                    
    def update_scores(self):
        self.player_score = sum(row.count(3) for row in self.world) + sum(row.count(1) for row in self.world)
        self.enemy_score = sum(row.count(4) for row in self.world) + sum(row.count(2) for row in self.world)
                    
    def heuristic(self):
        green_score = sum(row.count(3) for row in self.world) + sum(row.count(1) for row in self.world)
        red_score = sum(row.count(4) for row in self.world) + sum(row.count(2) for row in self.world)
        return green_score - red_score
    
    def get_possible_moves(self, pos):
        posible_moves = []
        if pos is not None:
            i, j = pos
            moves = [(i+2, j+1), (i+2, j-1), (i-2, j+1), (i-2, j-1),
                     (i+1, j+2), (i+1, j-2), (i-1, j+2), (i-1, j-2)]
            for move in moves:
                if 0 <= move[0] < 8 and 0 <= move[1] < 8 and self.world[move[0]][move[1]] == 0:
                    posible_moves.append(move)
        return posible_moves
    
    
    def move_player(self, move):
        self.world[self.player_pos[0]][self.player_pos[1]] = 3
        self.world[move[0]][move[1]] = 1
        self.player_pos = move
        
    def move_enemy(self, move):
        if move is None:
            return
        self.world[self.enemy_pos[0]][self.enemy_pos[1]] = 4
        self.world[move[0]][move[1]] = 2
        self.enemy_pos = move
        
    def minimax(self, depth, player):
        if depth == 0 or self.is_game_over():
            return self.heuristic(), None  # Devuelve la puntuación y None como movimiento
        if player:
            best_score = float('-inf')
            best_move = None
            for move in self.get_possible_moves(self.player_pos):
                score, _ = self.minimax(depth-1, not player)  # Ignora el movimiento retornado
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in self.get_possible_moves(self.enemy_pos):
                score, _ = self.minimax(depth-1, not player)  # Ignora el movimiento retornado
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        
    def is_game_over(self):
        return not self.get_possible_moves(self.player_pos) or not self.get_possible_moves(self.enemy_pos)

