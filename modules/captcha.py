import json, time, httpx

config = json.load(open('./config.json'))

class CaptchaSolver:
    @staticmethod
    def get_captcha_key_by_hand() -> str:
        return input('Captcha-key: ')

    @staticmethod
    def get_captcha_key(static_proxy: str, proxy: str, site_key: str = '4c672d35-0701-42b2-88c3-78380b0db560') -> str:

        task_payload = {
            'clientKey': config['captcha_key'],
            'task': {
                'userAgent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.1012 Chrome/91.0.4472.164 Electron/13.6.6 Safari/537.36',
                'websiteKey': site_key,
                'websiteURL': 'https://ptb.discord.com',
                'type': 'HCaptchaTask',

                'proxyPassword': static_proxy.split('@')[0].split(':')[1],
                'proxyAddress': static_proxy.split('@')[1].split(':')[0],
                'proxyLogin': static_proxy.split('@')[0].split(':')[0],
                'proxyPort': static_proxy.split('@')[1].split(':')[1],
                'proxyType': 'http',
            }
        }
        key = None

        with httpx.Client(proxies=f'http://{proxy}',
                          headers={'content-type': 'application/json', 'accept': 'application/json'},
                          timeout=30) as client:
            try:
                task_id = client.post(f'https://api.{config["captcha_api"]}/createTask', json=task_payload).json()[
                    'taskId']

                get_task_payload = {
                    'clientKey': config['captcha_key'],
                    'taskId': task_id
                }

                while key is None:
                    try:
                        response = client.post(f'https://api.{config["captcha_api"]}/getTaskResult',
                                               json=get_task_payload,
                                               timeout=30).json()

                        if 'ERROR_PROXY_CONNECT_REFUSED' in str(response):
                            return 'ERROR'

                        if 'ERROR' in str(response):
                            return 'ERROR'

                        if response['status'] == 'ready':
                            key = response['solution']['gRecaptchaResponse']
                        else:
                            time.sleep(3)
                    except Exception as e:

                        if 'ERROR_PROXY_CONNECT_REFUSED' in str(e):
                            key = 'ERROR'
                        else:
                            pass
                return key

            except Exception as e:
                return e
