import requests

filename = 'wtny.mp3'
url = 'http://devapi.gracenote.com/timeline/api/1.0/audio/extract/'

req = requests.post(url, files={
                                  "audio_file": open(filename, 'rb')
                               }
)
