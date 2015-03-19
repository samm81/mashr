from flask import Flask
from flask import render_template
from flask import request
from mixup import mix_from_paths
app = Flask(__name__)

@app.route("/")
def hello():
	#return "hello world!"
	return render_template('index.html')

@app.route("/loading", methods=['GET','POST'])
def loading():
	if request.method == 'POST':
		f = request.files['song1']
		f.save('song1.mp3')
		f = request.files['song2']
		f.save('song2.mp3')
	return render_template('loading.html')

@app.route("/download")
def download():
	print "in download"
	mix_from_paths('song1.mp3','song2.mp3')
	return render_template('download.html')

if __name__ == "__main__":
	app.run()
