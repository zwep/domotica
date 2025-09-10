import cv2
import wahoo.helper as whelper

icon = whelper.get_icon()
route_points = whelper.get_alp_route()
image = whelper.get_alps()

for j, point in enumerate(route_points):
    frame = image.copy()
    for i in range(len(route_points) - 1):
        cv2.line(frame, route_points[i], route_points[i+1], (0, 255, 0), 2)

    direction = whelper.get_direction(route_points, j)

    frame = whelper.overlay_icon(frame, icon, point, direction=direction)
    cv2.imshow("Route Animation", frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):  # ~30 FPS
        break

cv2.destroyAllWindows()
