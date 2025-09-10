import cv2
import numpy as np
import math
from wahoo.models import CyclingPowerFlags
from PIL import Image

ICON_PATH = r"F:\Documents\lenn\cycler_with_head.png"
ALP_IMG_PATH = r"F:\Documents\lenn\alpe_sat.jpg"
ALP_ROUTE_PATH = r"F:\Documents\lenn\route_alpe_sat.txt"

# BLE UUID for Cycling Power Measurement
# Overview of other UUIDs
# https://gist.github.com/sam016/4abe921b5a9ee27f67b3686910293026
POWER_UUID = "00002a63-0000-1000-8000-00805f9b34fb"
BLE_DEVICE_ADDRESS = "C6:76:C5:B6:3C:14"

# This shows how the data is encoded
# https://bitbucket.org/bluetooth-SIG/public/src/main/gss/
# This shows all the specifications
# https://btprodspecificationrefs.blob.core.windows.net/gatt-specification-supplement/GATT_Specification_Supplement.pdf

# This also helped me
# https://github.com/hbldh/bleak/discussions/1579

def get_icon():
    # TODO: CHeck how we want to resize.. and if we can maintain that the white background is nulled...
    # Only need to change this to a cooler function
    icon = cv2.imread(ICON_PATH, cv2.IMREAD_UNCHANGED)  # Load icon with alpha
    # icon = cv2.cvtColor(icon, cv2.COLOR_BGRA2RGBA)
    icon = cv2.resize(icon, (132, 132))  # Resize if needed
    # This almost does what I want... I guess
    return icon


def get_alps():
    image = cv2.imread(ALP_IMG_PATH)
    # clone = image.copy()
    return image

# import plotly.graph_objects as go
#
# fig = go.Figure(data=go.Image(z=A))
# fig.show()
#
#
# fig = go.Figure(data=go.Image(z=A[:,:,2:3]))
# fig.show()
#
# import plotly.express as px
# fig = px.imshow((A[:, :, 3:4] == A[:, :, 3:4].max()) * A[:, :, :])
# fig.show()
#
# # Show using plotly
# fig = px.imshow(A[:, :, :],
#                 color_continuous_scale='gray',
#                 binary_string=True,
#                 aspect='equal')
#
# fig.update_layout(coloraxis_showscale=False)  # hide color bar
# fig.show()


def get_alp_route():
    with open(ALP_ROUTE_PATH, 'r') as f:
        route_points = f.read()

    route_points = [x.split(':') for x in route_points.split('\n')]
    route_points = [(int(x[0]), int(x[1])) for x in route_points]
    return route_points

def overlay_icon(background, icon, position, direction):
    h_bg, w_bg, _ = background.shape
    x, y = position
    h, w = icon.shape[:2]
    x -= w // 2
    y -= h // 2
    if direction < 0:
        icon = icon[:, ::-1]

    # Yeah a bit stupid to do it like this...
    icon_mask = icon[:, :, 3] == icon[:, :, 3].max()

    for c in range(0, 3):
        background[y:y+h, x:x+w, c][icon_mask] = icon[:, :, c][icon_mask]
    return background

def get_direction(route_points, j, N=5):
    # Used to orient the icon in the 'riding' postion
    # j is the current index of the point
    # N is the number of average points we take (in the past)
    avg_x_pos = sum([x[0] for x in route_points[j - N:j]]) / N
    if route_points[j][0] - avg_x_pos <= 0:
        direction = -1
    else:
        direction = 1

    return direction


def handle_power_notification(sender, data):
    flags = int.from_bytes(data[0:2], byteorder='little')
    enabled_flags = CyclingPowerFlags(flags)

    # This does not need to be converted apparently
    instantaneous_power = int.from_bytes(data[2:4], byteorder='little', signed=True)
    index = 4

    if CyclingPowerFlags.PEDAL_POWER_BALANCE_PRESENT in enabled_flags:
        index += 1

    accumulated_torque = None
    """
    This still needs to be converted to real torque
    Base Unit:
    org.bluetooth.unit.moment_of_force.newton_metre
    Represented values: M = 1, d = 0, b = -5
    Unit is 1/32 Newton meter
    Present if bit 2 of Flags field is set to 1
    """
    if CyclingPowerFlags.ACCUMULATED_TORQUE_PRESENT in enabled_flags:
        accumulated_torque = int.from_bytes(data[index:index + 2], byteorder='little', signed=False)
        index += 2

    wheel_revs = None
    last_wheel_event_time = None
    """
    Still need to convert the last event time
    Base Unit: org.bluetooth.unit.time.second
    Represented values: M = 1, d = 0, b = -11
    Unit is 1/2048 second
    """
    if CyclingPowerFlags.WHEEL_REVOLUTION_DATA_PRESENT in enabled_flags:
        wheel_revs = int.from_bytes(data[index:index + 4], byteorder='little', signed=False)
        last_wheel_event_time = int.from_bytes(data[index + 4:index + 6], byteorder='little', signed=False)
        index += 6

    crank_revs = None
    last_crank_event_time = None

    """
    Convert event time
    Base Unit: org.bluetooth.unit.time.second
    Represented values: M = 1, d = 0, b = -10
    Unit is 1/1024 second
    """
    if CyclingPowerFlags.CRANK_REVOLUTION_DATA_PRESENT in enabled_flags:
        crank_revs = int.from_bytes(data[index:index + 2], byteorder='little', signed=False)
        last_crank_event_time = int.from_bytes(data[index + 2:index + 4], byteorder='little', signed=False)
        index += 4

    collected_data = {
        "instantaneous_power": instantaneous_power,
        "accumulated_torque": accumulated_torque,
        "wheel_revs": wheel_revs,
        "last_wheel_event_time": last_wheel_event_time,
        "crank_revs": crank_revs,
        "last_crank_event_time": last_crank_event_time
    }
    return collected_data


