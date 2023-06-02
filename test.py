from deepface import DeepFace
import cv2
import os

video =  cv2.VideoCapture(0)
try:
    os.remove("./people/representations_arcface.pkl")
except:
    print("No files found")


while True:
    ret, frame = video.read()
    
    # cv2.imwrite("./captures/capture.jpg", frame)
    height = frame.shape[0]
    width = frame.shape[1]
    results = DeepFace.extract_faces(frame, detector_backend= "ssd", enforce_detection= False, align= True, target_size= frame.shape[:-1])

    if cv2.waitKey(1) & 0xFF == ord('r'):
        newName = input('name: ')  
        cv2.imwrite("./people/{}.jpg".format(newName), frame)
        try:
            os.remove("./people/representations_arcface.pkl")
        except:
            print("No files found")

           

    for i, face in enumerate(results):
        coordinates = face["facial_area"]
        imagePath = "./captures/capture{}.jpg".format(i)
        # faceCut = frame[coordinates["y"]:coordinates["y"]+coordinates['h'], coordinates["x"]: coordinates["x"] + coordinates['w']]
        faceCut = frame.copy()
        faceCut[coordinates["y"]+coordinates["h"]: height, 0:width] = 0
        faceCut[0: coordinates["y"], 0:width] = 0
        faceCut[coordinates["y"]:coordinates["y"]+coordinates['h'], 0:coordinates["x"]] = 0
        faceCut[coordinates["y"]:coordinates["y"]+coordinates['h'], coordinates["x"]+ coordinates["w"]:width] = 0
        # cv2.imwrite(imagePath, faceCut) 
        # cv2.imshow("frame{}".format(i), cv2.imread(imagePath))
        # print(cv2.imread(imagePath))


        if len(os.listdir("./people")) != 0: 
            result = DeepFace.find(img_path = faceCut, db_path = "./people", model_name="Facenet512", enforce_detection = False, silent=True, align=True)
        
        # print(result[0])
            if len(result[0]) > 0:
                # print(result[0]["identity"]) 
                # cv2.rectangle(frame,(result[0]["source_x"][0], result[0]["source_y"][0]) ,(result[0]["source_x"][0] + result[0]["source_w"][0], result[0]["source_y"][0] + result[0]["source_h"][0]), (255,255,0), 3)    
                # cv2.rectangle(frame, (coordinates["x"], coordinates["y"]), (coordinates["x"] + coordinates['w'], coordinates["y"]+coordinates['h']),  (255,255,0), 3)
                cv2.putText(frame, result[0]["identity"][0][9:-4],  (coordinates["x"], coordinates["y"]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1)
                print("Recognized: " + result[0]["identity"][0][9:-4])
        # else:
        #     if newPerson:
                
        cv2.rectangle(frame, (coordinates["x"], coordinates["y"]), (coordinates["x"] + coordinates['w'], coordinates["y"]+coordinates['h']),  (255,255,0), 3)

                
    
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

        


# from deepface import DeepFace
# import cv2

# face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_alt.xml')
# video = cv2.VideoCapture(0)

# while True:
#     ret, frame = video.read()
#     faces = face_cascade.detectMultiScale(frame, 1.1, 4)

#     # Convert the frame from BGR to RGB color space
#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     cv2.imwrite("test.jpg", frame_rgb)
#     results = DeepFace.extract_faces("test.jpg", detector_backend="ssd", enforce_detection=False, align= False)
#     i = 1

#     for face in results:
#         face_path = "./captures/capture{}.jpg".format(i)

#         # Convert the face image from BGR to RGB color space
#         face_rgb = cv2.cvtColor(face["face"], cv2.COLOR_BGR2RGB)
#         cv2.imshow("frame", face["face"])q
#         cv2.imwrite(face_path, face_rgb)
#         result = DeepFace.find(img_path=face_path, db_path="./people", model_name="ArcFace", enforce_detection=False)
#         print(result[0]["identity"])
#         i += 1

#     # cv2.imshow("frame", frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# video.release()
# cv2.destroyAllWindows()