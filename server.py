import os
from flask import Flask, render_template, request, copy_current_request_context, session
from flask.ext.socketio import SocketIO, emit
from mixup import mix_from_paths
from music_graph import getVerbal, getFeedback
from mp3_metadata import getSongInfo
from threading import Thread
import uuid

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
    session['id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route("/loading", methods=['GET','POST'])
def loading():
    songName1 = ''
    songName2 = ''
    if request.method == 'POST':
		f = request.files['song1']
		songName1 = request.form['songName1']
		f.save('static/song1' + session['id'] + '.mp3')
		f = request.files['song2']
		songName2 = request.form['songName2']
		f.save('static/song2' + session['id'] + '.mp3')
    return render_template('loading.html')

@socketio.on('connect', namespace='/song_done')
def mash():
    @copy_current_request_context
    def load_song():
        mix_from_paths('static/song1' + session['id'] + '.mp3','static/song2' + session['id'] + '.mp3', 'thisisntevenmyfinalform' + session['id'] + '.mp3')
        emit('song done', {'data': 'the song has been created'})
    thread = Thread(target = load_song, args=())
    thread.start()

@app.route("/download")
def download():
	session.pop('id', None)
	return render_template('download.html', id=session['id'])

@app.route("/info")
def info():
	strings = getVerbal(getFeedback(getSongInfo('static/song1' + session['id'] + '.mp3'), getSongInfo('static/song2') + session['id'] + '.mp3'))
	strings = "According to MusicGraph, " + strings
	return strings

if __name__ == "__main__":
    # The key used for encrypting the session cookie
    app.secret_key = '?\xc8\xcb\xe9\xf7\xe1^n[\xb5\x98\xf8o\x8c:\xe2%V\x80\x05=\xad\xa6\xb7'
    socketio.run(app, host='0.0.0.0')
