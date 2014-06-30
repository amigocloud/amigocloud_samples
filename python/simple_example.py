from amigocloud import AmigoCloud

ac = AmigoCloud(username='<my_email>', password='<my_password>')

# print information about my account https://www.amigocloud.com/api/v1/me
print ac.get('/me')


