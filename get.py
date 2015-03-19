import requests

url = 'http://devapi.gracenote.com/timeline/api/1.0/audio/features/'
audio_id = '41646f89c4473a95ac8498f8567c9049'

req = requests.get(url + audio_id)
data = req.json()
features = data['features']

# print the bpm
print features['meta']['bpm']
