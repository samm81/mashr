import json
import requests

def getSegments(filename):
	url2 = 'http://devapi.gracenote.com/timeline/api/1.0/audio/extract/'
	url = 'http://odp-server-env-xpubununej.elasticbeanstalk.com/api/1.0/audio/extract/'

	req = requests.post(url, files={"audio_file": open(filename, 'rb')})

	url = 'http://devapi.gracenote.com/timeline/api/1.0/audio/features/'

	print req.text
	while True:
		try:
			audio_id = req.json()['audio_id'] 
			break
		except KeyError:
			continue 
	req = requests.get(url + audio_id)
	data = req.json()
	while data['job_status']!='1':
		req = requests.get(url + audio_id)
		data = req.json()
	features = json.loads(data['features'])
	# print features
	# print the bpm
	print features['timeline']['segment']

	# make the array of tuples
	list = []
	for item in features['timeline']['segment']:
		list.append((item['start'], item['end'], item['label']))

	return list
