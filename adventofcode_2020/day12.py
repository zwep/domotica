import numpy as np


def get_rotated_x(x, theta):
    theta = np.radians(theta)
    rot_vect = np.array([[np.cos(theta), -np.sin(theta)],
                         [np.sin(theta), np.cos(theta)]]).astype(int)
    return np.matmul(rot_vect, np.array(x).reshape(-1, ))


def new_orientation(cur_line, orientation):
    direction = cur_line[0]
    angle = int(cur_line[1:])
    if direction == "L":
        orientation = get_rotated_x(orientation, angle).reshape(-1, )
    elif direction == "R":
        orientation = get_rotated_x(orientation, -angle).reshape(-1, )
    else:
        pass
    return orientation


def new_position(cur_line, position, orientation):
    direction = cur_line[0]
    size = int(cur_line[1:])
    if direction == "N":
        position[1] += size
    elif direction == "E":
        position[0] += size
    elif direction == "W":
        position[0] -= size
    elif direction == "S":
        position[1] -= size
    elif direction == "F":
        position += size * orientation
    else:
        pass
    return position

day = 12
with open(f"adventofcode_2020/day{str(day)}_numbers.txt", "r") as f:
    A = f.read().splitlines()


orientation = np.array([1, 0])
position = np.array([0, 0])
for i_line in A:
    position = new_position(i_line, position, orientation)
    orientation = new_orientation(i_line, orientation)
    print(position, '  ', orientation)


# Part 2
def move_ship(cur_line, position, position_waypoint):
    direction = cur_line[0]
    size = int(cur_line[1:])
    if direction == "F":
        relative_position = (position_waypoint - position)
        position += size * relative_position
        position_waypoint = position + relative_position
    else:
        pass

    return position, position_waypoint


def move_waypoint(cur_line, position_waypoint, position_ship):
    direction = cur_line[0]
    size = int(cur_line[1:])
    if direction == "N":
        position_waypoint[1] += size
    elif direction == "E":
        position_waypoint[0] += size
    elif direction == "W":
        position_waypoint[0] -= size
    elif direction == "S":
        position_waypoint[1] -= size
    elif direction == "R":
        relative_position = position_waypoint - position_ship
        position_waypoint = position_ship + get_rotated_x(relative_position, -size)
    elif direction == "L":
        relative_position = position_waypoint - position_ship
        position_waypoint = position_ship + get_rotated_x(relative_position, size)
    else:
        pass
    return position_waypoint

# [x, y]
position = np.array([0, 0])
position_waypoint = np.array([10, 1])

print('\n\n',position, '  ', position_waypoint)
for i_line in A:
    position_waypoint = move_waypoint(i_line, position_waypoint, position)
    position, position_waypoint = move_ship(i_line, position, position_waypoint)
    print(i_line, position, '  ', position_waypoint)
