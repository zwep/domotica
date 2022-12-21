import os
import time
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


class Dijkstra:
    def __init__(self, valve_object_list):
        self.valve_collection_obj = valve_object_list
        self.valve_name_list = [x.name for x in valve_collection_obj.valve_object_list]
        self.n_valves = len(self.valve_name_list)

    def initialization(self, starting_valve):
        # Initialize distances.
        visited_nodes = [False] * self.n_valves
        index_selected_valve = self.valve_name_list.index(starting_valve)
        distance_list = [np.inf for _ in range(self.n_valves)]
        distance_list[index_selected_valve] = 0
        visited_nodes[index_selected_valve] = True
        return visited_nodes, distance_list

    def run(self, starting_valve):
        visited_nodes, distance_list = self.initialization(starting_valve)
        # Update weights...
        selected_valve = starting_valve
        while not all(visited_nodes):
            neighbour_list = valve_collection_obj.get_valve(selected_valve).connections
            for neighbour_name in neighbour_list:
                neighbour_index = self.valve_name_list.index(neighbour_name)
                current_index = self.valve_name_list.index(selected_valve)
                distance_list[neighbour_index] = min(1 + distance_list[current_index], distance_list[neighbour_index])

            # This is so cumbersome.... But it works..
            combined_visited_distance = list(zip(visited_nodes, distance_list))
            next_node_index = \
            min([(i, y) for i, (x, y) in enumerate(combined_visited_distance) if x is False], key=lambda x: x[1])[0]
            selected_valve = self.valve_name_list[next_node_index]
            visited_nodes[next_node_index] = True
        return distance_list

    def run_all_nodes(self):
        distance_matrix = []
        for i_valve in self.valve_name_list:
            distance_list = self.run(i_valve)
            distance_matrix.append(distance_list)

        return distance_matrix


class Game:
    def __init__(self, value_collection, total_time, distance_matrix):
        self.valve_collection = value_collection
        self.total_time = total_time
        self.distance_matrix = distance_matrix
        self.flow_rate = [x.flow_rate for x in self.valve_collection]

        n_valves = len(self.valve_collection)
        list_of_valves = valve_collection_obj.valve_object_list
        self.name2index = dict(zip([x.name for x in list_of_valves], range(n_valves)))
        self.index2name = dict(zip(range(n_valves), [x.name for x in list_of_valves]))

        self.print_current_pressure = 0
        self.best_performance = dict(zip(range(0, total_time+1), [0] * (total_time+1)))

    def get_neighbours_debug(self, valve_object, valve_state):
        return [(1, x) for x in valve_object.connections + [valve_object.name]]

    def get_neighbours(self, valve_object, valve_state):
        index_valve = self.name2index[valve_object.name]
        current_flow_rate = valve_object.flow_rate
        distance_row = distance_matrix[index_valve]
        possible_distances = list(set(distance_row))[::-1]
        possible_distances.pop(possible_distances.index(0))  # Remove the zero node (itself)
        #
        inactive_valve = np.array(valve_state) == 0
        useful_valve = np.array(self.flow_rate) > 0
        potential_neighbour_indices = []
        while len(potential_neighbour_indices) == 0:
             least_distance = possible_distances.pop()
             closeby_valve = np.array(distance_row) == least_distance
             potential_neighbour_indices = np.argwhere(inactive_valve & useful_valve & closeby_valve).ravel()
        # potential_neighbour_indices = np.argwhere(inactive_valve & useful_valve).ravel()
        potential_neighbour_indices = np.argwhere(inactive_valve).ravel()
        n_neighbours = len(potential_neighbour_indices)
        potential_neighbour_distances = np.array(distance_row)[potential_neighbour_indices]
        potential_neighbour_flow_rate = np.array(self.flow_rate)[potential_neighbour_indices]

        potential_neighbour_indices = list(potential_neighbour_indices)
        if valve_state[index_valve] == 0:
            # potential_neighbour_indices.append(index_valve)
            if any([(2 + potential_neighbour_distances[i]) * current_flow_rate > potential_neighbour_flow_rate[i] for i in range(n_neighbours)]):
                # Add it as an option to active itself only if the above holds..
                potential_neighbour_indices.append(index_valve)

        # Now convert it to distance and their names....
        return [(distance_row[i], self.index2name[i]) for i in potential_neighbour_indices][::-1]

    def check_possible_gain(self, valve_state):
        # Get current pressure gain
        current_pressure = self.valve_collection.get_total_flow_rate(valve_state)

    def print(self, name, state, depth, time, move_string):
        print('===== Processing')
        print(f'\t Name {name}')
        print(f'\t Pressure {self.print_current_pressure}')
        print(f'\t Time left {time}')
        print(f'\t Move string {move_string}')
        print('\t State')
        self.valve_collection.print(status_list=state, depth=depth)
        print('===== /Processing\n')

    def make_a_move(self, current_valve_name, valve_state=None, time_left=9999, depth=0,
                    move_string='', update_state=False):
        # Check if we can still make it...
        if time_left < 0:
            # print('Moved ', move_string)
            # print('-> Exit <-')
            return 0

        if time_left == 9999:
            time_left = self.total_time

        if valve_state is None:
            valve_state = [0] * len(self.valve_collection)
            # The first valve is always on..
            valve_state[0] = 1

        valve_object = self.valve_collection.get_valve(current_valve_name)
        move_string += current_valve_name + '->'

        # Check the available options
        current_pressure = self.valve_collection.get_total_flow_rate(valve_state)
        self.print_current_pressure = current_pressure
        if update_state:
            valve_state[self.name2index[current_valve_name]] = 1

        neighbour_valves = self.get_neighbours(valve_object, valve_state)
        # neighbour_valves = self.get_neighbours_debug(valve_object, valve_state)
        # print('\t' * depth, time_left, self.print_current_pressure, move_string)
        # print('\t' * depth, neighbour_valves)

        # Print the state before we start moving...
        # self.print(name=current_valve_name, state=valve_state, depth=depth, time=time_left, move_string=move_string)
        # Now we can move...
        # Or we can turn on a valve...
        # How to do this..
        amount_of_pressure = []
        for delta_t, x in neighbour_valves:
            if x == current_valve_name:
                index_current_valve = self.name2index[current_valve_name]
                if valve_state[index_current_valve] == 1:
                    continue
                else:
                    # In the next time step we are going to use set the new valve value
                    temp_value = current_pressure + self.make_a_move(x, valve_state=valve_state.copy(), time_left=time_left-1, depth=int(depth+1),
                                                                         move_string=move_string, update_state=True)
            else:
                current_pressure_correction = current_pressure * max(1, min(time_left, delta_t))
                temp_value = current_pressure_correction + \
                             self.make_a_move(x, valve_state=valve_state.copy(), time_left=int(time_left-delta_t),
                                              depth=int(depth+delta_t), move_string=move_string)
            amount_of_pressure.append(temp_value)

        best_performance_value = max(self.best_performance[self.total_time-time_left], max(amount_of_pressure))
        self.best_performance[time_left] = best_performance_value

        return max(amount_of_pressure)


