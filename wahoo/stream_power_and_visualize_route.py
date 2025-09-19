import cv2
import asyncio
from bleak import BleakClient
import sys

import wahoo.config
from wahoo.config import simulation, window_name, POWER_UUID, BLE_DEVICE_ADDRESS, SLIDESHOW_IMG_PATHS, IMG_FOLDER
from wahoo.models import QuestionStatus
import wahoo.helper as whelper
import numpy as np

"""
What to do..
- Status is better... but question numbering and ordering can be improed
- Also check the last question

"""

icon = whelper.get_icon()
alp_image = whelper.get_alps()
route_points = whelper.get_alp_route()
num_points = len(route_points)

screen_height, screen_width = whelper.get_screen_width_height()

alp_img_height, alp_img_width = alp_image.shape[:2]
resized_alp_image = whelper.scale_image_to_window(alp_image, max_width=screen_width, max_height=screen_height)
new_height, new_width = resized_alp_image.shape[:2]

# Scale the route points based on the increase in image height/width
height_scale_factor = new_height / alp_img_height
width_scale_factor = new_width / alp_img_width
route_points = [(int(x * height_scale_factor), int(y * width_scale_factor)) for x, y in route_points]

canvas = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
canvas[:, :new_width] = resized_alp_image
height_canvas, width_canvas, _ = canvas.shape

