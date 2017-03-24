from amigocloud import AmigoCloud

# Use amigocloud version 1.0.5 or higher to login with tokens
# This will raise an AmigoCloudError if the token is invalid or has expired
ac = AmigoCloud(token='<token>')

query = ({
        "author": "",
        "extra": "",
        "layer_name": "0",
        "name": "My first baselayer",
        "public_tiles": False,
        "transparency": False,
        "url": "<baselayer URL>",
        "zoom_level_max": 20,
        "zoom_level_min": 0
        })

sql_url='<AmigoCloud baselater API URL>'

response = ac.post(url=sql_url, data=query, content_type="application/json")

print 'Response:', response

