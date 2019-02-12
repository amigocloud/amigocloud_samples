from pprint import pprint
from amigocloud import AmigoCloud

# Use amigocloud version 1.0.5 or higher to login with tokens
# This will raise an AmigoCloudError if the API token is invalid or has expired
ac = AmigoCloud(token='<your token>',
                use_websockets=False)

# For examples of how to get these values, see simple_example2.py
PROJECT_ID = 14098
DATASET_ID = 84746

#API endpoint
sql_url = 'projects/{project_id}/sql'.format(project_id=PROJECT_ID)

# find all rows that intersect the hard coded point
query = """
SELECT * 
FROM dataset_{dataset_id} 
WHERE ST_Intersects(wkb_geometry, ST_PointFromText('POINT(-117.150727812638 32.7068451387017)', 4326))
""".format(dataset_id = DATASET_ID)

response = ac.get(sql_url, {'query': query, 
                            'dataset_id': DATASET_ID})

# print schema of response
pprint(response['columns'])

# print row contents
pprint(response['data'])

