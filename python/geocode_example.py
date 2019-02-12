from amigocloud import AmigoCloud

# Use amigocloud version 1.0.5 or higher to login with tokens
# This will raise an AmigoCloudError if the token is invalid or has expired
ac = AmigoCloud(token='<your_token>')

# Geocoder parameters
# Address to geocode. For example, AmigoCloud address.
ADDRESS = '300 3rd Street, San Francisco, United States'
# Values to filter the geocoding response.
COMPONENTS = 'country:US'
# More information:
# https://developers.google.com/maps/documentation/geocoding/intro#ComponentFiltering

# Geocoder API endpoint (Version 2)
geocoder_url = 'https://app.amigocloud.com/api/v2/me/geocoder/search'
geocoder_params = {'input': ADDRESS, 'components': COMPONENTS}

response = ac.get(geocoder_url, params=geocoder_params)

coordinates = {}
# Status 'OK' indicates that no errors occurred; the address was successfully
# parsed and at least one geocode was returned.
if response['status'] == 200:
    coordinates['lat'] = response['results'][0]['location']['lat']
    coordinates['lng'] = response['results'][0]['location']['lng']

# We can use these coordinates to find intersects in polygons
PROJECT_ID = 1234
DATASET_ID = 5678
POLYGON_GEOMETRY_FIELD_NAME = 'polygon'
sql_url = 'projects/{project_id}/sql'.format(project_id=PROJECT_ID)
query = """
        SELECT * 
        FROM dataset_{dataset_id} 
        WHERE ST_Intersects({geometry_field}, 
        ST_PointFromText('POINT({coordinate_lng} {coordinate_lat})', 4326))
        """.format(dataset_id=DATASET_ID,
                   geometry_field=POLYGON_GEOMETRY_FIELD_NAME,
                   coordinate_lng=str(coordinates['lng']),
                   coordinate_lat=str(coordinates['lat']))
