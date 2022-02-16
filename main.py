# Temp main to people who whant to work on it

from modules.session import HttpSession
from modules.discord import DiscordApi
from modules.captcha import CaptchaSolver
from modules.console import Console

import random, threading, httpx, time, json

num = '115008' #DiscordApi.get_build_number() Yes because i don't whant to wait 20min to get this shit after each debug
print(num)
proxies = open('./proxies.txt', 'r+').read().splitlines()
config = json.load(open('./config.json'))

def worker():
    try:
        pp = None

        while pp == None:
            try:
                prox = 'http://' + random.choice(proxies)
                httpx.get('https://google.com', proxies=prox, timeout=5)
                pp = prox
            except:
                pass
        print(pp)

        session = HttpSession(pp)
        api = DiscordApi()

        c = CaptchaSolver().get_captcha_key(pp.split('://')[1], pp.split('://')[1])
        print(c)

        session.get_cookies()
        token = api.register(session.http_client, c, num)
        print(token)

        if 'token' in str(token):
            print(DiscordApi.check_flag(session.http_client, token['token']))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    threading.Thread(target=Console.key_bind_thread()).start()
    threading.Thread(target=Console.title_thread()).start()
    Console.print_logo()

    while True:
        while threading.active_count() >= config['threads']:
            time.sleep(1)
        threading.Thread(target=worker).start()