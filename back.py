
from ipwhois import IPWhois
import pandas as pd
import yaml
import json
import requests
import webbrowser

# main backend class containing all functions: ip whois lookup, data from chosen scam detection APIs
class Analyzer:
    def __init__(self):
        self.vpnapi_key = '9fab416322bb4c6aaadaa5b9e8caa0b7'

        self.load_config()

    def load_config(self):
        with open('config.yaml') as cfg:
            self.apis = yaml.safe_load(cfg)

    def add_api(self, name, api_link, api_key):
        self.apis[name] = (api_link, api_key)

    def save_apis(self):
        with open('config.yaml', 'w+') as cfg:
            yaml.dump(self.apis, cfg, default_flow_style=False, allow_unicode=True)

    def get_whois_info(self, ip):
        return pd.Series(IPWhois(ip))

    def get_vpnapi_info(self, ip):
        link = f'https://vpnapi.io/api/{ip}?key={self.vpnapi_key}'
        return json.loads(requests.get(link).text)


    @staticmethod
    def open_scamalytics_in_browser(ip):
        link = f'https://scamalytics.com/ip/{ip}'
        webbrowser.open(link)
