import json
import urllib2
import random
import time
from datetime import datetime
from amigocloud import AmigoCloud, AmigoCloudError

AMIGOCLOUD_EMAIL = 'my@email.com'
AMIGOCLOUD_PASSWORD = 'mypassword'
AMIGOCLOUD_USER_ID = ##
AMIGOCLOUD_PROJECT_ID = ####
AMIGOCLOUD_REALTIME_DATASET_ID = ####

ac = AmigoCloud()
ac.login(AMIGOCLOUD_EMAIL, AMIGOCLOUD_PASSWORD)

buses = [[0 for x in range(2)] for x  in range(10)]


def busesGo () :

    random.seed()

    while (1):

        for i in range( 0, 10) :

            if buses[i][0] == 0:
                buses[i][0] = -122.413661
                buses[i][1] = 37.780061
            else:
                randomXDistance = random.uniform(-0.02, 0.02)
                randomYDistance = random.uniform(-0.02, 0.02)

                buses[i][0] = buses[i][0] + randomXDistance
                buses[i][1] = buses[i][1] + randomYDistance

            latitude = buses[i][0]
            longitude = buses[i][1]
            id = i
            bustime = datetime.now()

            moovbox_data = CreateMoveBoxData( id, latitude, longitude, 0, bustime, 0, 0, 1, 0, 0, 0 )

            url = 'users/' + str(AMIGOCLOUD_USER_ID) + '/projects/' + str(AMIGOCLOUD_PROJECT_ID) + '/datasets/' + str(AMIGOCLOUD_REALTIME_DATASET_ID) + '/realtime'

            ac.post(url, data=moovbox_data, send_as_json=False)

            print moovbox_data

        time.sleep(1)




def CreateMoveBoxData( id, latitude, longitude, fix, time, altitude, climb, speed, separation, track, satellites ):

    xml = '<gps id="' + str(id) + '">'
    xml += '<coordinates>'
    xml += '<coordinate>'
    xml += '<fix>' + str(fix) + '</fix>'
    xml += '<time>' + str(time) + '</time>'
    xml += '<latitude>' + str(latitude) + '</latitude>'
    xml += '<longitude>' + str(longitude) + '</longitude>'
    xml += '<altitude>' + str(altitude) + '</altitude>'
    xml += '<climb>' + str(climb) + '</climb>'
    xml += '<speed>' + str(speed) + '</speed>'
    xml += '<separation>' + str(separation) + '</separation>'
    xml += '<track>' + str(track) + '</track>'
    xml += '<satellites>' + str(satellites) + '</satellites>'
    xml += '</coordinate>'
    xml += '</coordinates>'
    xml += '</gps>'

    return xml



# request
busesGo()



