from requests.exceptions import HTTPError
from amigocloud import AmigoCloud

try:
    ac = AmigoCloud(email='<my_email>', password='<my_password>')
except HTTPError:
    print 'Wrong credentials!'
    import sys
    sys.exit(1)

# Print information about my account https://www.amigocloud.com/api/v1/me
print ac.get('me')
