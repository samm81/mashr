import sys
from pydub import AudioSegment
from gracenote_query import getBeats, getFeatures, getIntro, getOutro

CROSSFADE = 0

def mixup (path1, path2, beats1, beats2, introTime, outroTime):
	song1 = getSong(path1)
	song2 = getSong(path2)

	segments1 = beats1[2]
	segments2 = beats2[2]

	song = song1[:introTime*1000 + 1]

	i = 0
	for time1, time2 in zip(segments1, segments2):
		if time1[0] < introTime:
			continue;
		elif time2[1] > outroTime:
			break;
		if i % 2 is 0:
			segment = song1[time1[0]*1000 : time1[1]*1000]
		else:
			segment = song2[time2[0]*1000 : time2[1]*1000]

		song = song.append(segment, crossfade=CROSSFADE)
		i += 1

	song = song.append(song2[outroTime*1000:])
	return song

def getSong(path):
	return AudioSegment.from_mp3(path)

def export (song, name):
	song.export(name, format="mp3")



#path1 = "Blank Space.mp3"
#path2 = "Style.mp3"
#segments1 = [5, 11]
#segments2 = [20, 26]
#mixup(path1, path2, segments1, segments2)
#path1 = "alpha.mp3"
#path2 = "jump.mp3"
path1 = sys.argv[1]
path2 = sys.argv[2]
print 'loaded and alive'
print 'song 1 is', path1
print 'song 2 is', path2

print 'getting beats for song 1...'
features1 = getFeatures(path1)
beats1 = getBeats(features1)
print 'recieved beats for song 1'

print 'getting beats for song 2'
#print 'segments1:', segments1
features2 = getFeatures(path2)
beats2 = getBeats(features2)
#print 'segments2:', segments2
#segments1 = [(0,30),(30,45),(45,60)]
#segments2 = [(0,15),(15,30),(30,60)]
print 'recieved beats for song 2'

print 'creating the mashup!'
introTime = getIntro(features1)
print 'introTime:', introTime
outroTime = getOutro(features2)
print 'outroTime:', outroTime

export(mixup(path1, path2, beats1, beats2, introTime, outroTime), "thisisntevenmyfinalform.mp3")
print 'mashup created - all done'
