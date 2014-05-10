import sys
import json
import urllib
import urllib2
import contextlib


def login(url, email, password):
    """
    Logins the user and then returns the personal info of the user's
    account and the session and crsf token, needed for making new
    requests to the server.
    """

    cookies = urllib2.HTTPCookieProcessor()
    opener = urllib2.build_opener(cookies)

    # A false request to get the CSRF token
    try:
        opener.open(url, urllib.urlencode({}))
    except urllib2.HTTPError, e:
        pass

    # Retrieve the CSRF token to make the login POST
    try:
        csrf_token = [x.value for x in cookies.cookiejar
                      if x.name == 'csrftoken'][0]
    except IndexError:
        return False, "no csrftoken"

    params = dict(email=email, password=password,
                  csrfmiddlewaretoken=csrf_token)
    encoded_params = urllib.urlencode(params)

    try:
        with contextlib.closing(opener.open(url, encoded_params)) as f:
            my_personal_info = json.loads(f.read())
            cookies_headers = f.info().getheader('Set-Cookie')
            csrf_header = \
                cookies_headers.split('csrftoken=')[1].split(';', 1)[0]
            session_header = \
                cookies_headers.split('sessionid=')[1].split(';', 1)[0]
    except urllib2.HTTPError, e:
        print e.code, e.msg, "Maybe your email and/or password are wrong."
        return None

    return dict(my_personal_info=my_personal_info, csrf_header=csrf_header,
                session_header=session_header)


def fetch_url(context, url):
    """
    Opens any url from the api to which the LOGGED IN user has permission
    and returns the data JSON object as a dict.
    """

    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', 'csrftoken=' + context['csrf_header'] +
                              '; sessionid=' + context['session_header']))
    try:
        with contextlib.closing(opener.open(url)) as response:
            return json.loads(response.read())
    except urllib2.HTTPError, e:
        print e.code, e.msg
        return None
