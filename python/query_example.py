import urllib2
from pprint import pprint
from amigocloud import AmigoCloud

# for examples of how to get these values, see simple_example2.py
PROJECT_OWNER = '1'
PROJECT_ID = '573'
DATASET_ID = '3626'

try:
    ac = AmigoCloud(username='<my_username>', password='<my_password>')
except urllib2.HTTPError, e:
    print e.code, e.msg, "Check credentials"


# Get dataset information
dataset = ac.get('/users/{user_id}/projects/{project_id}/datasets/{dataset_id}'.format(
                        user_id=PROJECT_OWNER, project_id=PROJECT_ID, dataset_id=DATASET_ID))

print 'The table name we have to use in SQL queries is ' + dataset['table_name']

# AmigoCloud supports SQL operators of PostgreSQL and PostGIS. Please refer to
# http://postgis.net/documentation/ and http://postgis.net/docs/manual-2.1/reference.html
# for more information

# fetch records
sql = 'SELECT * FROM {table}'.format(table=dataset['table_name'])
query_result = ac.get('/users/{user_id}/projects/{project_id}/sql?query={sql}'.format(
                        user_id=PROJECT_OWNER, project_id=PROJECT_ID, sql=urllib2.quote(sql)))

print 'The schema of the result is:'
pprint(query_result['columns'])

print 'Even though the query returns ' + str(query_result['count']) + ', they are paginated.'
print 'This batch has ' + str(len(query_result['data'])) + ' records.'

# fetch all records and also check that the table has not changed while paginating.
