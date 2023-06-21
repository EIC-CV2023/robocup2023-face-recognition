import socket
import json
import cv2
import time
from custom_socket import CustomSocket


## Register
print("Register")
cap = cv2.VideoCapture(0)
cap.set(4, 480)
cap.set(3, 640)

host = socket.gethostname()
port = 12304
c = CustomSocket(host, port)
c.clientConnect()

while cap.isOpened():

    ret, frame = cap.read()
    cv2.imshow("client_cam", frame)

    name = "Game"

    res = c.register(frame, name)
    print(res)
    break

    # continue
    key = cv2.waitKey(1)
    if key == ord('r'):
        task = "register"
    if key == ord('d'):
        task = "detect"
    if key == ord("q"):
        cap.release()

cv2.destroyAllWindows()

time.sleep(2)

print("Detect")
## Detect
cap = cv2.VideoCapture(0)
cap.set(4, 480)
cap.set(3, 640)

host = socket.gethostname()
port = 12304
c = CustomSocket(host, port)
c.clientConnect()

while cap.isOpened():

    ret, frame = cap.read()
    cv2.imshow("client_cam", frame)

    res = c.detect(frame)
    if res != {}:
        print(res)

    # continue
    key = cv2.waitKey(1)
    if key == ord('r'):
        task = "register"
    if key == ord('d'):
        task = "detect"
    if key == ord("q"):
        cap.release()

cv2.destroyAllWindows()

