from pydub import AudioSegment

def mixup (path1, path2, segments1, segments2):
	song1 = AudioSegment.from_mp3(path1)
	song2 = AudioSegment.from_mp3(path2)
	second_slice = song2[segments2[0]*1000:segments2[1]*1000]
	first_beginning = song1[:segments1[0]*1000]
	first_end = song1[segments1[1]*1000:]

	mixed = first_beginning.append(second_slice, crossfade=1500).append(first_end, crossfade = 1500)
	mixed.export("mixed.mp3", format="mp3")



path1 = "Blank Space.mp3"
path2 = "Style.mp3"
segments1 = [5, 11]
segments2 = [20, 26]
mixup(path1, path2, segments1, segments2)
