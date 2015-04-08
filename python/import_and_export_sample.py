import json
import re
import time

from amigocloud import AmigoCloud


amigocloud = AmigoCloud(token='<your_token>')

PROJECT_OWNER = 1
PROJECT_ID = 123
FILE_PATH = 'sf_neighborhoods.zip'
DATASET_ID = None  # TBD

# Upload shapefile
response = amigocloud.upload_datafile(PROJECT_OWNER, PROJECT_ID, FILE_PATH)
print "Uploaded file '%s'" % FILE_PATH

# Wait until async job is done
job_url = 'me/jobs/%s' % response['job']
while True:
    response = amigocloud.get(job_url)
    if response['status'] not in ('STARTED', 'PENDING'):
        break
    time.sleep(0.5)  # Wait 500ms and retry
print "File '%s' finished processing" % FILE_PATH

# Save new dataset ID
DATASET_ID = response['extra']['dataset_ids'][0]
print 'Dataset with ID=%d was created' % DATASET_ID

# Get dataset data
dataset_data = amigocloud.get('users/%s/projects/%s/datasets/%s'
                              % (PROJECT_OWNER, PROJECT_ID, DATASET_ID))

# Add new column called "area"
add_column = {
    "type": "DDL",
    "entity": dataset_data['table_name'],
    "action": "ADD COLUMN",
    "data": [{
        "new": {
            "name": "area",
            "type": "float",
            "nullable": False,
            "default": 0.0
        }
    }]
}
response = amigocloud.post(dataset_data['submit_change'],
                           {'change': json.dumps(add_column)})

# Wait until async job is done
job_url = 'me/jobs/%s' % response['job']
while True:
    response = amigocloud.get(job_url)
    if response['status'] not in ('STARTED', 'PENDING'):
        break
    time.sleep(0.5)  # Wait 500ms and retry
print 'Column "area" was added to dataset'

# Fill new column "area" with the area of the geometry using the SQL API
sql_api_url = 'users/%s/projects/%s/sql' % (PROJECT_OWNER, PROJECT_ID)
query = 'UPDATE "%s" SET area = ST_AREA("%s"::geography)' % (
    dataset_data['table_name'], dataset_data['geometry_column']
)
amigocloud.post(sql_api_url, {'query': query})

# Request export
response = amigocloud.post(dataset_data['export'], {'format': 'KML'})
print 'Requested export'

# Wait until async job is done
job_url = 'me/jobs/%s' % response['job']
while True:
    response = amigocloud.get(job_url)
    if response['status'] not in ('STARTED', 'PENDING'):
        break
    time.sleep(0.5)  # Wait 500ms and retry
print 'Export file is ready'

response = amigocloud.get(response['extra']['link'], stream=True)
match = re.search('filename="([\w.]+)"',
                  response.headers['content-disposition'])
with open(match.group(1), 'wb') as download_file:
    for chunk in response.iter_content(1000000):  # Chunks of 1MB
        download_file.write(chunk)
