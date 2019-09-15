
import os
from flask import Flask, request, render_template
from werkzeug import secure_filename

from imageai.Detection.Custom import CustomObjectDetection
from PIL import Image, ImageFilter

app = Flask(__name__)

app.config["UPLOAD_PATH"] = "static"

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.config["UPLOAD_PATH"], filename))
		detector = CustomObjectDetection()
		detector.setModelTypeAsYOLOv3()
		detector.setModelPath("../images/models/detection_model-ex-059--loss-0006.886.h5")
		detector.setJsonPath("../images/json/detection_config.json")
		detector.loadModel()
		detections = detector.detectObjectsFromImage(input_image="static/"+f.filename, output_image_path="static/trashfire-"+f.filename, minimum_percentage_probability=30)
		image = Image.open("static/"+f.filename)
		for detection in detections:
			print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
			cropped_img = image.crop(detection["box_points"])
			blurred_img = cropped_img.filter(ImageFilter.GaussianBlur(radius=20))
			image.paste(blurred_img, detection["box_points"])
			image.save("static/"+f.filename)
		return render_template('image.html', image=f.filename, timage="trashfire-"+f.filename)
	return 'boo'

app.run(host='0.0.0.0', port='80', debug='TRUE')
