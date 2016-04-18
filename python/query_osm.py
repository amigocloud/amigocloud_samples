import urllib2
import xmltodict, json
from sets import Set
from amigocloud import AmigoCloud
import time
import sys

class OSMToAmigoCloud:

    def __init__(self):
        pass

    node_tags = Set()

    def query_osm(self, url):
        """
        Query OSM server and convert response to JSON
        :param url:
        :return:
        """
        print "Query OSM '%s' ..." % url
        response = urllib2.urlopen(url).read()
        json_response = xmltodict.parse(response)
        return json_response

    def write_csv(self, filename, json_obj):
        """
        Write JSON to a CSV file
        :param filename:
        :param json_obj:
        :return:
        """
        print "Parsing response ..."
        osm = json_obj['osm']
        nodes = osm['node']
        for node in nodes:
            self.build_set_from_node_tag_keys(node)

        osm = json_obj['osm']
        nodes = osm['node']
        with open(filename, 'wb') as csvfile:
            # Write header
            csvfile.write('id,lat,lon')
            for tag_key in self.node_tags:
                csvfile.write(',' + tag_key)
            csvfile.write("\n")
            for node in nodes:
                self.write_csv_row(csvfile, node)

    def upload_csv(self, project_id, token, filename):
        """
        Upload CSV file as dataset to AmigoCloud
        :param project_id:
        :param token:
        :param filename:
        :return:
        """
        user_id = 1
        amigocloud = AmigoCloud(token=token)#str(sys.argv[1]))
        response = amigocloud.upload_datafile(user_id, project_id, filename)
        print "Uploading file " + filename + " to project " + project_id + "..."

        # Wait until async job is done
        job_url = 'me/jobs/%s' % response['job']
        while True:
            response = amigocloud.get(job_url)
            if response['status'] not in ('STARTED', 'PENDING'):
                break
            time.sleep(0.5)  # Wait 500ms and retry

    def build_set_from_node_tag_keys(self, node):
        """
        Build Set of tag keys
        :param node:
        :return:
        """
        tags = node['tag']
        if isinstance(tags, list):
            for i in range(0, len(tags)):
                self.node_tags.add(tags[i]['@k'])
        else:
            self.node_tags.add(tags['@k'])

    def get_tag_value(self, tags, key):
        """
        Get value of a tag by tag key
        :param tags:
        :param key:
        :return:
        """
        if isinstance(tags, list):
            for i in range(0, len(tags)):
                if tags[i]['@k'] == key:
                    return tags[i]['@v']
        else:
            if tags['@k'] == key:
                return tags['@v']
        return ''

    def write_csv_row(self, csvfile, node):
        """
        Write node as a row to a CSV file
        :param csvfile:
        :param node:
        :return:
        """
        # Write data
        osm_id = node['@id']
        lat = node['@lat']
        lon = node['@lon']
        csvfile.write(osm_id + ',' + lat + ',' + lon)
        tags = node['tag']
        for tag_key in self.node_tags:
            value = self.get_tag_value(tags, tag_key)
            csvfile.write(',' + value)
        csvfile.write("\n")


filter="highway=bus_stop"
boundingbox="bbox=-122.21809,37.14116,-121.64131,37.49284"
# boundingbox="bbox=-122.08809,37.28116,-121.94131,37.32284"
url = "http://www.overpass-api.de/api/xapi?node["+filter+"]["+boundingbox+"]"
filename='OSM_Data.csv'
project_id = str(sys.argv[1])
token = str(sys.argv[2])

handler = OSMToAmigoCloud()
json_obj = handler.query_osm(url)
handler.write_csv(filename, json_obj)
handler.upload_csv(project_id, token, filename)

