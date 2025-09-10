import cv2
import asyncio
from bleak import BleakClient
import sys
from wahoo.helper import BLE_DEVICE_ADDRESS, POWER_UUID, get_distance_route_points
import wahoo.helper as whelper
import math
import time

"""
Left to do:
- show a photo, or multiple after point X
- Blijvende tekst als we aan het wachten zijn?
"""

# Global state
wait = False
latest_power = 0
# Used for the route...
frame_index = 0
# Used for the simulated power
time_index = 0

icon = whelper.get_icon()
image = whelper.get_alps()
clone = image.copy()
route_points = whelper.get_alp_route()
num_points = len(route_points)

# I think we are going to tell 8 stories...
num_segments = 32
# Let's just say he needs to cycle 5 km
meters_to_cycle = 5000
# Calculate how much arbitrary distance we have
route_distance_points = get_distance_route_points(route_points)
total_arbitrary_distance = sum(route_distance_points)
# Set a unit for this, given that we will cycle 5km
distance_per_unit = meters_to_cycle / total_arbitrary_distance

# Simulate some power...
def get_simulated_power(time_point):
    return 400 * abs(math.sin(2 * 3.14 * time_point/100))


# Getting the indices of the points where we will stop
distance_per_segment = total_arbitrary_distance / num_segments
distance_traveled = 0
segment_counter = 1
segment_frame_index = []
for i, distance in enumerate(route_distance_points):
    distance_traveled += distance
    if distance_traveled > segment_counter * distance_per_segment:
        segment_counter += 1
        segment_frame_index.append(i)
# Also include the last one
segment_frame_index.append(total_arbitrary_distance)

segment_status = {k: False for k in segment_frame_index}

# Async notification handler
async def handle_ble_and_animation():
    global latest_power, frame_index, time_index, wait

    def notification_handler(sender, data):
        global frame_index, latest_power, time_index, wait

        collected_data = whelper.handle_power_notification(None, data)
        latest_power = collected_data['instantaneous_power']
        frame = clone.copy()

        # Draw route
        for isegment in segment_frame_index:
            cv2.circle(frame, route_points[isegment], 8,(0, 0, 0), -1)
            cv2.circle(frame, route_points[isegment], 6, (255, 255, 255), -1)
            # Mark as 'completed' when we have passed it
            if frame_index >= isegment:
                cv2.circle(frame, route_points[isegment], 6, (13, 158, 13), -1)

        # Because of the speed he can surpass it
        segment_selection = [k for k, v in segment_status.items() if v is False]
        for segment_index in segment_selection:
            if frame_index >= segment_index:
                segment_status[segment_index] = True
                frame_index += 1
                height, width, _ = frame.shape
                cv2.putText(frame, "Well done!",
                            (height//2, width//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 8, cv2.LINE_AA)
                cv2.putText(frame, "Well done!",
                            (height//2, width//2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)

                wait = True
                break

        # Draw icon
        point = route_points[frame_index]
        direction = whelper.get_direction(route_points, frame_index)
        whelper.overlay_icon(frame, icon=icon, position=point, direction=direction)

        # Draw power
        # whelper.draw_speedometer(frame, latest_power)
        # TODO change this... to not the simualted power
        whelper.draw_speedometer(frame, get_simulated_power(time_index))
        time_index += 1

        if wait:
            height, width, _ = frame.shape
            if cv2.waitKey(30) & 0xFF == ord('g'):
                cv2.putText(frame, "GOGOGO!",
                            (height // 2, width // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
                wait = False
            else:
                cv2.putText(frame, "Even wachten...",
                            (height // 2, width // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
                z = r'F:\Pictures\file.jpg'
                derp = cv2.imread(z)
                cv2.imshow("Lenn's power extravaganza", derp.copy())
                return

            cv2.imshow("Lenn's power extravaganza", frame)
            return
        else:
            cv2.imshow("Lenn's power extravaganza", frame)

        # Update new position
        frame_index = whelper.watt_to_new_index(get_simulated_power(time_index), frame_index, distance_points=route_distance_points)

        # Wait 30 miliseconds for input
        if cv2.waitKey(30) & 0xFF == ord('q'):
            sys.exit()


    async with BleakClient(BLE_DEVICE_ADDRESS, timeout=20,use_cached=False) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        print("Connected!")

        await client.start_notify(POWER_UUID, notification_handler)
        try:
            while frame_index <= num_points:
                await asyncio.sleep(1)
        finally:
            await client.stop_notify(POWER_UUID)
            cv2.destroyAllWindows()

# Run the async BLE animation
asyncio.run(handle_ble_and_animation())

