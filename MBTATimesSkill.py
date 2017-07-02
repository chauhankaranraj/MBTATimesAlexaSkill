import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')
from MBTATimesGetter import getNextBusTimesScraping, getNextSubwayTimesScraping, getNextBusTimesApi
from flask import Flask
from flask_ask import Ask, statement, question, session, audio


app = Flask(__name__)
ask = Ask(app, '/mbtaTimesFinder')


@app.route('/')
def homepage():
    return 'Hi! This is the home page of MBTA Times Skill for Amazon Alexa'


@ask.launch
def startSkill():
    startQuestion = 'Do you want to go to Kenmore, Watertown, Park Street, or Boston College?'
    return question(startQuestion)

#==============================================================================================#
#======================================= MBTA Bus Times =======================================#
#==============================================================================================#

busStopIds = {'kenmore':'929', 'ken more':'929', 'college':'929', 'watertown':'962', 'water town':'962', 'dunkin donuts':'962'}	    # 929 to kenmore, 962 to watertown

@ask.intent('BusIntent')
def getBusTimes(busDestination):
    print('\n\n\nreceived ' + str(busDestination) + '\n\n\n')
    busTimes = getNextBusTimesApi(stop=busStopIds[str(busDestination).lower()])
    
    if len(busTimes)>=2:
        reply = 'The next buses to ' + str(busDestination) + ' are ' + busTimes[0] + ' and ' + busTimes[1]
    elif len(busTimes)==1:
        reply = 'The next bus to ' + str(busDestination) + ' is ' + busTimes[0]
    else:
        reply = 'Sorry, I could not find any buses to ' + str(busDestination) + ' at this time'
    
    return statement(reply)

#==============================================================================================#
#======================================== MBTA T Times ========================================#
#==============================================================================================#

@ask.intent('SubwayIntent')
def getSubwayTimes(subwayDestination):
    subwayTimes = getNextSubwayTimesScraping('brico', str(subwayDestination))    # brico is Packards Corner
   
    if len(subwayTimes)>=2:
        reply = 'The next trains to ' + str(subwayDestination) + ' are ' + subwayTimes[0] + ' and ' + subwayTimes[1]
    elif len(subwayTimes)==1:
        reply = 'The next train to ' + str(subwayDestination) + ' is ' + subwayTimes[0]
    else:
        reply = 'Sorry, I could not find any trains to ' + str(subwayDestination) + ' at this time'
    
    return statement(reply)

#==============================================================================================#
#======================================== Music Player ========================================#
#==============================================================================================#

allSongsUrls = {
	'despacito': 'https://archive.org/download/LuisFonsi_324/LuisFonsi-Despacitoft.DaddyYankee.ogg',
	'sugar how you get so fly': 'https://archive.org/download/RobinSchulzSugarfeat.FrancescoYatesOFFICIALMUSICVIDEO_201611/Robin%20Schulz%20-%20Sugar%20(feat.%20Francesco%20Yates)%20(OFFICIAL%20MUSICVIDEO).ogg',
	'photograph': 'https://archive.org/download/Photograph_201512/Photograph.ogg',
	'sweet child o mine': 'https://ia801608.us.archive.org/26/items/GunsNRosesSweetChildOMine_201703/Guns%20N%20Roses%20-%20Sweet%20Child%20O%20Mine.ogg',	
    'bailando': 'https://archive.org/details/BailandoSpanishVersion'
}

playlists = {
    'chill' = [
        'https://archive.org/download/LuisFonsi_324/LuisFonsi-Despacitoft.DaddyYankee.ogg',
        'https://archive.org/download/RobinSchulzSugarfeat.FrancescoYatesOFFICIALMUSICVIDEO_201611/Robin%20Schulz%20-%20Sugar%20(feat.%20Francesco%20Yates)%20(OFFICIAL%20MUSICVIDEO).ogg',
        'https://archive.org/details/BailandoSpanishVersion'
    ]
}


currentPlaylistName = None
currentSongIndex = 0

@ask.intent('MusicIntent')
def playSong(songName):
	url = allSongsUrls[str(songName)]
	return audio('Playing ' + str(songName)).play(url)

@ask.intent('StartPlaylistIntent')
def startPlaylist(playlistName):
    currentPlaylistName = playlistName
    return audio('Playing ' + str(playlistName) + ' playlist').play(playlists[str(playlistName).lower()][0])

@ask.playback_nearly_finished()
def queueNextSongInPlaylist():
    if currentSongIndex < len(playlists[str(currentPlaylistName)])-1:
        currentSongIndex += 1
        return audio.enqueue(playlists[currentPlaylistName][currentSongIndex])

@ask.on_playback_finished()
def notifyIfEndOfPlaylist():
    if currentSongIndex == len(playlists[currentPlaylistName])-1:
        return statement('There are no more songs in this playlist!')

@ask.intent('AMAZON.PauseIntent')
def pausedemo():
	return audio.stop()

@ask.intent('AMAZON.ResumeIntent')
def pausedemo():
	return audio.resume()

@ask.intent('AMAZON.StopIntent')
def pausedemo():
	return audio.clear_queue(stop=True)


    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
