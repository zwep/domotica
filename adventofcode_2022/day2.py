import os
import numpy as np
from adventofcode_2022.helper import DPATH


class Game:
    def __init__(self):
        self.input_translator = {'x': 'a', 'y': 'b', 'z': 'c'}
        self.move_score = ['a', 'b', 'c']

    @staticmethod
    def score_move(move):
        if move in ['a', 'x']:
            # Rock
            result = 1
        elif move in ['b', 'y']:
            # Paper
            result = 2
        else:
            # Scissor
            result = 3
        return result

    def score_game(self, move, my_move):
        my_move_trans = self.input_translator.get(my_move, my_move)
        move_score = self.score_move(move)
        my_move_score = self.score_move(my_move_trans)
        difference = move_score - my_move_score
        if difference == 0:
            return 3
        elif difference in [-2, 1]:
            # loss
            return 0
        elif difference in [-1, 2]:
            return 6

    def score_result(self, move, my_move):
        result_game = self.score_game(move, my_move)
        result_move = self.score_move(my_move)
        return result_game + result_move

    def play_game_part_1(self, puzzle_input):
        total_score = 0
        for (move, my_move) in puzzle_input:
            total_score += self.score_result(move, my_move)
        return total_score

    def get_my_move(self, move, my_move):
        # x means lose
        # y means draw
        # z means win
        if my_move == 'x':
            # Losing move
            new_move = self.move_score[(self.move_score.index(move)-1) % 3]
        elif my_move == 'y':
            new_move = move
        else:
            # Winning move
            new_move = self.move_score[(self.move_score.index(move) + 1) % 3]
        return new_move

    def play_game_part_2(self, puzzle_input):
        total_score = 0
        for (move, my_move) in puzzle_input:
            my_move = self.get_my_move(move, my_move)
            total_score += self.score_result(move, my_move)
        return total_score


dfile = os.path.join(DPATH, 'day2.txt')
with open(dfile, 'r') as f:
    puzzle_input = f.readlines()

puzzle_input = [[y.lower() for y in x.strip().split()] for x in puzzle_input]
puzzle_input = [x for x in puzzle_input if len(x) ==2]
game_obj = Game()
game_obj.play_game_part_1(puzzle_input)
game_obj.play_game_part_2(puzzle_input)

