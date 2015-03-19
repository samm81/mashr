import sys
from pydub import AudioSegment
from gracenote_query import getBeats, getFeatures, getIntro, getOutro

CROSSFADE = 0
FADE_DURATION = 5000

def mixup (path1, path2, beats1, beats2):
	song1 = getSong(path1)
	song2 = getSong(path2)

	segments1 = beats1[2]
	segments2 = beats2[2]

	song = AudioSegment.empty()
	for i, (time1, time2) in enumerate(zip(segments1, segments2)):
		if i % 2 is 0:
			segment = song1[time1[0]*1000 : time1[1]*1000]
		else:
			segment = song2[time2[0]*1000 : time2[1]*1000]

		song = song.append(segment, crossfade=CROSSFADE)

	return song.fade_in(FADE_DURATION).fade_out(FADE_DURATION)

def getSong(path):
	return AudioSegment.from_mp3(path)

def export (song, name):
	song.export(name, format="mp3")

def mix_from_paths(path1, path2):
	print 'loaded and alive'
	print 'song 1 is', path1
	print 'song 2 is', path2

	print 'getting beats for song 1...'
	features1 = getFeatures(path1)
	beats1 = getBeats(features1)
	print 'recieved beats for song 1'

	print 'getting beats for song 2'
	features2 = getFeatures(path2)
	beats2 = getBeats(features2)
	print 'recieved beats for song 2'

	print 'creating the mashup!'

	export(mixup(path1, path2, beats1, beats2), "output/thisisntevenmyfinalform.mp3")
	print 'mashup created - all done'

mix_from_paths(sys.argv[1], sys.argv[2])
