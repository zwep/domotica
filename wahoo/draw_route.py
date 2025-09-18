import cv2
from wahoo.helper import get_alps
from wahoo.config import ALP_ROUTE_PATH

# Load your image
image = get_alps()
clone = image.copy()

# Store the route points
route_points = []

# Mouse callback function
def draw_path(event, x, y, flags, param):
    global route_points, image

    if event == cv2.EVENT_LBUTTONDOWN or event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        route_points.append((x, y))
        cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

# Create window and set callback
cv2.namedWindow("Draw Route")
cv2.setMouseCallback("Draw Route", draw_path)

print("[INFO] Draw the route with the mouse. Press 'q' when done.")
while True:
    cv2.imshow("Draw Route", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):  # Quit drawing
        break

cv2.destroyAllWindows()

with open(ALP_ROUTE_PATH, 'w') as f:
    f.write('\n'.join([':'.join([str(y) for y in x]) for x in route_points]))