class ValveCollection:
    def __init__(self, valve_object_list):
        self.valve_object_list = valve_object_list

    def __len__(self):
        return len(self.valve_object_list)

    def get_valve(self, name):
        return [x for x in self.valve_object_list if x.name == name][0]

    def get_total_flow_rate(self, status_list=None):
        # In case there is no status list given...
        if status_list is None:
            status_list = [0] * len(self.valve_object_list)

        for ii, i_status in enumerate(status_list):
            self.valve_object_list[ii].status = bool(i_status)

        return sum([x.flow_rate for x in self.valve_object_list if x.status])

    def print(self, status_list=None, depth=0):
        if status_list is not None:
            for ii, i_status in enumerate(status_list):
                self.valve_object_list[ii].status = bool(i_status)

        for i_valve in self.valve_object_list:
            print('\t'*depth, i_valve.name, i_valve.flow_rate, 'ON' if i_valve.status else 'OFF')

    def __getitem__(self, item):
        return self.valve_object_list[item]


class Valve:
    def __init__(self, name, flow_rate, connections):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections
        self.status = False


dfile = os.path.join(DPATH, 'day16_test.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]

list_of_valves = []
for puzzle_line in puzzle_input:
    source_valve = re.findall('Valve ([A-Z]{2})', puzzle_line)[0]
    flow_rate = int(re.findall('rate=([0-9]+)', puzzle_line)[0])
    connected_valve_list = re.findall('valve[s]*(.*)', puzzle_line)[0].split(', ')
    connected_valve_list = [x.strip() for x in connected_valve_list]
    valve_object = Valve(name=source_valve, flow_rate=flow_rate, connections=connected_valve_list)
    list_of_valves.append(valve_object)


valve_collection_obj = ValveCollection(list_of_valves)
initial_flow = valve_collection_obj.get_total_flow_rate()
# valve_collection_obj.print()

dijkstra_obj = Dijkstra(valve_collection_obj)
distance_matrix = dijkstra_obj.run_all_nodes()


result_dict = {}
for i_time in [10]:
    t0 = time.time()
    game_obj = Game(value_collection=valve_collection_obj, total_time=i_time, distance_matrix=distance_matrix)
    result = game_obj.make_a_move('AA')
    calc_time = time.time() - t0
    # print(result, calc_time)
    result_dict[i_time] = (calc_time, result)

game_obj.best_performance

for k, v in result_dict.items():
    print(k, v[1], v[0])

# t=3 : 20
# t=4 : 40
# t=5 : 60
# t=6 : 20*3+33*1 = 93
# t=7 : 126
# t=8 : 159
# t=9 : 20*3+33*4 = 192
# t=10 : 20*3+33*4+54 = 246

# time_spend = []
# for i in range(1, 15):
#     print('Time ', i)
#     t0 = time.time()
#     game_obj = Game(value_collection=valve_collection_obj, total_time=i, distance_matrix=distance_matrix)
#     game_obj.make_a_move('AA')
#     calc_time = time.time() - t0
#     print(calc_time)
#     time_spend.append(calc_time)
#
# import matplotlib.pyplot as plt
# plt.plot(time_spend)
# plt.xlabel('Number of time steps')
# plt.ylabel('Number of seconds to complete')
#
# game_obj.best_performance
#
