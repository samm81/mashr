from pydub import AudioSegment
from gracenote_query import getBeats, getFeatures, getIntro, getOutro

CROSSFADE = 0

def mixup (path1, path2, beats1, beats2, introTime, outroTime):
	song1 = getSong(path1)
	song2 = getSong(path2)

	segments1 = beats1[2]
	segments2 = beats2[2]

	song = AudioSegment.empty()
	for i, (time1, time2) in enumerate(zip(segments1, segments2)):
		if time1[0] < introTime:
			continue;
		elif time2[1] > outroTime:
			break;
		if i % 2 is 0:
			segment = song1[time1[0]*1000 : time1[1]*1000]
		else:
			segment = song2[time2[0]*1000 : time2[1]*1000]

		if i is 0:
			song = segment
		else:
			song = song.append(segment, crossfade=CROSSFADE)

	return song

def getSong(path):
	return AudioSegment.from_mp3(path)

def introSong(song, endIntroTime):
	return song[:endIntroTime*1000]
def outroSong(song, begOutroTime):
	return song[begOutroTime*1000:]


def export (song, name):
	song.export(name, format="mp3")



#path1 = "Blank Space.mp3"
#path2 = "Style.mp3"
#segments1 = [5, 11]
#segments2 = [20, 26]
#mixup(path1, path2, segments1, segments2)
path1 = "alpha.mp3"
path2 = "jump.mp3"
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
intro = introSong(getSong(path1), introTime)
outroTime = getOutro(features2)
outro = outroSong(getSong(path2), outroTime)

export(intro.append(mixup(path1, path2, beats1, beats2, introTime, outroTime)).append(outro), "thisisntevenmyfinalform.mp3")
print 'mashup created - all done'
