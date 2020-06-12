from imutils.video import WebcamVideoStream
from flask import Response, Flask, render_template
import threading
import numpy as np
import imutils
import time
import cv2

outputFrame = None
lock = threading.Lock()

app = Flask(__name__)

protoPath = "face_detection_model/deploy.prototxt"
modelPath = "face_detection_model/res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# initialize the video stream, then allow the camera sensor to warm up
vs = WebcamVideoStream(src="/dev/video0").start()
time.sleep(2.0)


@app.route("/")
def index():
	# return the rendered template
	return render_template("index.html")


def face_detect():

	global vs, outputFrame, lock

	while True:
		frame = vs.read()
		frame = imutils.resize(frame, width=600)
		(h, w) = frame.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		detector.setInput(imageBlob)
		detections = detector.forward()

		for i in range(0, detections.shape[2]):
			confidence = detections[0, 0, i, 2]

			# filter out weak detections
			if confidence > 0.5 :

				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

		with lock:
			outputFrame = frame.copy()


def generate():
	global outputFrame, lock
	while True:
		with lock:
			if outputFrame is None:
				continue
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
			if not flag:
				continue
		yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage.tobytes()) + b'\r\n'


@app.route("/video_feed")
def video_feed():
	return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")


if __name__ == '__main__':

	t = threading.Thread(target=face_detect)
	t.daemon = True
	t.start()

	# start the flask app
	app.run(host='0.0.0.0', port=4000, debug=True, threaded=True, use_reloader=False)

vs.stop()