def draw_speedometer(frame, power, center=(550, 250), radius=200):
    """
    Draws a speedometer-style power gauge on the given frame.
    Power is expected to be in the range 0–100.
    """
    height, width, _ = frame.shape
    color_text = (255, 255, 255)
    color_outer_text = (0, 0, 0)
    color_center_knob = (0, 0, 0)
    color_outer_arc = (180, 180, 180)
    color_power_label = (255, 255, 255)
    color_needle = (0, 0, 255)

    # Draw outer arc (semi-circle from -120° to +120°)
    for angle in range(-120, 121, 2):
        rad = math.radians(angle)
        x1 = int(center[0] + radius * math.cos(rad))
        y1 = int(center[1] + radius * math.sin(rad))
        cv2.circle(frame, (x1, y1), 1, color_outer_arc, -1)

    # Draw tick marks every 10 units (i.e., every 24° for 100 range over 240°)
    for i in range(0, 101, 10):
        angle = -120 + (i * 2.4)
        rad = math.radians(angle)
        x1 = int(center[0] + (radius - 10) * math.cos(rad))
        y1 = int(center[1] + (radius - 10) * math.sin(rad))
        x2 = int(center[0] + radius * math.cos(rad))
        y2 = int(center[1] + radius * math.sin(rad))
        cv2.line(frame, (x1, y1), (x2, y2), color_text, 2)

        # Optional: Add labels
        # This way we can scale from 0...1000 Watts
        label = str(i * 10)
        lx = int(center[0] + (radius - 30) * math.cos(rad))
        ly = int(center[1] + (radius - 30) * math.sin(rad))
        # The order here is important, first draw the black background
        # Then add the white on top
        cv2.putText(frame, label, (lx - 10, ly + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_outer_text, 8, cv2.LINE_AA)
        cv2.putText(frame, label, (lx - 10, ly + 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_text, 2, cv2.LINE_AA)

    # Draw needle
    # 0.24 because we have 100 steps and we have 1000 Watts max
    angle = -120 + (power * .24)
    rad = math.radians(angle)
    needle_length = radius - 40
    x = int(center[0] + needle_length * math.cos(rad))
    y = int(center[1] + needle_length * math.sin(rad))
    cv2.line(frame, center, (x, y), color_needle, 4)

    # Draw center knob
    cv2.circle(frame, center, 8, color_center_knob, -1)

    # Draw power label
    cv2.putText(frame, f'{int(power)} Watt', (center[0] - 40, center[1] + 70),
                cv2.FONT_HERSHEY_DUPLEX, 1, color_outer_text, 8, cv2.LINE_AA)

    cv2.putText(frame, f'{int(power)} Watt', (center[0] - 40, center[1] + 70),
                cv2.FONT_HERSHEY_DUPLEX, 1, color_power_label, 2, cv2.LINE_AA)

    return frame


def get_distance_route_points(route_points):
    # The idea here was to use this to determine the next frame
    # when he would speed up
    num_points = len(route_points)
    dist_points = []
    for i in range(num_points-1):
        ix, iy = route_points[i+1]
        jx, jy = route_points[i]
        s = ((ix - jx) ** 2 + (iy - jy) ** 2) ** 0.5
        dist_points.append(s)

    return dist_points


def watt_to_mps(watt):
    # 200 watts equals 30 kmh (=8.3 m/s) is what I say here
    # The 3.6 is the conversion from kmh -> m/s
    # I think I should calculate in meters and seconds here...
    mps_reff = 30 / 3.6
    watt_reff = 200
    return watt * (mps_reff / watt_reff)


def watt_to_new_index(watt, current_index, distance_points):
    # We are doing everything per second basis..
    # So actually, this is just 'meters'
    mps = watt_to_mps(watt)
    # This gives the distance to GO TO this current index
    total_distance = 0
    for j, dist in enumerate(distance_points[current_index:]):
        total_distance += dist
        # If we have reached our target
        if total_distance >= mps:
            # I don't need to subtract one here, I think,
            # because we already start at 0
            return j + current_index

    return len(distance_points) + 1
