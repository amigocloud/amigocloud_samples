from amigocloud import AmigoCloud

# Use amigocloud version 1.0.5 or higher to login with tokens
# This will raise an AmigoCloudError if the token is invalid or has expired
ac = AmigoCloud(token='<your_token>')

# For examples of how to get these values, see simple_example2.py
PROJECT_ID = 1234
DATASET_ID = 5678

# Name of the fields that are going to be use in the geocoding.
# You can found them in the schema editor.
ADDRESS_FIELD_NAME = 'address'
GEOMETRY_FIELD_NAME = 'point'

# Dictionary to filter the geocoding response.
PARAMS = {'country': 'PE'}
# More information:
# https://developers.google.com/maps/documentation/geocoding/intro#ComponentFiltering

# Project and dataset ids must be strings
ac.geocode_addresses(str(PROJECT_ID), str(DATASET_ID),
                     ADDRESS_FIELD_NAME, GEOMETRY_FIELD_NAME, **PARAMS)
