# -*- coding: utf-8 -*-

from unittest import TestCase
import torrentsearch


class TestThePirateBay(TestCase):
    
    def test_search(self):
        ih = torrentsearch.ThePirateBay()
        for torrent in ih.search('terminator 1080p'):
            print(torrent)
            print('=' * 80)
            print()
