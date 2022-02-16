import base64, json, websocket, time, threading, re, httpx
from urllib.request import Request, urlopen

config = json.load(open('./config.json'))

class Payload:
    @staticmethod
    def simple_register(username: str, fingerprint: str, captcha_key: str) -> dict:
        return {
            "consent": True,
            "fingerprint": fingerprint,
            "username": username,
            "captcha_key": captcha_key,
        } if config['invite_code'] != '' else {
            "consent": True,
            "fingerprint": fingerprint,
            "username": username,
            "captcha_key": captcha_key,
            "gift_code_sku_id": None,
            "invite": config['invite_code']
        }

class DiscordApi:
    @staticmethod
    def get_build_number() -> str:
        asset = re.compile(r'([a-zA-z0-9]+)\.js', re.I).findall((urlopen(Request(f'https://discord.com/app', headers={'User-Agent': 'Mozilla/5.0'})).read()).decode('utf-8'))[-1]
        fr = (urlopen(Request(f'https://discord.com/assets/{asset}.js', headers={'User-Agent': 'Mozilla/5.0'})).read()).decode('utf-8')
        return str(re.compile('Build Number: [0-9]+, Version Hash: [A-Za-z0-9]+').findall(fr)[0].replace(' ', '').split(',')[0].split(':')[-1]).replace(' ', '')

    @staticmethod
    def get_trackers(build_num: str, xtrack: bool, encoded: bool = True) -> [str, dict]:
        payload = {
            "os": "Windows",
            "browser": "Chrome",
            "device": "",
            "system_locale": "fr-FR",
            "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
            "browser_version": "98.0.4758.102",
            "os_version": "10",
            "referrer": "",
            "referring_domain": "",
            "referrer_current": "",
            "referring_domain_current": "",
            "release_channel": "stable",
            "client_build_number": build_num if xtrack else 9999,
            "client_event_source": None
        }

        return base64.b64encode(json.dumps(payload, separators=(',', ':')).encode()).decode() if encoded else payload

    @staticmethod
    def check_flag(client: httpx.Client, token: str) -> dict:
        flag_found = {}
        flag_list = {
            0: 'User is not flagged',
            1048576: 'User is marked as a spammer.',
            2199023255552: 'User is currently temporarily or permanently disabled.'
        }

        client.headers['authorization'] = token
        response = client.get('https://discord.com/api/v9/users/@me').json()

        if client.get('https://discord.com/api/v9/users/@me/library').status_code != 200:
            flag_found['locked'] = True
        else:
            flag_found['locked'] = False

        for flag_id, flag_text in flag_list.items():
            if response['flags'] == flag_id or response['public_flags'] == flag_id:
                flag_found[flag_id] = flag_text

        return flag_found

    @staticmethod
    def register(client: httpx.Client, captcha_key: str, build_num: str) -> str:
        payload = Payload.simple_register('UwU1337feefef', client.headers['x-fingerprint'], captcha_key)

        client.headers['x-track' if config["invite_code"] == '' else 'x-super-properties'] = DiscordApi.get_trackers(0 if config["invite_code"] == '' else build_num, True if config["invite_code"] == '' else False)
        client.headers['content-length'] = str(len(json.dumps(payload)))
        client.headers['referer'] = f'https://discord.com/invite/{config["invite_code"]}' if config["invite_code"] != '' else ''

        if config['invite_code'] != '':
            client.headers['X-Debug-Options'] = 'bugReporterEnabled'
            client.headers['X-Discord-Locale'] = 'fr'

        response = client.post('https://discord.com/api/v9/auth/register', json=payload).json()
        client.headers.pop('content-length')

        if config["invite_code"] == '':
            client.headers.pop('x-track')

        return response

class DiscordWs(threading.Thread):
    def __init__(self, acc_token: str) -> None:
        self.token = acc_token
        self.running = True
        self.ws = websocket.WebSocket()
        threading.Thread.__init__(self)

    def send_payload(self, payload: dict) -> None:
        self.ws.send(json.dumps(payload))

    def recieve(self) -> dict:
        data = self.ws.recv()

        if data:
            return json.loads(data)

    def heartbeat(self, interval: float):
        while self.running:
            time.sleep(interval)
            self.send_payload({
                'op': 1,
                'd': None
            })

    def login(self):
        self.ws.connect('wss://gateway.discord.gg/?encoding=json')
        interval = self.recieve()['d']['heartbeat_interval'] / 1000
        threading.Thread(target=self.heartbeat, args=(interval,)).start()

    def online(self):
        self.send_payload({
            "op": 2,
            "d": {
                "token": self.token,
                "capabilities": 253,
                "properties": DiscordApi.get_super_properties(False),
                "presence": {
                    "status": "online",
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            }
        })

        time.sleep(6)

        self.send_payload({
            "op": 3,
            "d": {
                "status": "idle",
                "since": 0,
                "activities": [
                    {
                        "name": "Custom Status",
                        "type": 4,
                        "state": "IOGen.",
                        "emoji": None
                    }
                ],
                "afk": False
            }
        })

    def run(self):
        self.login()
        self.online()
        time.sleep(30)
        self.running = False
