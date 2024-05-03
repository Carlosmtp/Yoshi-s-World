import random

class Game:
    def __init__(self):
        self.world = [[0] * 8 for _ in range(8)]
        self.player_pos = random.randrange(8), random.randrange(8)
        self.enemy_pos = random.randrange(8), random.randrange(8)        
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