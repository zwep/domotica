import os
import shapely.geometry
import re
import string
import numpy as np
from adventofcode_2022.helper import DPATH
import matplotlib.pyplot as plt


def get_manhattan_distance(x, y):
    return np.abs(x - y).sum()


def get_sensor_coords(i_line):
    sensor_x, sensor_y = map(int, re.findall('Sensor at x=(-[0-9]+|[0-9]+), y=(-[0-9]+|[0-9]+)', i_line)[0])
    beacon_x, beacon_y = map(int, re.findall('beacon is at x=(-[0-9]+|[0-9]+), y=(-[0-9]+|[0-9]+)', i_line)[0])
    sensor_coord = np.array([sensor_x, sensor_y])
    beacon_coord = np.array([beacon_x, beacon_y])
    distance = get_manhattan_distance(sensor_coord, beacon_coord)
    return sensor_coord, beacon_coord, distance


class BeaconStuff:
    def __init__(self, puzzle_input, target_line, max_interval=20, loud=False):
        self.loud = loud
        self.max_interval = max_interval
        self.puzzle_input = puzzle_input
        self.target_line = target_line
        self.could_have_left_you = 0
        self.chilling_beacons = []
        self.interval_collection = []
        self.sensor_coord_list = []
        self.sensor_distance_list = []

    def process_puzzle(self):
        for i_line in puzzle_input:
            sensor_coord, beacon_coord, distance_beacon = get_sensor_coords(i_line)
            interval_coverage = self.inspect_the_sensor(sensor_coord, distance_beacon)
            if interval_coverage is not None:
                self.interval_collection.append(interval_coverage)
            if beacon_coord[1] == self.target_line:
                if self.loud:
                    print('A beacon is chilling on the target line', beacon_coord)
                self.chilling_beacons.append(beacon_coord)

            # Store these results for part 2..
            self.sensor_coord_list.append(sensor_coord)
            self.sensor_distance_list.append(distance_beacon)

    def inspect_the_sensor(self, sensor_coord, distance):
        above_sensor = sensor_coord + np.array([0, distance])
        below_sensor = sensor_coord - np.array([0, distance])
        if (self.target_line <= above_sensor[1]) and (self.target_line >= below_sensor[1]):
            interval_coverage = self.effect_of_sensor(sensor_coord, distance)
        else:
            interval_coverage = None
            self.could_have_left_you += 1
        return interval_coverage

    def effect_of_sensor(self, sensor_coord, distance):
        # Not sure why I wanted the signed distance...
        signed_distance = sensor_coord[1] - self.target_line
        remaining_distance = distance - np.abs(signed_distance)
        # Correction for the center case
        # No correction needed...?
        # remaining_distance = remaining_distance
        # The remaining distance can be covered both in +x and -x direction
        if remaining_distance > 0:
            # Return the interval
            return sensor_coord[0] - remaining_distance, sensor_coord[0] + remaining_distance
        else:
            return None

    def calculate_intervals(self, interval_collection=None):
        if interval_collection is None:
            sorted_intervals = sorted(self.interval_collection, key=lambda x: x[0])
            if len(self.interval_collection) == 0:
                return None
        else:
            sorted_intervals = interval_collection
        total_length = 0
        starting_point = sorted_intervals[0][0]
        for a, b in sorted_intervals:
            if starting_point in range(a, b + 1):
                # This includes the start/end_point
                length_inteval = b - starting_point + 1
                starting_point = b + 1
                total_length += length_inteval

        return total_length

    def filter_interval(self):
        if len(self.interval_collection):
            sorted_intervals = sorted(self.interval_collection, key=lambda x: x[0])
            filtered_intervals = []
            for i_interval in sorted_intervals:
                if all(np.array(i_interval) <= 0):
                    continue
                if all(np.array(i_interval) >= self.max_interval):
                    continue
                # Correct for the interval..
                i_interval = (max(i_interval[0], 0), min(i_interval[1], self.max_interval))
                filtered_intervals.append(i_interval)
            return filtered_intervals
        else:
            return None


dfile = os.path.join(DPATH, 'day15.txt')
with open(dfile, 'r') as f:
    puzzle_input = [x.strip() for x in f.readlines()]

puzzle_input = [x for x in puzzle_input if x]

"""
Part 1
"""

beacon_obj = BeaconStuff(puzzle_input, target_line=10)
beacon_obj.process_puzzle()

correction_beacons = len(set([tuple(x) for x in beacon_obj.chilling_beacons]))
coverage = beacon_obj.calculate_intervals()
print(coverage - correction_beacons)


"""
Part 2
"""


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.slope, self.intercept = self.get_slope_and_intercept()

    def get_slope_and_intercept(self):
        # Given two points, calculate the slope and intercept to form a line y = ax+b
        x1, y1 = self.p1
        x2, y2 = self.p2
        slope_coefficient = (y2 - y1) / (x2 - x1)
        slope_intercept = slope_coefficient * x1 - y1
        return slope_coefficient, slope_intercept

    def get_intersection_with_line(self, line_obj):
        # Given two lines y = ax + b and y = cx + d
        # We can get the x and y intersection points with these formula
        a = self.slope
        b = self.intercept
        c = line_obj.slope
        d = line_obj.intercept
        y_intersection = ((a * d) - (c * b)) / (a - c)
        x_intersection = (y_intersection - b) / a
        return x_intersection, y_intersection

    def validate_intersection(self, line_obj):
        x_intersection, y_intersection = self.get_intersection_with_line(line_obj)
        # Is this interection valid..?
        check_x_coord = self.p1[0] <= x_intersection <= self.p2[0]
        check_y_coord = self.p1[1] <= x_intersection <= self.p2[1]
        return check_x_coord, check_y_coord

    def plot(self):
        fig = plt.gca()
        fig.plot([self.p1[0], self.p2[0]], [self.p1[1], self.p2[1]], color='k')


def get_line_obj_from_coords(selected_coord, selected_distance):
    top_point = selected_coord + np.array([0, selected_distance])
    bottom_point = selected_coord + np.array([0, -selected_distance])
    left_point = selected_coord + np.array([-selected_distance, 0])
    right_point = selected_coord + np.array([selected_distance, 0])

    line_point_1 = Line(top_point, left_point)
    line_point_2 = Line(top_point, right_point)
    line_point_3 = Line(bottom_point, left_point)
    line_point_4 = Line(bottom_point, right_point)
    return line_point_1, line_point_2, line_point_3, line_point_4




fig, ax = plt.subplots()

# Okay lets get the line intersections...
beacon_obj = BeaconStuff(puzzle_input, max_interval=1, target_line=1)
beacon_obj.process_puzzle()
n_sensors = len(beacon_obj.sensor_coord_list)
polygon_list = []
for i_sensor in range(n_sensors):
    selected_coord = beacon_obj.sensor_coord_list[i_sensor]
    selected_distance = beacon_obj.sensor_distance_list[i_sensor]
    line_object_list = get_line_obj_from_coords(selected_coord, selected_distance)

    point_list = np.array([line_object_list[0].p1, line_object_list[0].p2, line_object_list[2].p1, line_object_list[1].p2])
    point_list = point_list
    polygon1 = shapely.geometry.Polygon(point_list)
    polygon_list.append(polygon1)


remaining_polygon = shapely.geometry.Polygon([(0, 0), (0, 4000000), (4000000, 4000000), (4000000, 0)])

for x in polygon_list:
    remaining_polygon = remaining_polygon.difference(x)

dir(remaining_polygon)
(minx, miny, maxx, maxy) = remaining_polygon.bounds
#
(maxx - 1) * 4000000 + (maxy - 1)
