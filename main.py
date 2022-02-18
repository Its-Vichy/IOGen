# Temp main to people who whant to work on it

from modules.session import HttpSession
from modules.discord import DiscordApi, DiscordWs
from modules.captcha import CaptchaSolver
from modules.console import Console

import random, threading, httpx, time, json, itertools

num = "115427" ##DiscordApi.get_build_number() #Yes because i don't whant to wait 20min to get this shit after each debug
print(num)
proxies = open('./proxies.txt', 'r+').read().splitlines() # itertools.cycle() / next(proxies) to made perfect rotation but i put random to debug
config = json.load(open('./config.json'))

def worker():
    try:
        pp = None

        while pp == None:
            try:
                prox = 'http://' + random.choice(proxies)
                httpx.get('https://google.com', proxies=prox, timeout=5)
                pp = prox
            except Exception as e:
                Console.debug('[-] Invalid proxy found')
                pass
        Console.debug('[*] Valid proxy found')

        session = HttpSession(pp)
        api = DiscordApi()

        c = CaptchaSolver().get_captcha_by_ai(pp.split('://')[1]) #get_captcha_key(pp.split('://')[1], pp.split('://')[1])

        if c == 'ERROR' or c is None:
            Console.debug(f'[-] Captcha proxy error')
            return

        Console.debug(f'[@] Captcha solved: {c[:20]}')

        session.get_cookies()
        token = api.register(session.http_client, c, num)
        Console.debug(f'[>] Generated token: {token}')

        if 'token' in str(token):
            DiscordWs(token).start()
            print(DiscordApi.check_flag(session.http_client, token['token']))
    except Exception as e:
        Console.debug(f'[-] Exception worker: {e}')

if __name__ == '__main__':
    Console.print_logo()

    threading.Thread(target=Console.key_bind_thread).start()
    threading.Thread(target=Console.title_thread).start()


    """
    Removed for debug dont start 3k thread loop.
    """
    """while True:
        while threading.active_count() >= config['threads']:
            time.sleep(1)"""

    for _ in range(20):
        threading.Thread(target=worker).start()