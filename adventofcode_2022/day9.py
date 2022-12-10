import os
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


class MovingGame:
    def __init__(self, plot_output=False):
        self.current_head = np.array([0, 0])
        self.current_tail = np.array([0, 0])
        self.plot_output = plot_output
        self.tail_positions = [self.current_tail]
        self.head_plot_obj = AX.scatter(*self.current_head)
        self.tail_plot_obj = AX.scatter(*self.current_tail)

    def process_move(self, move_string):
        direction_string, step_size = move_string.split()
        step_size = int(step_size)
        for i_step in range(step_size):
            print(direction_string, i_step)
            if self.plot_output:
                plot_head(self)
                plot_tail(self)

            self.make_a_head_move(direction_string)
            difference_head_tail = (self.current_head - self.current_tail)
            distance_head_tail = np.sqrt(np.mean((self.current_tail - self.current_head) ** 2))
            # print('Distance before tail move', distance_head_tail)
            # print('Difference before tail move', difference_head_tail)
            # print('Status head ', self.current_head)
            # print('Status tail ', self.current_tail)
            if distance_head_tail > 1:
                self.make_a_tail_move(direction_string, difference_head_tail)
                self.tail_positions.append(np.copy(self.current_tail))

    def check_tail_move_part_2(self, direction_string):
        difference_head_tail = (self.current_head - self.current_tail)
        distance_head_tail = np.sqrt(np.mean((self.current_tail - self.current_head) ** 2))
        print('Distance before tail move', distance_head_tail)
        print('Difference before tail move', difference_head_tail)
        print('Status head ', self.current_head)
        print('Status tail ', self.current_tail)
        if distance_head_tail > 1:
            self.make_a_tail_move(direction_string, difference_head_tail)
            # self.tail_positions.append(np.copy(self.current_tail))
            return True
        return False

    def make_a_head_move(self, direction_string):
        # Only do single moves so that we track each position properly
        if direction_string == 'R':
            self.current_head += np.array([1, 0])
        elif direction_string == 'L':
            self.current_head += np.array([-1, 0])
        elif direction_string == 'U':
            self.current_head += np.array([0, 1])
        elif direction_string == 'D':
            self.current_head += np.array([0, -1])

    def make_a_tail_move(self, direction_string, difference):
        # Only do single moves so that we track each position properly
        temp_difference = difference / np.abs(difference)
        temp_difference[np.isnan(temp_difference)] = 0
        temp_difference = temp_difference.astype(int)
#        if all(np.abs(temp_difference) == 1):
        # tt_difference = (difference / np.abs(difference)).astype(int)
        # print(tt_difference)
        self.current_tail += temp_difference
            #pass
        # else:
        #     if direction_string == 'R':
        #         self.current_tail += np.array([1, 0])
        #     elif direction_string == 'L':
        #         self.current_tail += np.array([-1, 0])
        #     if direction_string == 'U':
        #         self.current_tail += np.array([0, 1])
        #     elif direction_string == 'D':
        #         self.current_tail += np.array([0, -1])


def process_move_part_2(move_string):
    direction_string, step_size = move_string.split()
    step_size = int(step_size)
    return direction_string, step_size


def plot_head(game_object):
    game_object.head_plot_obj.remove()
    game_object.head_plot_obj = AX.scatter(*game_object.current_head, c='y')
    plt.pause(0.01)


def plot_tail(game_object):
    game_object.tail_plot_obj.remove()
    game_object.tail_plot_obj = AX.scatter(*game_object.current_tail, c='g')
    plt.pause(0.01)


def plot_status(game_object_list):
    head_plot_obj = [AX.scatter(*x.current_head, c='y') for x in game_object_list]
    tail_plot_obj = [AX.scatter(*x.current_tail, c='g') for x in game_object_list]
    plt.pause(0.4)
    return head_plot_obj, tail_plot_obj


if __name__ == "__main__":
    dfile = os.path.join(DPATH, 'day9_test2.txt')
    with open(dfile, 'r') as f:
        puzzle_input = [x.strip() for x in f.readlines()]

    puzzle_input = [x for x in puzzle_input if x]

    # Create global figure/ax
    FIG, AX = plt.subplots()
    _ = AX.imshow(np.zeros((10, 10)))
    plt.grid()
    plt.gca().invert_yaxis()

    """
    Part 1
    """
    # game_object = MovingGame(plot_output=True)
    # # Run it...
    # for i_move in puzzle_input:
    #     game_object.process_move(i_move)
    #
    # print('Tail positions ', len(set([tuple(x) for x in game_object.tail_positions])))

    """
    Part 2
    """
    # Create global figure/ax
    FIG, AX = plt.subplots()
    _ = AX.imshow(np.zeros((10, 10)))
    plt.grid()
    plt.gca().invert_yaxis()

    number_of_knots_pairs = 5
    knot_object_list = [MovingGame(plot_output=False) for _ in range(number_of_knots_pairs)]

    for ii in range(number_of_knots_pairs-1):
        knot_object_list[ii].current_tail = knot_object_list[ii+1].current_head

    [x.current_head for x in knot_object_list]
    [x.current_tail for x in knot_object_list]

    head_plot_obj, tail_plot_obj = plot_status(knot_object_list)
    all_tail_positions = []
    for i_move in puzzle_input:
        direction_string, step_size = process_move_part_2(i_move)
        for i_step in range(step_size):

            print(direction_string, i_step)
            object_counter = 0
            make_a_move = True
            while make_a_move:
                [x.remove() for x in head_plot_obj]
                [x.remove() for x in tail_plot_obj]
                head_plot_obj, tail_plot_obj = plot_status(knot_object_list)
                print(make_a_move, object_counter)
                i_game_object = knot_object_list[object_counter]
                if object_counter == 0:
                    i_game_object.make_a_head_move(direction_string)
                else:
                    # knot_object_list[object_counter].current_tail = np.copy(knot_object_list[object_counter].current_head)
                    # knot_object_list[object_counter].current_head = np.copy(knot_object_list[object_counter-1].current_tail)
                    pass

                make_a_move = i_game_object.check_tail_move_part_2(direction_string)
                object_counter += 1
                if object_counter == number_of_knots_pairs:
                    make_a_move = False

            all_tail_positions.extend([np.copy(x.current_tail) for x in knot_object_list])

            # for ii, i_game_object in enumerate(knot_object_list[1:]):
            #     all_tail_positions.append(np.copy(i_game_object.current_tail))
                # plot_head(i_game_object)
                # plot_tail(i_game_object)

    # print(all_tail_positions)
    # plt.scatter(*np.array(all_tail_positions).T)
    print(len(list(set([tuple(x) for x in all_tail_positions]))))
