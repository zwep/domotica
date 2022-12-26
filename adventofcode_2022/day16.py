import os
import time
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


class ValveCollection:
    def __init__(self, valve_object_list):
        self.valve_object_list = valve_object_list

    def __len__(self):
        return len(self.valve_object_list)

    def get_valve(self, name):
        return [x for x in self.valve_object_list if x.name == name][0]

    def get_flow_rate_from_index(self, valve_index_list):
        return [self.valve_object_list[ii].flow_rate for ii in valve_index_list]

    def get_total_flow_rate(self, status_list=None):
        # In case there is no status list given...
        if status_list is None:
            status_list = [0] * len(self.valve_object_list)

        for ii, i_status in enumerate(status_list):
            if i_status is None:
                self.valve_object_list[ii].status = False
            else:
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
    def __init__(self, value_collection, distance_matrix):
        self.valve_collection = value_collection
        self.distance_matrix = distance_matrix
        self.flow_rate = [x.flow_rate for x in self.valve_collection]

        self.print_current_pressure = 0

        n_valves = len(self.valve_collection)
        list_of_valves = valve_collection_obj.valve_object_list
        self.name2index = dict(zip([x.name for x in list_of_valves], range(n_valves)))
        self.index2name = dict(zip(range(n_valves), [x.name for x in list_of_valves]))

        self.best_performance = {}

    @staticmethod
    def get_neighbours_debug(valve_object, **kwargs):
        return [(1, x) for x in valve_object.connections] + [(0, valve_object.name)]

    def get_neighbours(self, valve_object, valve_state, time_left, elephant_time):
        # Here we get the neighbours in a smart way...
        index_valve = self.name2index[valve_object.name]
        # current_flow_rate = valve_object.flow_rate
        distance_row = distance_matrix[index_valve]
        # possible_distances = list(set(distance_row))[::-1]
        # possible_distances.pop(possible_distances.index(0))  # Remove the zero node (itself)
        #
        inactive_valve = np.array(valve_state) == 0
        useful_valve = np.array(self.flow_rate) > 0
        # Select only the inactive and useful valves that we have available
        potential_neighbour_indices = np.argwhere(inactive_valve & useful_valve).ravel()
        #
        # n_neighbours = len(potential_neighbour_indices)
        potential_neighbour_distances = np.array(distance_row)[potential_neighbour_indices]
        potential_neighbour_flow_rate = np.array(self.flow_rate)[potential_neighbour_indices]
        # print(potential_neighbour_flow_rate / potential_neighbour_distances)
        relative_flow_rate = potential_neighbour_flow_rate / (1 + potential_neighbour_distances)
        max_index = np.argsort(relative_flow_rate)[-(self.total_time - time_left + 5):]
        potential_neighbour_indices = potential_neighbour_indices[max_index]
        # Now convert it to distance and their names....
        result = [(distance_row[i], self.index2name[i]) for i in potential_neighbour_indices]
        # Add the null case to activate the elephant
        if elephant_time is False:
            result = result + [(-1, None)]

        return result

    def print(self, name, state, depth, time, move_string):
        print('===== Processing')
        print(f'\t Name {name}')
        print(f'\t Pressure {self.print_current_pressure}')
        print(f'\t Time left {time}')
        print(f'\t Move string {move_string}')
        print('\t State')
        self.valve_collection.print(status_list=state, depth=depth)
        print('===== /Processing\n')

    def make_a_move(self, current_valve_name, time_left, valve_state=None, depth=0, move_string='',
                    elephant_time=False):

        if time_left < 0:
            if elephant_time is False:
                # Start the elephant time....
                valve_state = [None if x == 1 else x for x in valve_state]
                return self.make_a_move('AA', 26, valve_state=valve_state.copy(), elephant_time=True)
            else:
                return 0

        if valve_state is None:
            self.total_time = time_left
            valve_state = [0] * len(self.valve_collection)

        valve_object = self.valve_collection.get_valve(current_valve_name)
        move_string += current_valve_name + '->'

        # Check the available options
        current_pressure = self.valve_collection.get_total_flow_rate(valve_state)
        self.print_current_pressure = current_pressure

        neighbour_valves = self.get_neighbours(valve_object, valve_state, time_left=time_left, elephant_time=elephant_time)

        amount_of_pressure = []
        if len(neighbour_valves):
            for delta_t, x in neighbour_valves:
                if x is None:
                    # Trigger the elephant time?
                    # print(time_left)
                    temp_value = current_pressure * time_left + self.make_a_move('AA', valve_state=valve_state.copy(), time_left=-1, elephant_time=elephant_time)
                    amount_of_pressure.append(temp_value)
                else:
                    # In the next time step we are going to use set the new valve value
                    # Make sure to copy it....
                    new_state = valve_state.copy()
                    new_state[self.name2index[x]] = 1
                    # We need the minimum of time_left and 1, for the case when we have zero time left.
                    # Since in that case we dont want to add the current pressure value anymore.
                    current_pressure_correction = current_pressure * (min(time_left, delta_t)) + current_pressure * min(max(0, time_left-delta_t), 1)
                    # We moved AND turned on the valve
                    delta_t = delta_t + 1
                    temp_value = current_pressure_correction + \
                                 self.make_a_move(x, valve_state=new_state, time_left=int(time_left - delta_t),
                                                  depth=int(depth + delta_t), move_string=move_string, elephant_time=elephant_time)

                    amount_of_pressure.append(temp_value)
        else:
            """
            This case is for when we turn on our last valve.

            According to my last toy example... this should simply be
            the total time left times the most up-to-date pressure           

            """
            amount_of_pressure = [current_pressure * time_left]

        return max(amount_of_pressure)

