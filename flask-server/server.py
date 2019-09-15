
from flask import Flask, request, render_template
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		f = request.files['file']
		f.save(secure_filename(f.filename))
		return render_template('image.html', image=f.filename)
	return 'boo'

app.run(host='0.0.0.0', port='80', debug='TRUE')