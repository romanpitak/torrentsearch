# -*- coding: utf-8 -*-

import pprint


class BaseTorrent:

    def __init__(self):
        self.name = None
        self.info_hash = None

    def _pull_detail(self):
        pass

    def __str__(self):
        return pprint.pformat(self.name)

    def __eq__(self, other):
        return self.info_hash == other.info_hash

    def __ne__(self, other):
        return self.info_hash != other.info_hash

    def __hash__(self):
        return hash(self.info_hash)
