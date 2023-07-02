from deepface import DeepFace
import cv2
import os
from custom_socket import CustomSocket
import socket
import json
import numpy as np
import traceback

DEEPFACE_MODEL = "Facenet512"
REPRESENTATION = "representations_facenet512.pkl"
DETECTOR_BACKEND = "ssd"

'''
Command Parameter
{"task": ["REGISTER", "DETECT"],
 "name": name,
 "only_face": bool,
 "clear_db": bool}
'''


def main():
    HOST = socket.gethostname()
    PORT = 12304

    server = CustomSocket(HOST, PORT)
    server.startServer()

    while True:
        conn, addr = server.sock.accept()
        print("Client connected from", addr)

        while True:
            res = dict()
            msg = {"res": res}
            try:
                data = server.recvMsg(
                    conn, has_splitter=True, has_command=True)
                frame_height, frame_width, frame, command = data

                msg["camera_info"] = [frame_width, frame_height]

                # register
                if command["task"] == 'REGISTER':
                    if command["clear_db"]:
                        print("Clearing Database")
                        for db_file in os.listdir("./people"):
                            os.remove(f"./people/{db_file}")

                    registered_name = command["name"]
                    register_frame = ""
                    if command["only_face"]:
                        register_frame = frame
                    else:
                        results = DeepFace.extract_faces(
                            frame, detector_backend=DETECTOR_BACKEND, enforce_detection=False, align=True, target_size=frame.shape[:-1])

                        if results:
                            print(
                                f"Found {len(results)} person, registering the first one")
                            face = results[0]
                            coordinates = face["facial_area"]
                            face_x, face_y, face_w, face_h = coordinates[
                                "x"], coordinates["y"], coordinates["w"], coordinates["h"]
                            # imagePath = "./captures/capture{}.jpg".format(i)
                            face_crop = frame[face_y:face_y +
                                              face_h, face_x:face_x+face_w]
                            register_frame = face_crop

                    if register_frame != "":
                        cv2.imwrite(
                            "./people/{}.jpg".format(registered_name), register_frame)
                        res["feedback"] = f"{registered_name} registered"
                        try:
                            os.remove(f"./people/{REPRESENTATION}")
                        except:
                            print("No representation file found")
                    else:
                        print("No face to register")
                        res["feedback"] = f"No face to register"

                # detect
                if len(os.listdir("./people")) == 0:
                    print("Database empty")
                else:
                    if command["task"] == 'DETECT':
                        if command["only_face"]:
                            result = DeepFace.find(
                                img_path=frame, db_path="./people", model_name=DEEPFACE_MODEL, enforce_detection=False, silent=True, align=True)
                            if len(result[0]) > 0:
                                recog_name = result[0]["identity"][0][9:-4]
                                print("Recognized: " + recog_name)
                                res["name"] = recog_name
                        else:
                            results = DeepFace.extract_faces(
                                frame, detector_backend=DETECTOR_BACKEND, enforce_detection=False, align=True, target_size=frame.shape[:-1])

                            for i, face in enumerate(results):
                                coordinates = face["facial_area"]
                                face_x, face_y, face_w, face_h = coordinates[
                                    "x"], coordinates["y"], coordinates["w"], coordinates["h"]
                                # imagePath = "./captures/capture{}.jpg".format(i)
                                face_crop = frame[face_y:face_y +
                                                  face_h, face_x:face_x+face_w]

                                result = DeepFace.find(
                                    img_path=face_crop, db_path="./people", model_name=DEEPFACE_MODEL, enforce_detection=False, silent=True, align=True)

                                if len(result[0]) > 0:
                                    recog_name = result[0]["identity"][0][9:-4]
                                    # cv2.putText(frame, recog_name,  (
                                    #     coordinates["x"], coordinates["y"]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
                                    print("Recognized: " + recog_name)
                                    res["name"] = recog_name

                                cv2.rectangle(
                                    frame, (face_x, face_y), (face_x+face_w, face_y+face_h),  (255, 255, 0), 3)

                # cv2.imshow("frame", frame)
                # cv2.waitKey(1)
                server.sendMsg(conn, json.dumps(msg))

            except Exception as e:
                traceback.print_exc()
                print(e)
                print("Connection Closed")
                break


if __name__ == '__main__':
    main()
