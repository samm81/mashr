import os
from flask import Flask, render_template, request, copy_current_request_context, make_response
from flask.ext.socketio import SocketIO, emit
from mixup import mix_from_paths
from music_graph import getVerbal, getFeedback
from mp3_metadata import getSongInfo
from threading import Thread
import uuid
import logging

app = Flask(__name__)
socketio = SocketIO(app)

# Disable caching to fix refresh bug
@app.after_request
def add_header(response):
	response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
	response.headers['Cache-Control'] = 'public, max-age=0'
	return response

@app.route("/")
def hello():
	id = str(uuid.uuid4())
	resp = make_response(render_template('index.html'))
	resp.set_cookie('id', id)
	app.logger.debug("id: {}".format(id))
	return resp

@app.route("/loading", methods=['GET','POST'])
def loading():
	id = request.cookies.get('id')
	songName1 = ''
	songName2 = ''
	if request.method == 'POST':
		f = request.files['song1']
		songName1 = request.form['songName1']
		f.save('static/song1' + id + '.mp3')
		f = request.files['song2']
		songName2 = request.form['songName2']
		f.save('static/song2' + id + '.mp3')
	return render_template('loading.html')

@socketio.on('connect', namespace='/song_done')
def mash():
	@copy_current_request_context
	def load_song():
		id = request.cookies.get('id')
		mix_from_paths('static/song1' + id + '.mp3','static/song2' + id + '.mp3', 'thisisntevenmyfinalform' + id + '.mp3')
		emit('song done', {'data': 'the song has been created'})
	thread = Thread(target = load_song, args=())
	thread.start()

@app.route("/download")
def download():
	userId = request.cookies.get('id')
	return render_template('download.html', id=userId)

@app.route("/info")
def info():
	id = request.cookies.get('id')
	strings = getVerbal(getFeedback(getSongInfo('static/song1' + id + '.mp3'), getSongInfo('static/song2') + id + '.mp3'))
	strings = "According to MusicGraph, " + strings
	return strings

if __name__ == "__main__":
	host = '0.0.0.0'
	port = 8000
	level = logging.DEBUG
	
	file_handler = logging.FileHandler('log', mode='w')
	file_handler.setLevel(level)
	app.logger.addHandler(file_handler)
	logging.getLogger("werkzeug").addHandler(file_handler)
	
	app.logger.info("started running with host {} on port {}, debug = {}".format(host, port, app.debug))
	socketio.run(app, host=host, port=port)
