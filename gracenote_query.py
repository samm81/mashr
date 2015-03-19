import json
import requests

def getFeatures(filename):
    # url2 = 'http://devapi.gracenote.com/timeline/api/1.0/audio/extract/'
    url = 'http://odp-server-env-xpubununej.elasticbeanstalk.com/api/1.0/audio/extract/'

    req = requests.post(url, files={"audio_file": open(filename, 'rb')})

    url = 'http://devapi.gracenote.com/timeline/api/1.0/audio/features/'

    # print req.text

    print 'pushing song audio'
    while True:
        try:
            audio_id = req.json()['audio_id']
            break
        except KeyError:
           continue
    print 'pushed audio'
    req = requests.get(url + audio_id)
    data = req.json()
    print 'waiting for job to finish....'
    try:
        while data['job_status']!='1':
            req = requests.get(url + audio_id)
            data = req.json()
    except KeyError:
        print data
    print 'job finished!'
    features = json.loads(data['features'])    
    return features

def getSegments(features):
    # make the array of tuples
    list = []
    for item in features['timeline']['segment']:
        list.append((item['start'], item['end'], item['label']))

    return list

def getBeats(features):
	hasSkipped = False
	list = []
	prev = features['timeline']['beat'][0]['time']
	for item in features['timeline']['beat']:
		if len(list) == 0 and not hasSkipped:
			hasSkipped = True
			continue
		list.append((prev, item['time']))
		prev = item['time']

        return (features['meta']['bpm'], features['meta']['duration'], list)

def getIntro(features):
    time = 100000000
    for item in features['timeline']['segment']:
	time = min(time, int(item['end']))

    beats = sorted(getBeats(features)[2])
    for beat in beats:
	if beat[0] > time:
	    return beat[0]
    
    return time

def getOutro(features):
    time = 0 
    for item in features['timeline']['segment']:
        time = max(time, int(item['start']))

    beats = reversed(sorted(getBeats(features)[2]))
    for beat in beats:
	if beat[1] < time:
	    return beat[1] 
    
    return time

def isMatch(f1, f2):
   return abs(int(getBeats(f1)[0]) - int(getBeats(f2)[0])) < 10
