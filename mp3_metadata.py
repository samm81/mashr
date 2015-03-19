import eyed3

def getTitle(filename):
    audio = eyed3.load(filename)
    return audio.tag.title

def getArtist(filename):
    return eyed3.load(filename).tag.artist

def getSongInfo(filename):
    return (getTitle(filename), getArtist(filename))
