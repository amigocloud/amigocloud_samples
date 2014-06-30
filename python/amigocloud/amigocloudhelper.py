import json
import urllib
import urllib2
from contextlib import closing

BASE_URL = 'https://www.amigocloud.com/api/v1'

class AmigoCloudHelper:

    def __init__(self, username=None, password=None,
                 base_url=BASE_URL):

        self.base_url = base_url

        if not username is None and not password is None:
            self.login(username, password)

    def login(self, username, password):
        """
        Logs in the user using the CSRF token mechanism.
        """

        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)

        # Initial request to get the CSRF token
        try:
            opener.open(self.base_url + '/login', urllib.urlencode({}))
        except urllib2.HTTPError, e:
            pass

        # Retrieve the CSRF token to make the login POST
        try:
            csrf_token = [x.value for x in cookies.cookiejar
                          if x.name == 'csrftoken'][0]
        except IndexError:
            return False, "no csrftoken"

        params = dict(email=username, password=password,
                      csrfmiddlewaretoken=csrf_token)
        encoded_params = urllib.urlencode(params)

        try:
            with closing(opener.open(self.base_url + '/login', encoded_params)) as f:
                my_personal_info = json.loads(f.read())
                cookies_headers = f.info().getheader('Set-Cookie')
                csrf_header = \
                    cookies_headers.split('csrftoken=')[1].split(';', 1)[0]
                session_header = \
                    cookies_headers.split('sessionid=')[1].split(';', 1)[0]
        except urllib2.HTTPError, e:
            print e.code, e.msg, "Maybe your email and/or password are wrong."
            return None

        self.context = dict(my_personal_info=my_personal_info, csrf_header=csrf_header,
                            session_header=session_header, username = username)
        return

    def get_raw(self, endpoint):


        if endpoint[0:4] == 'http':
            # the user is specifying the full url
            url = endpoint
        elif endpoint[0] != '/':
            # the user wants to use the default base_url
            url = self.base_url + '/' + endpoint
        else:
            url = self.base_url + endpoint


        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'csrftoken=' + self.context['csrf_header'] +
                                  '; sessionid=' + self.context['session_header']))

        return opener.open(url)

    def get(self, endpoint):
        """
        Opens any url from the api to which the LOGGED IN user has permission
        and returns the data JSON object as a dict.
        """

        urllib2opener = self.get_raw(endpoint)
        with closing(urllib2opener) as response:
            return json.loads(response.read())
