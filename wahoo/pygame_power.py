import pygame
import asyncio
from bleak import BleakClient
import sys
import math
import numpy as np
from wahoo.helper import BLE_DEVICE_ADDRESS, POWER_UUID, get_distance_route_points
import wahoo.helper as whelper


"""
This was cnverted using ChatGPT to see if we can use pygame instead of cv2
Nice idea, but somewhere there is trouble with asyncio and pygame..
So I think this is a problem that is too difficult for now

"""


if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Global state
wait = False
latest_power = 0
frame_index = 0
time_index = 0

# Load assets
icon = whelper.get_icon()
image = whelper.get_alps()          # Assuming NumPy image (H x W x 3)
route_points = whelper.get_alp_route()
route_distance_points = get_distance_route_points(route_points)

# Convert NumPy image to Pygame Surface
def numpy_to_surface(np_img):
    # Convert BGR (OpenCV format) to RGB for Pygame
    rgb = np_img[..., ::-1].copy()
    surface = pygame.surfarray.make_surface(np.transpose(rgb, (1, 0, 2)))  # Pygame expects (W, H)
    return surface

# Calculate route info
num_points = len(route_points)
num_segments = 32
meters_to_cycle = 5000
total_arbitrary_distance = sum(route_distance_points)
distance_per_unit = meters_to_cycle / total_arbitrary_distance
distance_per_segment = total_arbitrary_distance / num_segments

# Segment calculation
distance_traveled = 0
segment_counter = 1
segment_frame_index = []
for i, distance in enumerate(route_distance_points):
    distance_traveled += distance
    if distance_traveled > segment_counter * distance_per_segment:
        segment_counter += 1
        segment_frame_index.append(i)
segment_frame_index.append(num_points - 1)
segment_status = {k: False for k in segment_frame_index}


# Simulated power function
def get_simulated_power(t):
    return 400 * abs(math.sin(2 * 3.14 * t / 100))


# Pygame text rendering
pygame.font.init()
font = pygame.font.SysFont("Arial", 36)


# Async BLE + Pygame loop
async def handle_ble_and_animation():
    global latest_power, frame_index, time_index, wait

    # Init Pygame
    pygame.init()
    screen = pygame.display.set_mode((image.shape[1], image.shape[0]), pygame.FULLSCREEN)
    pygame.display.set_caption("Lenn's power extravaganza")
    clock = pygame.time.Clock()

    base_surface = numpy_to_surface(image)

    def draw_scene(power):
        global screen, base_surface, frame_index, wait

        # Clone base background
        frame = base_surface.copy()

        # Draw route points
        for isegment in segment_frame_index:
            pygame.draw.circle(frame, (0, 0, 0), route_points[isegment], 8)
            pygame.draw.circle(frame, (255, 255, 255), route_points[isegment], 6)
            if frame_index >= isegment:
                pygame.draw.circle(frame, (13, 158, 13), route_points[isegment], 6)

        # Check for segment progression
        segment_selection = [k for k, v in segment_status.items() if v is False]
        for segment_index in segment_selection:
            if frame_index >= segment_index:
                segment_status[segment_index] = True
                frame_index += 1
                msg = font.render("Well done!", True, (255, 255, 255))
                frame.blit(msg, (screen.get_width() // 2 - 100, screen.get_height() // 2))
                wait = True
                break

        # Draw icon (placeholder, since overlay_icon is OpenCV-based)
        point = route_points[frame_index]
        direction = whelper.get_direction(route_points, frame_index)
        # You would need to re-implement overlay_icon for Pygame
        # For now, assume `icon` is a Pygame surface and draw it rotated
        if isinstance(icon, pygame.Surface):
            rotated_icon = pygame.transform.rotate(icon, -direction)
            icon_rect = rotated_icon.get_rect(center=point)
            frame.blit(rotated_icon, icon_rect)

        # Draw power (placeholder for whelper.draw_speedometer)
        power_text = font.render(f"Power: {int(power)}W", True, (255, 255, 255))
        frame.blit(power_text, (50, 50))

        # Handle waiting logic
        if wait:
            msg = font.render("Even wachten... Press G to continue", True, (255, 255, 255))
            frame.blit(msg, (screen.get_width() // 2 - 200, screen.get_height() // 2 + 50))

        # Draw to screen
        screen.blit(frame, (0, 0))
        pygame.display.flip()

    # BLE handler
    def notification_handler(sender, data):
        global frame_index, time_index, wait, latest_power

        collected_data = whelper.handle_power_notification(None, data)
        latest_power = collected_data['instantaneous_power']
        power = get_simulated_power(time_index)
        draw_scene(power)

        if not wait:
            frame_index = whelper.watt_to_new_index(power, frame_index, distance_points=route_distance_points)
        time_index += 1

    # BLE connection
    async with BleakClient(BLE_DEVICE_ADDRESS, timeout=20, use_cached=False) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        print("Connected!")

        await client.start_notify(POWER_UUID, notification_handler)

        try:
            running = True
            while running and frame_index < num_points:
                await asyncio.sleep(0.03)  # ~30 FPS

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            running = False
                            break
                        elif wait and event.key == pygame.K_g:
                            wait = False

                clock.tick(30)  # Cap at 30 FPS
        finally:
            await client.stop_notify(POWER_UUID)
            pygame.quit()


# Start the game
asyncio.run(handle_ble_and_animation())
