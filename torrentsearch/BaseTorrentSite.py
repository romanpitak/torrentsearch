# -*- coding: utf-8 -*-

import requests


class BaseTorrentSite:

    def __init__(self):
        self.session = requests.Session()
        pass
