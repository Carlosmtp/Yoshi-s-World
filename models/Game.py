import copy
import random

class Game:
    def __init__(self, difficulty, initial_player_pos=None, initial_enemy_pos=None):
        self.difficulty = difficulty
        self.world = [[0] * 8 for _ in range(8)]
        if initial_player_pos is not None:
            self.initial_player_pos = initial_player_pos
        else:
            self.initial_player_pos = random.randrange(8), random.randrange(8)
        if initial_enemy_pos is not None:
            self.initial_enemy_pos = initial_enemy_pos
        else:
            self.initial_enemy_pos = random.randrange(8), random.randrange(8)
        self.player_pos = self.initial_player_pos
        self.enemy_pos = self.initial_enemy_pos
        self.player_score = 1
        self.enemy_score = 1    
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
        player_controlled = sum(row.count(1) for row in self.world) + sum(row.count(3) for row in self.world)
        enemy_controlled = sum(row.count(2) for row in self.world) + sum(row.count(4) for row in self.world)

        player_possible_moves = len(self.get_possible_moves(self.player_pos))
        enemy_possible_moves = len(self.get_possible_moves(self.enemy_pos))

        player_distance_to_enemy = self.manhattan_distance(self.player_pos, self.enemy_pos)

        heuristic_value = (player_controlled - enemy_controlled) * 0.3
        if player_possible_moves == 0:
            heuristic_value += -5.0
        elif enemy_possible_moves == 0:
            heuristic_value += 5.0
        else:
            heuristic_value += (player_possible_moves - enemy_possible_moves) * 0.6
        heuristic_value -= player_distance_to_enemy * 0.1
        return heuristic_value

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def get_possible_moves(self, pos):
        posible_moves = []
        if pos is not None:
            i, j = pos
            moves = [(i + 2, j + 1), (i + 2, j - 1), (i - 2, j + 1), (i - 2, j - 1),
                     (i + 1, j + 2), (i + 1, j - 2), (i - 1, j + 2), (i - 1, j - 2)]
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

    def clone(self):
        clone_game = Game(self.difficulty, self.player_pos, self.enemy_pos)
        clone_game.world = copy.deepcopy(self.world)
        clone_game.update_scores()
        return clone_game

    def minimax(self, depth, player):
        if depth == 0 or self.is_game_over():
            return self.heuristic(), None
        if player:
            best_score = float('-inf')
            best_move = None
            for move in self.get_possible_moves(self.player_pos):
                clone_game = self.clone()
                clone_game.move_player(move)
                score, _ = clone_game.minimax(depth - 1, not player)
                if score > best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move
        else:
            best_score = float('inf')
            best_move = None
            for move in self.get_possible_moves(self.enemy_pos):
                clone_game = self.clone()
                clone_game.move_enemy(move)
                score, _ = clone_game.minimax(depth - 1, not player)
                if score < best_score:
                    best_score = score
                    best_move = move
            return best_score, best_move

    def is_game_over(self):
        return self.get_possible_moves(self.player_pos) == self.get_possible_moves(self.enemy_pos) == []
