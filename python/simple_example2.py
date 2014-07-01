from pprint import pprint
from requests.exceptions import HTTPError
from amigocloud import AmigoCloud

try:
    ac = AmigoCloud(email='<my_email>', password='<my_password>')
except HTTPError:
    print 'Wrong credentials!'
    import sys
    sys.exit(1)

# Get User ID
user_data = ac.get('me')
print 'My user ID is', user_data['id']

# Get list of projects
projects = ac.get(user_data['projects'])
print 'These are my projects:'
pprint(projects)  # pretty print them since this could be very long

# Get first project
project = projects['results'][0]
print 'Project ID is', project['id']

# Get all datasets of the first project
datasets = ac.get(project['datasets'])
print 'These are all the datasets of my first project:'
pprint(datasets)

# Get first dataset in that project
dataset = datasets['results'][0]
print 'Dataset ID is', dataset['id']

print 'This is the bounding of the first dataset:'
print(dataset['boundingbox'])

print 'This is a url to preview the dataset as html'
print(dataset['preview'])

print "Saving a rendered png of that dataset to disk (output_file.png)"
print dataset['preview_image']

# Get the preview image (response is not json, so we fetch raw response)
response = ac.get(dataset['preview_image'], raw=True)

with open('output_file.png', 'wb') as output_file:
    output_file.write(response)
