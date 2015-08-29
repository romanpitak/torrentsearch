# -*- coding: utf-8 -*-

import pprint

class BaseTorrent:

    def __init__(self):
        self.__dict__['data'] = {
            'name': '',
            'path': [],
            'detail': False,
            'leechers': None,
            'session': None,
        }

    def _pull_detail(self):
        pass

    def __getattr__(self, item):
        if item not in self.__dict__['data'] and 'detail_url' != item and not self.detail:
            self.detail = True
            self._pull_detail()
        if item in self.__dict__['data']:
            return self.__dict__['data'][item]
        raise AttributeError('\'Torrent\' object has no attribute \'{}\''.format(item))

    def __setattr__(self, key, value):
        self.__dict__['data'][key] = value

    def __str__(self):
        return pprint.pformat(self.__dict__['data'])
        # return str(self.__dict__['data'])

    def __eq__(self, other):
        return self.hash == other.hash

    def __ne__(self, other):
        return self.hash != other.hash

    def __hash__(self):
        return hash(self.hash)
