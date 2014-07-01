from pprint import pprint
from requests.exceptions import HTTPError
from amigocloud import AmigoCloud

try:
    ac = AmigoCloud(email='<my_email>', password='<my_password>')
except HTTPError:
    print 'Wrong credentials!'
    import sys
    sys.exit(1)

# For examples of how to get these values, see simple_example2.p
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

print 'The table name we have to use in SQL queries is', table_name
print 'The table has', dataset['feature_count'], 'rows'

# AmigoCloud supports SQL operators of PostgreSQL and PostGIS. For more
# information please refer to:
# http://postgis.net/documentation/ and
# http://postgis.net/docs/manual-2.1/reference.html

sql_url = '/users/{user_id}/projects/{project_id}/sql'.format(
    user_id=PROJECT_OWNER, project_id=PROJECT_ID
)

# Get all records (fetching 100 on each request), until all rows are fetched
query = 'SELECT * FROM {table}'.format(table=table_name)
total_rows = dataset['feature_count']
offset = 0
limit = 100
rows = []

# To ensure atomicity between requests we can pass the master state and
# dataset_id as parameters
response = ac.get(dataset['master'])
master = response['master']

while len(rows) < total_rows:
    response = ac.get(sql_url, query=query, offset=offset, limit=limit,
                      state=master, dataset_id=DATASET_ID)

    if not offset:  # i.e. If first request
        print 'The schema of the result is:'
        pprint(response['columns'])

    fetched_rows = len(response['data'])
    offset += fetched_rows
    rows += response['data']
    print 'Fetched', fetched_rows, 'rows'

print 'These are all the rows:'
pprint(rows)

# Update records based on some condition
query = ("UPDATE {table} SET field1 = field1 + 1 "
         "WHERE amigo_id = 'abcd'".format(table=table_name))
response = ac.post(sql_url, query=query)

print 'Query:', response['query']
print 'This query updated', response['count'], 'row(s)'

# Delete records based on some condition
query = "DELETE FROM {table} WHERE amigo_id = 'abcd'".format(table=table_name)
response = ac.post(sql_url, query=query)

print 'Query:', response['query']
print 'This query deleted', response['count'], 'row(s)'

# Insert new record
query = ("INSERT INTO {table} (field1, field2) "
         "VALUES (123, 'Hello world!')".format(table=table_name))
response = ac.post(sql_url, query=query)

print 'Query:', response['query']
print 'This query inserted', response['count'], 'row(s)'
