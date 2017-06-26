import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')
from MBTATimesGetter import getNextBusTimesScraping, getNextSubwayTimesScraping, getNextBusTimesApi
from flask import Flask
from flask_ask import Ask, statement, question, session


app = Flask(__name__)
ask = Ask(app, '/mbtaTimesFinder')


@app.route('/')
def homepage():
    return 'Hi! This is the home page of MBTA Times Skill for Amazon Alexa'


@ask.launch
def startSkill():
    startQuestion = 'Do you want to go to Kenmore, Watertown, Park Street, or Boston College?'
    return question(startQuestion)


@ask.intent('KenmoreBusIntent')
def getKenmoreBusTimes():
    busTimes = getNextBusTimesApi(stop='929')    # 929 to kenmore, 962 to watertown
    if len(busTimes)>=2:
        reply = 'The next buses to Kenmore are ' + busTimes[0] + ' and ' + busTimes[1]
    elif len(busTimes)==1:
        reply = 'The next bus to Kenmore is ' + busTimes[0]
    else:
        reply = 'Sorry, I could not find any buses to Kenmore at this time'
    return statement(reply)


@ask.intent('WatertownBusIntent')
def getWatertownBusTimes():
    busTimes = getNextBusTimesApi(stop='962')    # 929 to kenmore, 962 to watertown
    if len(busTimes)>=2:
        reply = 'The next buses to Watertown are ' + busTimes[0] + ' and ' + busTimes[1]
    elif len(busTimes)==1:
        reply = 'The next bus to Watertown is ' + busTimes[0]
    else:
        reply = 'Sorry, I could not find any buses to Watertown at this time'
    return statement(reply)


@ask.intent('ParkStreetSubwayIntent')
def getParkStreetSubwayTimes():
    subwayTimes = getNextSubwayTimesScraping('brico', 'Park Street')    # brico is Packards Corner
    if len(subwayTimes)>=2:
        reply = 'The next trains to Park Street are ' + subwayTimes[0] + ' and ' + subwayTimes[1]
    elif len(subwayTimes)==1:
        reply = 'The next train to Park Street is ' + subwayTimes[0]
    else:
        reply = 'Sorry, I could not find any trains to Park Street at this time'
    return statement(reply)


@ask.intent('BostonCollegeSubwayIntent')
def getBostonCollegeSubwayTimes():
    subwayTimes = getNextSubwayTimesScraping('brico', 'Boston College')    # brico is Packards Corner
    if len(subwayTimes)>=2:
        reply = 'The next trains to Boston College are ' + subwayTimes[0] + ' and ' + subwayTimes[1]
    elif len(subwayTimes)==1:
        reply = 'The next train to Boston College is ' + subwayTimes[0]
    else:
        reply = 'Sorry, I could not find any trains to Boston College at this time'
    return statement(reply)



if __name__ == '__main__':
    app.run(debug=True)