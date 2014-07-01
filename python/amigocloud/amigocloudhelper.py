import json
import requests

BASE_URL = 'https://www.amigocloud.com/api/v1'


class AmigoCloudHelper(object):

    def __init__(self, email=None, password=None, base_url=BASE_URL):

        self.base_url = base_url
        self.csrftoken = ''
        self.sessionid = ''

        if email and password:
            self.login(email, password)

    def build_url(self, url):

        if url.startswith('http'):
            # User already specified the full url
            return url
        # User wants to use the base_url
        if url.startswith('/'):
            return self.base_url + url
        return self.base_url + '/' + url

    def login(self, email, password):
        """
        Logs in the user and keeps the session ID.
        """

        login_url = self.build_url('login')

        response = requests.post(login_url, {'email': email,
                                             'password': password})
        response.raise_for_status()  # Raise exception if something failed

        self.csrftoken = response.cookies['csrftoken']
        self.sessionid = response.cookies['sessionid']

    def get(self, url, raw=False, **get_params):
        """
        GET request to AmigoCloud endpoint.
        """

        full_url = self.build_url(url)
        cookies = {'sessionid': self.sessionid}

        response = requests.get(full_url, params=get_params, cookies=cookies)
        response.raise_for_status()  # Raise exception if something failed

        if raw:
            return response.content
        return json.loads(response.text)

    def _secure_request(self, url, method, raw=False, **req_params):

        full_url = self.build_url(url)
        headers = {'referer': self.base_url, 'x-csrftoken': self.csrftoken,
                   'content-type': 'application/json'}
        cookies = {'sessionid': self.sessionid, 'csrftoken': self.csrftoken}

        method = getattr(requests, method, None)
        response = method(full_url, data=json.dumps(req_params),
                          headers=headers, cookies=cookies)
        response.raise_for_status()  # Raise exception if something failed

        if raw:
            return response.content
        return json.loads(response.text)

    def post(self, url, raw=False, **post_params):
        """
        POST request to AmigoCloud endpoint.
        """

        return self._secure_request(url, 'post', raw=raw, **post_params)

    def put(self, url, raw=False, **put_params):
        """
        PUT request to AmigoCloud endpoint.
        """

        return self._secure_request(url, 'put', raw=raw, **put_params)

    def patch(self, url, raw=False, **patch_params):
        """
        POST request to AmigoCloud endpoint.
        """

        return self._secure_request(url, 'patch', raw=raw, **patch_params)
