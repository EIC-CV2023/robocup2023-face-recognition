from deepface import DeepFace
import cv2
import os

cap =  cv2.VideoCapture(0)

DEEPFACE_MODEL = "Facenet512"
DETECTOR_BACKEND = "ssd"


while True:
    ret, frame = cap.read()
    height = frame.shape[0]
    width = frame.shape[1]

    results = DeepFace.extract_faces(frame, detector_backend= DETECTOR_BACKEND, enforce_detection= False, align= True, target_size= frame.shape[:-1])
          
    for i, face in enumerate(results):
        coordinates = face["facial_area"]
        face_x, face_y, face_w, face_h = coordinates["x"], coordinates["y"], coordinates["w"], coordinates["h"]
        imagePath = "./captures/capture{}.jpg".format(i)
        face_crop = frame[face_y:face_y+face_h, face_x:face_x+face_w]

        if len(os.listdir("./people")) != 0: 
            result = DeepFace.find(img_path = face_crop, db_path = "./people", model_name=DEEPFACE_MODEL, enforce_detection = False, silent=True, align=True)

            if len(result[0]) > 0:
                recog_name = result[0]["identity"][0][9:-4]
                cv2.putText(frame, recog_name,  (coordinates["x"], coordinates["y"]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
                print("Recognized: " + recog_name)

        else:
            print("No file in database")            

        cv2.rectangle(frame, (face_x, face_y), (face_x+face_w, face_y+face_h),  (255,255,0), 3)

                
    
    cv2.imshow("frame", frame)
    cv2.imshow("framecrop", face_crop)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# video.release()
cv2.destroyAllWindows()