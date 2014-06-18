from amigocloud_helper import login, fetch_url

if __name__ == '__main__':
    login_url = 'https://www.amigocloud.com/api/v1/login/'
    email = 'account.email@amigocloud.com'
    password = 'accountpassword'

    # Logging in
    context = login(login_url, email, password)
    print context['my_personal_info']

    result = fetch_url(context,
                       "https://www.amigocloud.com/api/v1/users/3/projects/104")
    print result
