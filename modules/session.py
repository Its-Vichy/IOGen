from modules.cloudfare import Cloudfare
from modules.discord import DiscordApi
import httpx

class HttpSession:
    def __init__(self, proxy: str = None):
        self.base_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'accept-encoding': 'gzip, deflate, br',
            'content-type': 'application/json',
            'referer': 'https://discord.com/',
            'origin': 'https://discord.com',
            'sec-ch-ua-platform': 'Windows',
            'sec-fetch-site': 'same-origin',
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'accept': '*/*',
        }

        self.http_client = httpx.Client(proxies=proxy, headers=self.base_headers, timeout=30)

    def get_cookies(self):
        response = self.http_client.get('https://discordapp.com/api/v9/experiments')
        r, m = Cloudfare().Get_CFParams(self.http_client)

        __cf_bm = Cloudfare().Get_CfBm(self.http_client, r, m)
        __dcfduid = response.cookies.get('__dcfduid')
        __sdcfduid = response.cookies.get('__sdcfduid')

        cookies = httpx.Cookies()
        cookies.set('locale', 'fr', domain='discord.com')
        cookies.set('__cf_bm', __cf_bm, domain='.discord.com')
        cookies.set('__dcfduid', __dcfduid, domain='discord.com')
        cookies.set('__sdcfduid', __sdcfduid, domain='discord.com')
        self.http_client.cookies = cookies

        self.http_client.headers['x-fingerprint'] = response.json()['fingerprint']
        self.http_client.headers['cookie'] = f'__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}; locale=fr; __cf_bm={__cf_bm}'

        DiscordApi.submit_trackers(self.http_client)
