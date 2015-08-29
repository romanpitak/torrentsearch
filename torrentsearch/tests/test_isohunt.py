# -*- coding: utf-8 -*-

from unittest import TestCase
import torrentsearch


class TestIsoHunt(TestCase):

    def test_search(self):
        ih = torrentsearch.IsoHunt()
        for torrent in ih.search('terminator 1080p'):
            print(torrent)
            print('=' * 80)
            print()
