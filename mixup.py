from pydub import AudioSegment
from gracenote_query import getBeats

CROSSFADE = 0

def mixup (path1, path2, beats1, beats2):
	song1 = AudioSegment.from_mp3(path1)
	song2 = AudioSegment.from_mp3(path2)

	numBeats1 = beats1[0] * (beats1[1] / 60)
	beatLength1 = beats1[1] / numBeats1
	numBeats2 = beats2[0] * (beats2[1] / 60)
	beatLength2 = beats2[1] / numBeats2

	minBeats = min(numBeats1, numBeats2)
	segments1 = beats1[2]
	segments2 = beats2[2]

	song = AudioSegment.empty()
	for i, (time1, time2) in enumerate(zip(segments1, segments2)):
		if i % 2 is 0:
			segment = song1[time1[0]*1000 : time1[1]*1000]
		else:
			segment = song2[time2[0]*1000 : time2[1]*1000]

		if i is 0:
			song = segment
		else:
			song = song.append(segment, crossfade=CROSSFADE)

	return song

def export (song, name):
	song.export(name, format="mp3")



#path1 = "Blank Space.mp3"
#path2 = "Style.mp3"
#segments1 = [5, 11]
#segments2 = [20, 26]
#mixup(path1, path2, segments1, segments2)
path1 = "jump.mp3"
path2 = "alpha.mp3"
print 'loaded and alive'
print 'song 1 is', path1
print 'song 2 is', path2

print 'getting beats for song 1...'
beats1 = getBeats(path1)
print 'recieved beats for song 1'

print 'getting beats for song 2'
#print 'segments1:', segments1
beats2 = getBeats(path2)
#print 'segments2:', segments2
#segments1 = [(0,30),(30,45),(45,60)]
#segments2 = [(0,15),(15,30),(30,60)]
print 'recieved beats for song 2'

print 'creating the mashup!'
export(mixup(path1, path2, beats1, beats2), "thisisntevenmyfinalform.mp3")
print 'mashup created - all done'
