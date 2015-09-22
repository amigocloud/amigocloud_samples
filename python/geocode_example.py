# requires: pygeocoder>=1.2.5

from amigocloud import AmigoCloud
from pygeocoder import Geocoder

# Use amigocloud version 1.0.5 or higher to login with tokens
# This will raise an AmigoCloudError if the token is invalid or has expired
ac = AmigoCloud(token='<your_token>')

# For examples of how to get these values, see simple_example2.py
PROJECT_OWNER = 1
PROJECT_ID = 2
DATASET_ID = 3

# Get dataset information
dataset_url = '/users/{user_id}/projects/{project_id}/datasets/{dataset_id}'
dataset = ac.get(dataset_url.format(user_id=PROJECT_OWNER,
                                    project_id=PROJECT_ID,
                                    dataset_id=DATASET_ID))
table_name = dataset['table_name']

# SQL API endpont
sql_url = '/users/{user_id}/projects/{project_id}/sql'.format(
    user_id=PROJECT_OWNER, project_id=PROJECT_ID
)

# Get all records (fetching 100 on each request), until all rows are fetched
select_query = 'SELECT * FROM {table}'.format(table=table_name)
offset = 0
limit = 100
counter = 1
total_rows = dataset['feature_count']

# Update query
update_query = (
    "UPDATE {table_name} SET "
    "(location, latitude, longitude) = "
    "(ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326), {lat}, {lon}) "
    "WHERE amigo_id = '{amigo_id}'"
)

while True:
    # Fetch the next 100 records
    result = ac.get(sql_url, {'query': select_query,
                              'limit': limit, 'offset': offset})

    for row in result['data']:
        # Join street_address + city + state
        address = [row['street_address'], row['city'], row['state']]
        address_str = ' '.join(elem for elem in address if elem)

        # Geocode the address (get coordinates)
        print '[%s/%s] Geocoding "%s" ...' % (counter, total_rows, address_str)
        geo = Geocoder.geocode(address_str)

        # Update the row, saving the lat, long and geometry in the respective
        # columns (the dataset must already have these columns)
        kwargs = {'table_name': table_name, 'amigo_id': row['amigo_id'],
                  'lat': geo.coordinates[0], 'lon': geo.coordinates[1]}
        ac.post(sql_url, {'query': update_query.format(**kwargs)})

        counter += 1

    if len(result['data']) < limit:
        break
    offset += limit