# 2186 too low
# 2211 too high

dfile = os.path.join(DPATH, 'day16.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]

# Parse the input
list_of_valves = []
for puzzle_line in puzzle_input:
    source_valve = re.findall('Valve ([A-Z]{2})', puzzle_line)[0]
    flow_rate = int(re.findall('rate=([0-9]+)', puzzle_line)[0])
    connected_valve_list = re.findall('valve[s]*(.*)', puzzle_line)[0].split(', ')
    connected_valve_list = [x.strip() for x in connected_valve_list]
    valve_object = Valve(name=source_valve, flow_rate=flow_rate, connections=connected_valve_list)
    list_of_valves.append(valve_object)


# Collect all the valves in one list and put them in this object
valve_collection_obj = ValveCollection(list_of_valves)
initial_flow = valve_collection_obj.get_total_flow_rate()

# Calculate the shortest path from each node to another..
dijkstra_obj = Dijkstra(valve_collection_obj)
distance_matrix = dijkstra_obj.run_all_nodes()

result_dict = {}
for i_time in [26]:
    t0 = time.time()
    game_obj = Game(value_collection=valve_collection_obj, distance_matrix=distance_matrix)
    result = game_obj.make_a_move('AA', time_left=i_time)
    calc_time = time.time() - t0
    # print(result, calc_time)
    result_dict[i_time] = (calc_time, result)

# Print results
for k, v in result_dict.items():
   print(k, v[1], v[0])

#
# game_obj.best_performance
#
# plot_time_consumption = False
# if plot_time_consumption:
#     time_spend = []
#     for i in range(1, 30):
#         print('Time ', i)
#         t0 = time.time()
#         game_obj = Game(value_collection=valve_collection_obj, distance_matrix=distance_matrix)
#         game_obj.make_a_move('AA', time_left=i)
#         calc_time = time.time() - t0
#         print(calc_time)
#         time_spend.append(calc_time)
#
#     import matplotlib.pyplot as plt
#     plt.plot(time_spend)
#     plt.xlabel('Number of time steps')
#     plt.ylabel('Number of seconds to complete')

#
#
# import graphviz
# import networkx as nx
#
# G = nx.Graph()
# for i_valve in valve_collection_obj:
#     print(i_valve)
#     for i_connection in i_valve.connections:
#         # G.add_node(i_valve, attr={'flow': int(i_valve.flow_rate)})
#         G.add_edge(i_valve.name, i_connection, weight=1)
#
# plt.figure()
# nx.draw_networkx(G)
