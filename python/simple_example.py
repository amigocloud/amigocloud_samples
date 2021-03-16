from amigocloud import AmigoCloud

# Use amigocloud version 1.0.5 or higher to login with tokens
# This will raise an AmigoCloudError if the token is invalid or has expired
ac = AmigoCloud(token='<your_token>')

# Print information about my account https://app.amigocloud.com/api/v1/me
print ac.get('me')
