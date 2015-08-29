# -*- coding: utf-8 -*-

from lxml import html
from ..BaseTorrentSite import BaseTorrentSite
from ..utils import *
from .Torrent import Torrent
import time


class Site(BaseTorrentSite):

    def __init__(self):
        super().__init__()
        response = self.session.get('https://thepiratebay.se/')
        self.url = response.url  # get proxy name

    def search(self, query):
        response = self.session.get(self.url + 's/', params={
            'q': query,
            'page': 0,
            'orderby': 99
        })

        document = html.fromstring(response.text)
        torrents = []
        for result_tr in document.cssselect('#searchResult > tr'):
            torrent = Torrent()
            torrent.path = [x.text_content().strip() for x in result_tr.cssselect('td.vertTh a')]
            torrent.name = result_tr.cssselect('div.detName > a.detLink')[0].text_content().strip()
            torrent.detail_url = self.url[:-1] + result_tr.cssselect('div.detName > a.detLink')[0].get('href')
            torrent.magnet = result_tr.cssselect('a[title="Download this torrent using magnet"]')[0].get('href')
            torrent.seeders, torrent.leechers = [x.text_content().strip() for x in result_tr.xpath('td')[-2:]]
            description = result_tr.cssselect('td > font.detDesc')[0].text_content().strip()
            description = dict([x.split(' ', 1) for x in description.split(', ')])
            torrent.size = byte_sized(description['Size'].split('\xa0'))
            if ':' in description['Uploaded']:
                torrent.uploaded = time.strptime(time.strftime('%Y') + description['Uploaded'], '%Y%m-%d\xa0%H:%M')
            else:
                torrent.uploaded = time.strptime(description['Uploaded'], '%m-%d\xa0%Y')
            torrents.append(torrent)
        return torrents
