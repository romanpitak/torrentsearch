# -*- coding: utf-8 -*-

from lxml import html
from .BaseTorrentSite import BaseTorrentSite
from .utils import *
from .BaseTorrent import BaseTorrent as Torrent
import time


class TorrentzEu(BaseTorrentSite):

    def __init__(self):
        super().__init__()
        self.rating = {
            'any': 'any',
            'good': 'search',
            'verified': 'verified'
        }
        self.order = {
            'rating': 'N',
            'date': 'A',
            'size': 'S',
            'peers': '',
        }
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Referer': 'https://torrentz.eu/',
        }
        self.session.get('https://torrentz.eu/', headers=self.headers)

    def search(self, query, rating='good', order='peers', added=None):
        url = 'https://torrentz.eu/' + self.rating[rating] + self.order[order]
        if added:
            query += ' added:{}'.format(added)
        params = {'f': query}

        response = self.session.get(url, params=params, headers=self.headers)
        document = html.fromstring(response.text)

        torrents = []
        for torrent_dl in document.cssselect('div.results > dl')[:5]:
            torrent = Torrent()
            name = torrent_dl.xpath('dt/a')[0]
            torrent.name = name.text_content().strip()
            torrent.info_hash = name.get('href')[1:]
            torrent.tags = [x for x in xtext(torrent_dl, 'dt')[0].split('»')[1].split(' ') if x]
            verified = int(text(torrent_dl, 'dd > span.v')[0])  # TODO
            added = torrent_dl.cssselect('dd > span.a > span')[0].get('title')
            torrent.uploaded = time.strptime(added, '%a, %d %b %Y %H:%M:%S')
            torrent.size = byte_sized(text(torrent_dl, 'dd > span.s')[0].split(' '))
            torrent.seeders = int(text(torrent_dl, 'dd > span.u')[0].replace(',', ''))
            torrent.leechers = int(text(torrent_dl, 'dd > span.d')[0].replace(',', ''))
            torrents.append(torrent)
        return torrents
