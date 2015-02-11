#!/usr/bin/env python

import random
import time
from amigocloud import AmigoCloud

AMIGOCLOUD_EMAIL = 'my@email.com'  # Your email here
AMIGOCLOUD_PASSWORD = 'mypassword'  # Yor password here
AMIGOCLOUD_USER_ID = 0  # Your user id here
AMIGOCLOUD_PROJECT_ID = 0  # The project id here
AMIGOCLOUD_REALTIME_DATASET_ID = 0  # The dataset id here


def simulate(nr_buses=10):

    ac = AmigoCloud()
    ac.login(AMIGOCLOUD_EMAIL, AMIGOCLOUD_PASSWORD)

    url = 'users/%s/projects/%s/datasets/%s/realtime' % (
        AMIGOCLOUD_USER_ID, AMIGOCLOUD_PROJECT_ID,
        AMIGOCLOUD_REALTIME_DATASET_ID
    )

    buses = [{'lat': 37.780061, 'lng': -122.413661} for _ in xrange(nr_buses)]

    while True:
        for bus_id in xrange(nr_buses):
            buses[bus_id]['lat'] += random.uniform(-0.02, 0.02)
            buses[bus_id]['lng'] += random.uniform(-0.02, 0.02)

            now = time.time()
            moovbox_data = create_moovbox_data(
                id=bus_id,
                latitude=buses[bus_id]['lng'],
                longitude=buses[bus_id]['lat'],
                fix=0,
                time=now,
                altitude=0,
                climb=0,
                speed=0,
                separation=0,
                track=0,
                satellites=0
            )

            ac.post(url, data=moovbox_data, send_as_json=False)
            print moovbox_data

        time.sleep(1)


def create_moovbox_data(**kwargs):
    return ('<gps id="%(id)s">\n'
            '  <coordinates>\n'
            '    <coordinate>\n'
            '      <fix>%(fix)s</fix>\n'
            '      <time>%(time)s</time>\n'
            '      <latitude>%(latitude)s</latitude>\n'
            '      <longitude>%(longitude)s</longitude>\n'
            '      <altitude>%(altitude)s</altitude>\n'
            '      <climb>%(climb)s</climb>\n'
            '      <speed>%(speed)s</speed>\n'
            '      <separation>%(separation)s</separation>\n'
            '      <track>%(track)s</track>\n'
            '      <satellites>%(satellites)s</satellites>\n'
            '    </coordinate>\n'
            '  </coordinates>\n'
            '</gps>') % kwargs


if __name__ == '__main__':
    simulate()
