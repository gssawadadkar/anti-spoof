import face_recognition
import cv2
import numpy as np
from models.mysql_operations import fetch_employee_image, mysql_config, get_employee_name
# from mysql_operations import fetch_employee_image, mysql_config, get_employee_name
import dlib
import os

def get_video_capture():
    try:
        cap = cv2.VideoCapture(0)  # Adjust the index based on your camera configuration
        if not cap.isOpened():
            raise RuntimeError("Could not open camera. Please make sure the camera is connected.")
        return cap
    except Exception as e:
        print(f"Error initializing camera: {str(e)}")
        return None

# Initialize the camera outside the route function
cap = get_video_capture()



def gen_frames():  
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            # frame = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
            print("*********************************************************unknown frame from gen_frames",frame.shape)
            faces=detector.detectMultiScale(frame,1.1,7)
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
             #Draw the rectangle around each face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                # roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                # eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 3)
                for (ex, ey, ew, eh) in faces:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')




#######################                           Working--------------------

def recognize_employee(cap, EmpCode, mysql_config):
    # gen_frames()
    # cap = get_video_capture()

    known_face = fetch_employee_image(EmpCode, mysql_config)
    # print("known faceiiiiiiiiiiiiii",known_face.shape)
    # known_face = cv2.resize(known_face, (new_height,new_width))
    print("known faceiiiiiiiiiiiiii",known_face.shape)
    face_known_frame = face_recognition.face_locations(known_face)
    encode_known_face = face_recognition.face_encodings(known_face, face_known_frame)

    while True:
        success, img = cap.read()
        # new_width, new_height = 1160, 522
        img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        # img = cv2.resize(img, (new_height,new_width))
        print("UNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNknown faceiiiiiiiiiiiiii",img_s.shape)
        img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)
        face_cur_frame = face_recognition.face_locations(img_s)
        encode_cur_frame = face_recognition.face_encodings(img_s, face_cur_frame)
        

        for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
            matches = face_recognition.compare_faces(encode_known_face, encode_face, tolerance=0.5)
            face_dist = face_recognition.face_distance(encode_known_face, encode_face)

            print("matches:", matches)
            print("data type of matches sssssssssssssssss:",type(matches[0]))
            print("face_dist:", face_dist)
            return matches,face_dist
        
 ################################################################################
 ######################trial#######################
 
# def recognize_employee(cap, EmpCode, mysql_config):
#     known_face = fetch_employee_image(EmpCode, mysql_config)

#     # Check if the known_face is loaded successfully
#     if known_face is None or known_face.size == 0:
#         print("Error: Unable to fetch or empty known face.")
#         return [], []

#     face_known_frame = face_recognition.face_locations(known_face)
#     encode_known_face = face_recognition.face_encodings(known_face, face_known_frame)

#     while True:
#         success, img = cap.read()

#         # Check if the image is read successfully
#         if not success or img is None or img.size == 0:
#             print("Error: Unable to read or empty frame.")
#             return [], []

#         img_s = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#         img_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2RGB)
#         face_cur_frame = face_recognition.face_locations(img_s)
#         encode_cur_frame = face_recognition.face_encodings(img_s, face_cur_frame)

#         matches_list = []
#         face_dist_list = []

#         for encode_face, face_loc in zip(encode_cur_frame, face_cur_frame):
#             matches = face_recognition.compare_faces(encode_known_face, encode_face, tolerance=0.5)
#             face_dist = face_recognition.face_distance(encode_known_face, encode_face)

#             print("matches:", matches)
#             print("data type of matches sssssssssssssssss:", type(matches[0]))
#             print("face_dist:", face_dist)

#             matches_list.append(matches)
#             face_dist_list.append(face_dist)
            
            
#         cap.release()
#         cv2.destroyAllWindows()   
#         return matches_list, face_dist_list
    # This line should not be indented inside the while loop
    # print("from this function getting error so fix now")


# Example usage
if __name__=="__main__":
    cap = cv2.VideoCapture(0)
    EmpCode = input("Enter employee code: ")
    recognize_employee(cap, EmpCode, mysql_config)  # Replace mysql_config with your actual MySQL configuration