# Positions of text, everything should be relative towards height/width of canvas
question_text_position = (height_canvas // 5, new_width)
difficulty_text_position = (int(height_canvas / 2.304), int(width_canvas / 3.23))
speedometer_position = (int(height_canvas / 1.728), int(width_canvas / 6.144))
speedometer_radius = int(height_canvas / 4.32)

"""
Definition of segments/questions
"""
num_questions = 21
# Let's just say he needs to cycle 5 km
meters_to_cycle = 5000
# Calculate how much arbitrary distance we have
route_distance_points = whelper.get_distance_route_points(route_points)

total_arbitrary_distance = sum(route_distance_points)
# Set a unit for this, given that we will cycle 5km
distance_per_unit = meters_to_cycle / total_arbitrary_distance

# Getting the indices of the points where we will stop
visiting_question = 0
distance_per_question = total_arbitrary_distance / num_questions
distance_traveled = 0
question_counter = 1
# Include the first one
question_frame_index = [0]
for i, distance in enumerate(route_distance_points):
    distance_traveled += distance
    if distance_traveled > question_counter * distance_per_question:
        question_counter += 1
        question_frame_index.append(i)

# Also include the last one
question_frame_index.append(num_points-1)
question_frame_index = sorted(question_frame_index)
question_status = {k: QuestionStatus.NEUTRAL for k in question_frame_index}


question_photo_mapping = {}
for question_nr, image_name_list in SLIDESHOW_IMG_PATHS.items():
    question_photo_mapping.setdefault(question_nr, [])
    for image_name in image_name_list:
        image = cv2.imread(IMG_FOLDER / f"{image_name}.jpg")
        # Also scale the image so that it fits....
        new_image = whelper.scale_image_to_window(image, max_width=screen_width - new_width, max_height=new_height)
        question_photo_mapping[question_nr].append(new_image)

current_image_index = 0
current_image = None

# Async notification handler
async def handle_ble_and_animation():
    def notification_handler(sender, data):
        global visiting_question, current_image_index, current_image

        # Create the window
        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        # Log status of stuff
        print(f"Frame index: {wahoo.config.frame_index}")
        print(f"pauseding: {wahoo.config.paused}")
        print(f"Difficulty factor: {wahoo.config.difficulty_factor}")
        print("-----")

        collected_data = whelper.handle_power_notification(None, data)
        wahoo.config.latest_power = collected_data['instantaneous_power']
        frame = canvas.copy()
        if current_image is not None:
            img_height, img_width, _ = current_image.shape
            frame[:img_height, new_width:new_width + img_width] = current_image

        # Draw question positions
        for i_question in question_frame_index:
            whelper.display_circle(frame, position=route_points[i_question], color=question_status[i_question].value)

        # Select the questions we have not answered yet
        # And check if we have passed any of these positions
        # If so, pauze the game
        question_selection = [k for k, v in question_status.items() if v == QuestionStatus.NEUTRAL]
        print(f"Neutral questions {question_selection}")
        for question_index in question_selection:
            if wahoo.config.frame_index >= question_index:
                question_status[question_index] = QuestionStatus.VISITING
                visiting_question = question_index
                wahoo.config.paused = True
                break

        # Draw icon
        point = route_points[wahoo.config.frame_index]
        direction = whelper.get_direction(route_points, wahoo.config.frame_index)
        whelper.overlay_icon(frame, icon=icon, position=point, direction=direction)

        # Draw power
        if simulation:
            whelper.draw_speedometer(frame, whelper.get_simulated_power(wahoo.config.time_index),
                                     center=speedometer_position, radius=speedometer_radius)
            wahoo.config.time_index += 1
        else:
            whelper.draw_speedometer(frame, wahoo.config.latest_power,
                                     center=speedometer_position, radius=speedometer_radius)

        # Draw the difficulty text
        str_difficulty_factor = int(wahoo.config.difficulty_factor * 100)
        difficulty_factor_text = f"Moeilijkheid: {str_difficulty_factor} %"
        whelper.display_text(frame, difficulty_factor_text, position=difficulty_text_position, fontscale=1)

        pressed_key = cv2.waitKey(30) & 0xFF  # Only call this ONCE

        if wahoo.config.paused:
            visiting_questions = [k for k, v in question_status.items() if v == QuestionStatus.VISITING]
            print(f'Visiting questions: {visiting_questions}')
            if pressed_key == ord('g'):
                print("Pressed G")
                if question_status[visiting_question] == QuestionStatus.CORRECT:
                    return

                # (g)oed, now stuff should get easier...
                wahoo.config.difficulty_factor -= 0.05
                question_status[visiting_question] = QuestionStatus.CORRECT
            elif pressed_key == ord('f'):
                print("Pressed F")
                if question_status[visiting_question] == QuestionStatus.INCORRECT:
                    return

                # (f)alse
                wahoo.config.difficulty_factor += 0.1
                question_status[visiting_question] = QuestionStatus.INCORRECT
            elif pressed_key == ord('n'):
                print("Pressed N")
                if question_status[visiting_question] == QuestionStatus.VISITING:
                    print("We are still visiting...")
                    return

                # Oh no... how to make this persistent...
                question_nr = question_frame_index.index(visiting_question)
                n_photos = len(question_photo_mapping[question_nr])
                if n_photos > 0:
                    current_image = question_photo_mapping[question_nr][current_image_index]
                    img_height, img_width, _ = current_image.shape
                    frame[:, new_width:] = np.zeros(frame[:, new_width:].shape)
                    frame[:img_height, new_width:new_width + img_width] = current_image
                    current_image_index += 1

                if current_image_index == n_photos:
                    # Reset everything...
                    # Next up: format images per question
                    current_image_index = 0
                    current_image = None
                    visiting_question = None
                    frame[:, new_width:] = np.zeros(frame[:, new_width:].shape)
                    wahoo.config.paused = False

            elif pressed_key == ord('q'):
                sys.exit()
            else:
                n_photos = 0
                question_nr = -1
                if visiting_question in question_frame_index:
                    question_nr = question_frame_index.index(visiting_question)
                    n_photos = len(question_photo_mapping[question_nr])

                if question_nr == 0:
                    question_name = "de oefen vraag"
                else:
                    question_name = f"vraag nummer {question_nr}"

                if question_status[visiting_question] == QuestionStatus.VISITING:
                    question_text = f"Antwoord voor {question_name}"
                elif visiting_question is None:
                    question_text = "FIETSEN FIETSEN FIETSEN!"
                elif current_image_index < n_photos:
                    question_text = ""
                else:
                    question_text = f"{question_name.capitalize()}"

                whelper.display_text(frame, question_text, position=question_text_position)

            cv2.imshow(window_name, frame)
            return
        else:
            cv2.imshow(window_name, frame)

        # Update new position
        if simulation:
            wahoo.config.frame_index = whelper.watt_to_new_index(whelper.get_simulated_power(wahoo.config.time_index),
                                                                 wahoo.config.frame_index, distance_points=route_distance_points,
                                                                 difficulty_factor=wahoo.config.difficulty_factor)
        else:
            wahoo.config.frame_index = whelper.watt_to_new_index(wahoo.config.latest_power, wahoo.config.frame_index,
                                                                 distance_points=route_distance_points,
                                                                 difficulty_factor=wahoo.config.difficulty_factor)

        # Wait 30 miliseconds for input
        if pressed_key == ord('q'):
            sys.exit()


    async with BleakClient(BLE_DEVICE_ADDRESS, timeout=20,use_cached=False) as client:
        if not client.is_connected:
            print("Failed to connect.")
            return
        print("Connected!")

        await client.start_notify(POWER_UUID, notification_handler)
        try:
            while wahoo.config.frame_index <= num_points:
                await asyncio.sleep(1)
        finally:
            await client.stop_notify(POWER_UUID)
            cv2.destroyAllWindows()

# Run the async BLE animation
asyncio.run(handle_ble_and_animation())

