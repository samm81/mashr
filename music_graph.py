import re
import requests

API_KEY = "4462be4a4075b8e837e3789922c66ca0"

def getFeedback(song1, song2):
    tid1 = getTrackID(song1[0], song1[1])
    tid2 = getTrackID(song2[0], song2[1])

    try:
	req = (requests.get("http://api.musicgraph.com/api/v2/track/"+tid1+"/acoustical-features?api_key="+API_KEY).json()['data'],
            requests.get("http://api.musicgraph.com/api/v2/track/"+tid2+"/acoustical-features?api_key="+API_KEY).json()['data']);
    except KeyError:
	return 0

    print req
   
    tempo_match = abs(int(req[0]['tempo']) - int(req[1]['tempo'])) < 10
    duration_match = abs(int(req[0]['duration']) - int(req[1]['duration'])) < 30
    intensity_match = abs(int(req[0]['intensity']) - int(req[1]['intensity'])) < 50 
    loudness_match = abs(int(req[0]['loudness']) - int(req[1]['loudness'])) < 15
    chord_match = abs(int(req[0]['maj_chords']) - int(req[1]['maj_chords'])) < 15 

    return (tempo_match, duration_match, intensity_match, loudness_match, chord_match) 

def getTrackID(song, artist):
    req = requests.get("http://api.musicgraph.com/api/v2/track/search?api_key="+API_KEY+"&title="+song+"&artist_name="+artist+"&limit=1&fields=id")
    data = req.json()
    if len(data['data']) == 0:
	return ""
    return data['data'][0]['id']
   
def getVerbal(valid):
    if valid == 0:
	stuff = []
	thing = stuff[0]
	# return "Could not find data for both songs."
	# return 0

    names = ["tempo", "duration", "intensity", "loudness", "chord"]
    good = "These songs are a good match in "
    bad = "These songs make a poor match in "
    
    gc = 0
    bc = 0

    for i in range(0, 5):
	if valid[i]:
	    gc += 1
	    good += names[i]+", "
	else:
	    bc += 1
	    bad += names[i]+", "

    good = re.sub(r", $", ".", good) 
    good = re.sub(r", (?=\w+\.)", " and ", good)

    bad = re.sub(r", $", ".", bad)
    bad = re.sub(r", (?=\w+\.)", " and ", bad)

    total = (good if gc > 0 else "") + "\n" + (bad if bc > 0 else "") + "\n" + "Due to these "+("similarities, " if gc > bc else "conflicts, ")+"these two songs " + ("will " if gc > bc else "may not ") + "mash well together."
    return total
 
