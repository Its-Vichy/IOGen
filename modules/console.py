from colorama import Fore, init;init()
import os, threading, time, json, keyboard

config = json.load(open('./config.json'))
lock = threading.Lock()

class Console:
    _generated, _verified, _locked, _proxy_err, _cap_worker, _mail_worker = 0, 0, 0, 0, 0, 0

    @staticmethod
    def debug(content: str):
        if config['debug']:
            lock.acquire()
            print(f'{Fore.LIGHTMAGENTA_EX}[DEBUG] {content}{Fore.RESET}')
            lock.release()

    @staticmethod
    def printf(content: str):
        lock.acquire()
        print(content.replace('[+]', f'[{Fore.LIGHTGREEN_EX}+{Fore.RESET}]').replace('[*]',
                                                                                     f'[{Fore.LIGHTYELLOW_EX}*{Fore.RESET}]').replace(
            '[>]', f'[{Fore.CYAN}>{Fore.RESET}]').replace('[-]', f'[{Fore.RED}-{Fore.RESET}]'))
        lock.release()

    @staticmethod
    def title_thread():
        start_time = time.time()

        while True:
            time.sleep(1)
            work_token_min = round(Console._generated / ((time.time() - start_time) / 60))
            all_token_min = round(Console._generated + Console._locked / ((time.time() - start_time) / 60))
            os.system(
                f'title [0xGen - 0xVichy#1234 - Private] Generated: {Console._generated} - Verified: {Console._verified} - Locked: {Console._locked} - ProxyErr: {Console._proxy_err} | Workers: [Captcha: {Console._cap_worker} Verification: {Console._mail_worker} Total: {config["threads"]}] | W.T/M: {work_token_min} - Ttl.T/M: {all_token_min} | Debug: {config["debug"]}'.replace(
                    '|', '^|'))

    @staticmethod
    def key_bind_thread():
        while True:
            time.sleep(0.2)
            if keyboard.is_pressed('up'):
                config['threads'] += 1

            if keyboard.is_pressed('down'):
                config['threads'] -= 1

            if keyboard.is_pressed('left'):
                config['debug'] = True

            if keyboard.is_pressed('right'):
                config['debug'] = False

            if config['threads'] < 0:
                config['threads'] = 0

    @staticmethod
    def print_logo():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'''
{Fore.CYAN}  ___ ___   {Fore.LIGHTWHITE_EX}____            
{Fore.CYAN} |_ _/ _ \\ {Fore.LIGHTWHITE_EX}/ ___| ___ _ __  
{Fore.CYAN}  | | | | | {Fore.LIGHTWHITE_EX}|  _ / _ \\ '_ \\ 
{Fore.CYAN}  | | |_| | {Fore.LIGHTWHITE_EX}|_| |  __/ | | |  {Fore.CYAN}github.com/its-vichy
{Fore.CYAN} |___\\___/ {Fore.LIGHTWHITE_EX}\\____|\\___|_| |_|
        ''')
