import sys
sys.path.append('/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/site-packages')
import time
from bs4 import BeautifulSoup
import urllib3
import xml.etree.ElementTree as et
import requests


#=============================================================================#
#=============================== Web scraping ================================#
#=============================================================================#

def getNextBusTimesScraping(stop):
    route = '57A'       # will include 57 and 57a

    http = urllib3.PoolManager()
    requestUrl = 'http://www.mbtainfo.com/' + route + '/' + stop
    response = http.request('GET', requestUrl)
    soup = BeautifulSoup(response.data, 'html.parser')

    timesList = soup.find_all('li')
    
    predictions = []
    for prediction in timesList:
        predictions.append(prediction.contents[0].split()[0] + ' minutes away')

    return predictions

# start = time.time()
# print(getNextBusTimesScraping('962'))   # stop 929 to kenmore, stop 962 to watertown
# end = time.time()
# print(end-start)

def getNextSubwayTimesScraping(stop, destination):
    line = 'green'

    http = urllib3.PoolManager()
    requestUrl = 'http://www.mbtainfo.com/' + line + '/' + stop
    response = http.request('GET', requestUrl)
    soup = BeautifulSoup(response.data, 'html.parser')

    predictions = []

    if destination=='Boston College':
        eastboundTimesList = soup.find('h2', text='Eastbound').next_sibling.next_sibling.contents
        for time in eastboundTimesList:
            try:
                value = time.contents[0].split()[0] # time.tag might be <li> or '\n'
                try:
                    value = int(value)  # checking if value is an int
                    predictions.append(str(value) + ' minutes away')
                except ValueError as e: # value is not an int
                    if value=='Arriving': predictions.append(value)
            except AttributeError as e: # time.tag is not <li> (most often, it is '\n')
                continue
    
    elif destination=='Park Street':
        westboundTimesList = soup.find('h2', text='Westbound').next_sibling.next_sibling
        for time in westboundTimesList:
            try:
                value = time.contents[0].split()[0] # time.tag might be <li> or '\n'
                try:
                    value = int(value)  # checking if value is an int
                    predictions.append(str(value) + ' minutes away')
                except ValueError as e: # value is not an int
                    if value=='Arriving': predictions.append(value)
            except AttributeError as e: # time.tag is not <li> (most often, it is '\n')
                continue

    return predictions

# start = time.time()
print(getNextSubwayTimesScraping('brico', 'Park Street'))   # brico is Packards Corner stop id
# end = time.time()
# print(end-start)

#=============================================================================#
#================================ NextBus API ================================#
#=============================================================================#

def getNextBusTimesApi(stop):
    predictions = []
    routes = ['57', '57A']

    for route in routes:
        requestUrl = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=mbta&r='+route+'&s='+stop
        apiResponse = requests.get(requestUrl)
        timesList = et.fromstring(apiResponse.content)

        for child in timesList.iter(tag='prediction'):
            predictions.append(child.attrib['minutes'] + ' minutes away')

    return predictions

# start = time.time()
# print(getNextBusTimesApi('962'))
# end = time.time()
# print(end-start)

