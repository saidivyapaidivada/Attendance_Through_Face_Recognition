from flask import Flask, request, render_template, jsonify
import pickle
import face_recognition
import numpy as np
import cv2, queue, threading, time
import os, re
import time
app = Flask(__name__)
db = {}
@app.route("/")
@app.route("/<string:className>")
def getClass(className):
	if "class" in className.lower() and len(className)==6:
		pass
	else:
		className="ClassA"
	students = []
	try:
		students = [student[:-4] for student in os.listdir(f"static/pictures/"+className)]
	except:
		return "<h1 style='margin:auto;margin:100px;font-size:50px;'>Please provide correct class name</h1>"
	return render_template("class.html",students = students,className = className)

@app.route("/<string:className>/status",methods=["GET"])
def getClassStatus(className):
	known_face_encodings = []
	known_face_names = []
	known_faces_filenames = os.listdir(f"static/pictures/{className}")
	for filename in known_faces_filenames:
	    face = face_recognition.load_image_file(f'static/pictures/{className}/' + filename)
	    known_face_names.append(re.sub("[0-9]",'', filename[:-4]))
	    known_face_encodings.append(face_recognition.face_encodings(face)[0])
	face_locations = []
	face_encodings = []
	face_names = []
	cap = cv2.VideoCapture(0)
	ret,frame = cap.read()
	cap.release()
	face_locations = face_recognition.face_locations(frame)
	face_encodings = face_recognition.face_encodings(frame, face_locations)
	# Initialize an array for the name of the detected users
	face_names = []
	for face_encoding in face_encodings:
    	# See if the face is a match for the known face(s)
		
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
		
		# Or instead, use the known face with the smallest distance to the new face
		face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
		
		best_match_index=-1
		try:
			best_match_index = np.argmin(face_distances)
			if matches[best_match_index]:
				name = known_face_names[best_match_index]
				if name not in face_names:
					face_names.append(name)
		except:
			pass
	status = {}
	for name in known_face_names:
		if name in face_names:
			status[name]="Active"
		else:
			status[name]="Inactive"
	return jsonify(status)

@app.route("/extra",methods=["GET"])
def getExtra():
	return "<h1>Is this info enough to tell that this is working</h1>"


if __name__=="__main__":
	app.debug = True
	app.run(host="0.0.0.0")

	
