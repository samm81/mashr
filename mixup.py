from pydub import AudioSegment
from gracenote_query import getSegments

CROSSFADE_TIME = 1000

def mixup (path1, path2, segments1, segments2):
	song1 = AudioSegment.from_mp3(path1)
	song2 = AudioSegment.from_mp3(path2)

	song = AudioSegment.empty()
	print 'zip:', zip(segments1, segments2)
	for i, (times1, times2) in enumerate(zip(segments1, segments2)):
		if i % 2 is 0:
			segment = song1[times1[0]*1000 : times1[1]*1000]
		else:
			segment = song2[times2[0]*1000 : times2[1]*1000]

		if i is 0:
			song = segment
		else:
			song = song.append(segment, crossfade=CROSSFADE_TIME)

	return song

def export (song, name):
	song.export(name, format="mp3")



#path1 = "Blank Space.mp3"
#path2 = "Style.mp3"
#segments1 = [5, 11]
#segments2 = [20, 26]
#mixup(path1, path2, segments1, segments2)
path1 = "Blank Space.mp3"
path2 = "Style.mp3"
segments1 = getSegments(path1)
#print 'segments1:', segments1
segments2 = getSegments(path2)
#print 'segments2:', segments2
#segments1 = [(0,30),(30,45),(45,60)]
#segments2 = [(0,15),(15,30),(30,60)]
export(mixup(path1, path2, segments1, segments2), "thisisntevenmyfinalform.mp3")
