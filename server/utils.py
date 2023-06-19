import os
import sys
import configparser


def msg(message, msg_type='info'):
    # print message to stdout
    # this is hacky... we should be using a logger
    if msg_type == 'info':
        print(f'[+] {message}')
    elif msg_type == 'status':
        print(f'[*] {message}')
    elif msg_type == 'warning':
        print(f'[warn] {message}')
    elif msg_type == 'error':
        print(f'[err] {message}')


class Config:
    def __init__(self, config_file):
        # check if config file exists
        self.config_file = config_file
        if not os.path.exists(self.config_file):
            msg(f'config file not found: {self.config_file}', 'error')
            sys.exit(1)

        # load config file
        msg(f'loading config file: {self.config_file}', 'status')
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get(self, section, key):
        # get config option by section and key name
        answer = None

        try:
            answer = self.config.get(section, key)
        except:
            msg(f'config file missing option: {section} {key}', 'error')

        return answer
