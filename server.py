import os
from flask import Flask
from flask import render_template
from flask import request
from mixup import mix_from_paths
from music_graph import getVerbal, getFeedback
app = Flask(__name__)

songName1 = ''
songName2 = ''

@app.route("/")
def hello():
	#return "hello world!"
	if os.path.exists('static/thisisntevenmyfinalform.mp3'):
		os.remove("static/thisisntevenmyfinalform.mp3")
	return render_template('index.html')

@app.route("/loading", methods=['GET','POST'])
def loading():
	if request.method == 'POST':
		f = request.files['song1']
		songName1 = request.form['songName1']
		f.save('song1.mp3')
		f = request.files['song2']
		songName2 = request.form['songName2']
		f.save('song2.mp3')
	return render_template('loading.html')

@app.route("/song_done")
def load_song():
	mix_from_paths('song1.mp3','song2.mp3')
	return "Loaded!"

@app.route("/download")
def download():
	return render_template('download.html')

@app.route("/info")
def info():
	print getVerbal(getFeedback(songName1, songName2))
	return ''

if __name__ == "__main__":
	app.run()
