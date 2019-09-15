
from flask import Flask, request, render_template
from werkzeug import secure_filename

from imageai.Detection.Custom import CustomObjectDetection
from PIL import Image, ImageFilter

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		takeImage(f.filename)
		return render_template('image.html', image=f.filename)
	return 'boo'

app.run(host='0.0.0.0', port='80', debug='TRUE')

function takeImage(filename):
	detector = CustomObjectDetection()
	detector.setModelTypeAsYOLOv3()
	detector.setModelPath("../images/models/detection_model-ex-059--loss-0006.886.h5")
	detector.setJsonPath("../images/json/detection_config.json")
	detector.loadModel()
	detections = detector.detectObjectsFromImage(input_image=filename, output_image_path="static/"+filename)
	image = Image.open(filename)
	for detection in detections:
	    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
	    blurImage(image, detection["box_points"])
	return "success"

function blurImage(img, box[]):
	cropped_img = image.crop(box)
	blurred_img = cropped_image.filter(ImageFilter.GaussianBlur(radius=20))
	img.paste(blurred_img, box)