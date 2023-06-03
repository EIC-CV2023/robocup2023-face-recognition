from deepface import DeepFace
import cv2
import os

cap =  cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    height = frame.shape[0]
    width = frame.shape[1]
    results = DeepFace.extract_faces(frame, detector_backend= "ssd", enforce_detection= False, align= True, target_size= frame.shape[:-1])

    if cv2.waitKey(1) == ord('r'):
        registered_name = input('name: ')  
        cv2.imwrite("./people/{}.jpg".format(registered_name), frame)
        try:
            os.remove("./people/representations_arcface.pkl")
        except:
            print("No files found")

           

    for i, face in enumerate(results):
        coordinates = face["facial_area"]
        face_x, face_y, face_w, face_h = coordinates["x"], coordinates["y"], coordinates["w"], coordinates["h"]
        imagePath = "./captures/capture{}.jpg".format(i)
        # faceCut = frame[coordinates["y"]:coordinates["y"]+coordinates['h'], coordinates["x"]: coordinates["x"] + coordinates['w']]
        face_crop = frame[face_y:face_y+face_h, face_x:face_x+face_w]

        cv2.rectangle(frame, (face_x, face_y), (face_x+face_w, face_y+face_h),  (255,255,0), 3)

                
    
    cv2.imshow("frame", frame)
    cv2.imshow("framecrop", face_crop)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# video.release()
cv2.destroyAllWindows()
