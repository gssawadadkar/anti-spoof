from flask import Flask, request, jsonify,render_template, Response,redirect,url_for
from models.facial_recog import recognize_employee,gen_frames,get_video_capture
from flask_cors import CORS
import cv2
import face_recognition
import mysql.connector
import numpy as np
from models.mysql_operations import fetch_employee_image, mysql_config,get_employee_name
# from models.mysql_operations import fetch_employee_image, mysql_config, get_employee_name
import dlib
import os
import subprocess
import sys






app=Flask(__name__)
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




# def gen_frames():
#     while True:
#         success, frame = cap.read()  # read the camera frame
#         if not success:
#             break
#         else:
#             # Convert the BGR frame to RGB (face_recognition uses RGB)
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#             # Find all face locations in the current frame
#             face_locations = face_recognition.face_locations(rgb_frame)

#             # Draw rectangles around the faces
#             for face_location in face_locations:
#                 top, right, bottom, left = face_location
#                 cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

#             # Convert the frame back to BGR for streaming
#             frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

#             # Encode the frame as JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # Yield the frame for streaming
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=["POST","GET"])
def index():
    return render_template('index.html')


@app.route('/video_feed',methods=["POST","GET"])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/verify_employee', methods=["POST", "GET"])
def verify_employee():
    gen_frames()
    EmpCode = request.form.get('empcode')
    print("Employee Code ==========================", EmpCode)

    try:
        consecutive_matches_threshold = 2
        consecutive_matches_count = 0
        gen_frames()
        for _ in range(8):
            matches, face_dist = recognize_employee(cap, EmpCode, mysql_config)
            print("Matches1111111111111111111111111111111111111", matches)
            if all(matches)==True and face_dist[0] <0.5:
                if consecutive_matches_count==consecutive_matches_threshold:
                    employee_name = get_employee_name(EmpCode, mysql_config)
                    print("consecutive_matches_countyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy", consecutive_matches_count)
                    restart_flask_app()
                    return render_template("result.html", status="success", employee_name_1=employee_name)
                    # break
                consecutive_matches_count += 1
               
                    

            # employee_name = get_employee_name(EmpCode, mysql_config)       
            # return render_template("result.html", status="success", employee_name_1=employee_name)       
                        # return render_template("result.html", status="success", employee_name_1=employee_name)
        else:
                 
            return render_template("result.html", status="error", message='Employee verification failed. Please try again.')

    except Exception as e:
        return render_template("result.html", status="error", message=str(e)), 500

    finally:
        cap.release()
        cv2.destroyAllWindows()
    
def restart_flask_app():
    python_executable = sys.executable
    script_path = sys.argv[0]
    subprocess.Popen([python_executable, script_path])
    sys.exit()


if __name__ == '__main__':
    app.run(debug=True)

