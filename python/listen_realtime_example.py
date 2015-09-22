from amigocloud import AmigoCloud
amigocloud = AmigoCloud(token='<token>')

owner_id = 1  # Project Owner ID
project_id = 2  # Project ID
dataset_id = 3  # Dataset ID

amigocloud.listen_dataset_events(owner_id, project_id, dataset_id)

def realtime(data):
    print 'Realtime dataset id=%(dataset_id)s' % data
    for obj in data['data']:
        print "Object '%(object_id)s' is now at (%(latitude)s, %(longitude)s)" % obj

amigocloud.add_callback('realtime', realtime)
amigocloud.start_listening()
