from six import BytesIO
import json
import time
import uuid
from zipfile import ZipFile

from amigocloud import AmigoCloud
from PIL import Image

# Your parameters
TOKEN = '<AN_AMIGOCLOUD_ADMIN_TOKEN>'
OWNER_ID = 1
PROJECT_ID = 123

PROJECT_URL = '/users/%s/projects/%s' % (OWNER_ID, PROJECT_ID)

WONDERS = [
    (78.0421006679535, 27.1749801931118, 'Taj Mahal'),
    (-88.5717236995697, 20.6828287415649, 'Chichen Itza'),
    (-43.2106018066406, -22.9515964040996, 'Christ the Redeemer'),
    (12.4923133850098, 41.8902979498154, 'Colosseum'),
    (116.570434570312, 40.4312689704475, 'Great Wall of China'),
    (-72.5633239746094, -13.1757712244234, 'Machu Picchu'),
    (35.4788017272949, 30.3220632175406, 'Petra'),
    (31.1342239379883, 29.9790259829611, 'The Great Pyramid of Giza'),
]

ac = AmigoCloud(token=TOKEN)


def track_job(job_id):
    """
    Tracks the end of a job.

    :returns whether or not the job succeeded
    """

    wait_time = 0.1
    while True:
        time.sleep(wait_time)
        result = ac.get('/me/jobs/%s' % job_id)
        if result['status'] not in ('STARTED', 'PENDING'):
            return result['status'] == 'SUCCESS'
        wait_time *= 2


def create_dataset_with_gallery():
    """
    Creates a dataset with name, location and photo gallery

    :returns Dataset and Gallery URLs
    """
    dataset_schema = [{'name': 'name',
                       'nullable': False,
                       'type': 'string'},
                      {'name': 'location',
                       'geometry_type': 'POINT',
                       'nullable': False,
                       'type': 'geometry'}]

    result = ac.post(PROJECT_URL + '/datasets/create', {
        'name': '7 Wonders',
        'schema': json.dumps(dataset_schema)
    })
    if not track_job(result['job']):
        raise Exception('Failed to create dataset')

    dataset_url = result['url']

    # A gallery is a table related to the dataset
    result = ac.post(dataset_url + '/related_tables', {
        'name': 'photos',
        'type': 'gallery'
    })
    return dataset_url, result['url']


def insert_records(dataset_url, gallery_url):
    """
    Inserts the data for each wonder along with a picture

    :returns list of amigo_ids of the records
    """

    dataset_id = dataset_url.rsplit('/', 1)[1]
    photos = ZipFile('7wonders.zip')
    amigo_ids = []

    for i, wonder in enumerate(WONDERS):
        amigo_id = uuid.uuid4().hex
        amigo_ids.append(amigo_id)
        change = {
            'action': 'INSERT',
            'type': 'DML',
            'data': [
                {
                    'new': {
                        'location': 'SRID=4326;POINT(%.12f %.12f)' %
                                    (wonder[0], wonder[1]),
                        'name': wonder[2]
                    },
                    'amigo_id': amigo_id
                }
            ],
            'entity': 'dataset_%s' % dataset_id
        }
        # Inserting data
        result = ac.post(dataset_url + '/submit_change', {
            'change': json.dumps(change)
        })
        if not track_job(result['job']):
            raise Exception('Failed to insert data')

        photo = BytesIO(photos.read('%d.jpg' % (i + 1)))
        # Uploading picture
        ac.upload_file(gallery_url + '/upload',
                       gallery_url + '/chunked_upload', file_obj=photo,
                       extra_data={
                           'source_amigo_id': amigo_id,
                           'filename': 'photo.jpg'})
    return amigo_ids


def get_gallery_photo_urls(amigo_ids, gallery_url):
    for amigo_id in amigo_ids:
        # getting information of all photos related to a record
        result = ac.get(gallery_url + '/entries?source_amigo_id=' + amigo_id)
        for record in result['data']:
            url = '%s/files/%s/%s/%s' % (
                gallery_url, record['source_amigo_id'], record['amigo_id'],
                record['filename']
            )
            result = ac.get(url, raw=True)
            img = Image.open(BytesIO(result))
            img.show()


def main():
    urls = create_dataset_with_gallery()
    amigo_ids = insert_records(*urls)
    get_gallery_photo_urls(amigo_ids, urls[1])


if __name__ == '__main__':
    main()
