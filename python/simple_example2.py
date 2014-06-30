import urllib2
from pprint import pprint
from amigocloud import AmigoCloud

try:
    ac = AmigoCloud(username='<my_email>', password='<my_password>')
except urllib2.HTTPError, e:
    print e.code, e.msg, "Check credentials"

# Get User ID
user_data = ac.get('/me')
print 'My user_id is', user_data['id']

# Get list of projects
projects = ac.get('/users/{user_id}/projects'.format(user_id=user_data['id']))
print 'These are my projects:'
pprint(projects) # pretty print them since this could be very long

# Get all datasets of the first project
project = projects['results'][0]

datasets = ac.get('/users/{user_id}/projects/{project_id}/datasets'.format(
                        user_id=user_data['id'], project_id=project['id']))
print 'These are all the datasets of my first project:'
pprint(datasets)

# Get first dataset in that project
dataset = ac.get('/users/{user_id}/projects/{project_id}/datasets/{dataset_id}'.format(
            user_id=user_data['id'], project_id=project['id'], dataset_id = datasets['results'][0]['id']))

print 'This is the bounding of the first project:'
print(dataset['boundingbox'])

print 'This is a url to preview the dataset as html'
print(dataset['preview'])

print 'Saving a rendered png of that dataset to disk'
print dataset['preview_image']

# get the preview image, except that since it is not json, we have to fetch the raw urllib2 response
# and make sure that we close it after we are done
response = ac.get_raw(dataset['preview_image'])

output_file = open('output_file.png', 'w')
output_file.write(response.read())

response.close()
output_file.close()
