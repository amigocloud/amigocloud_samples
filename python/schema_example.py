import json
from pprint import pprint
from requests.exceptions import HTTPError
from amigocloud import AmigoCloud

try:
    ac = AmigoCloud(email='<my_email>', password='<my_password>')
except HTTPError:
    print 'Wrong credentials!'
    import sys
    sys.exit(1)

# For examples of how to get these values, see simple_example2.py
PROJECT_OWNER = 1
PROJECT_ID = 573
DATASET_ID = 3626

# Get dataset information
dataset_url = '/users/{user_id}/projects/{project_id}/datasets/{dataset_id}'
dataset = ac.get(dataset_url.format(user_id=PROJECT_OWNER,
                                    project_id=PROJECT_ID,
                                    dataset_id=DATASET_ID))
# Store the table name
table_name = dataset['table_name']

# Request and store master state
response = ac.get(dataset['master'])
master = response['master']

print 'The table name we have to use in SQL queries is', table_name
print 'The master state of the dataset is', master

# Build "ADD COLUMN schema change:
add_column = {
    "type": "DDL",
    "entity": table_name,
    "action": "ADD COLUMN",
    "parent": master,
    "data": [
        {
            "new": {
                "name": "log_level",
                "type": "integer",
                "nullable": False,
                "default": 2
            }
        }
    ]
}

# Add 'log_level' column to the dataset
response = ac.post(dataset['submit_change'], change=json.dumps(add_column))

response = ac.get(dataset['schema'])

print 'Current schema of the dataset:'
pprint(response)

# Request and store new master state
response = ac.get(dataset['master'])
new_master = response['master']

# Build "ALTER COLUMN schema change:
alter_column = {
    "type": "DDL",
    "entity": table_name,
    "action": "ALTER COLUMN",
    "parent": new_master,
    "data": [
        {
            "new": {
                "name": "log_level",
                "type": "integer",
                "nullable": False,
                "default": 2,
                "choices": [
                    {"code": 1, "value": "debug"},
                    {"code": 2, "value": "info"},
                    {"code": 3, "value": "warning"},
                    {"code": 4, "value": "error"},
                    {"code": 5, "value": "critical"}
                ]
            }
        }
    ]
}

# Add choices or "picklist" to column 'log_level' (we need to define the entire
# column)
response = ac.post(dataset['submit_change'], change=json.dumps(alter_column))

response = ac.get(dataset['schema'])

print 'Current schema of the dataset:'
pprint(response)

# Request and store new master state
response = ac.get(dataset['master'])
new_master = response['master']

# Build "DROP COLUMN schema change:
drop_column = {
    "type": "DDL",
    "entity": table_name,
    "action": "DROP COLUMN",
    "parent": new_master,
    "data": [
        {
            "old": {
                "name": "log_level"
            }
        }
    ]
}

response = ac.post(dataset['submit_change'], change=json.dumps(drop_column))

response = ac.get(dataset['schema'])

print 'Current schema of the dataset:'
pprint(response)
