import os
from flask import Flask
from flask import render_template
from flask import request
from flask import copy_current_request_context
from flask.ext.socketio import SocketIO, emit
from mixup import mix_from_paths
from music_graph import getVerbal, getFeedback
from mp3_metadata import getSongInfo
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)


songName1 = ''
songName2 = ''

@app.route("/")
def hello():
	#return "hello world!"
	#if os.path.exists('static/thisisntevenmyfinalform.mp3'):
	#	os.remove("static/thisisntevenmyfinalform.mp3")
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

@socketio.on('connect', namespace='/song_done')
def mash():
    @copy_current_request_context
    def load_song():
        mix_from_paths('song1.mp3','song2.mp3')
        emit('song done', {'data': 'the song has been created'})
    thread = Thread(target = load_song, args=())
    thread.start()

@app.route("/download")
def download():
	return render_template('download.html')

@app.route("/info")
def info():
	strings = getVerbal(getFeedback(getSongInfo('song1.mp3'), getSongInfo('song2.mp3')))
	strings = "According to MusicGraph, " + strings
	return strings

if __name__ == "__main__":
	socketio.run(app)

