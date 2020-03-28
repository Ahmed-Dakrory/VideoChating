from flask import send_file
from flask import Flask
from flask import Response
from flask import render_template
import numpy as np
import cv2
import time


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame

    cap=cv2.VideoCapture(0)
    
    # loop over frames from the output stream
    while True:
        time.sleep(0.01)
        # Capture frame-by-frame
        ret, outputFrame = cap.read()
	# encode the frame in JPEG format
        (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
        # ensure the frame was successfully encoded
        if not flag:
            continue
            
        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')



app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"


@app.route("/vid")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/path')
def get_image():
    
    filename = 'image1.jpeg'
    
    return send_file(filename, mimetype='image/gif')







app.run(host='0.0.0.0')





