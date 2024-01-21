from flask import Flask, request, jsonify,render_template, Response
from flask_cors import CORS
import cv2
import face_recognition
import mysql.connector
import numpy as np
from models.mysql_operations import fetch_employee_image, mysql_config, get_employee_name
from models.facial_recog import recognize_employee, gen_frames,cap
import dlib
import os



app=Flask(__name__)





def gen_frames():  
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            
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


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')





@app.route('/verify_employee', methods=["POST", "GET"])
def verify_employee():
    # Assuming you have a video capture object
    # cap = cv2.VideoCapture(0)  # Adjust the index based on your camera configuration

    EmpCode = request.form.get('empcode')
    print("Employee Code ==========================", EmpCode)

    try:
        consecutive_matches_threshold = 2
        consecutive_matches_count = 0
        gen_frames()
        
        for _ in range(8):
            matches, face_dist = recognize_employee(cap, EmpCode, mysql_config)
            print("Matches1111111111111111111111111111111111111", matches)
            
            if matches and face_dist and all(matches) and len(face_dist) > 0 and face_dist[0] < 0.5:
                if consecutive_matches_count == consecutive_matches_threshold:
                    employee_name = get_employee_name(EmpCode, mysql_config)
                    print("consecutive_matches_countyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", consecutive_matches_count)
                    return render_template("result.html", status="success", employee_name_1=employee_name)
                
                consecutive_matches_count += 1

        else:
            return render_template("result.html", status="error", message='Employee verification failed. Please try again.')

    except Exception as e:
        return render_template("result.html", status="error", message=str(e)), 500

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(debug=True)



