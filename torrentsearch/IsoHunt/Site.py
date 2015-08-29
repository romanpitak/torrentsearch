# -*- coding: utf-8 -*-

from lxml import html
from ..BaseTorrentSite import BaseTorrentSite
from ..utils import *
from .Torrent import Torrent


class Site(BaseTorrentSite):

    def __init__(self):
        super().__init__()
        document = html.fromstring(self.session.get('https://isohunt.to/torrents/advancedSearch').text)
        form = document.cssselect('form#advanced_search')[0]
        self.pars = {key: form.fields[key] for key in form.fields}

    def search(self, query):
        data = self.pars.copy()
        data['AdvancedSearch[allWords]'] = query
        document = html.fromstring(self.session.post('https://isohunt.to/torrents/advancedSearch', data=data).text)
        torrents = []
        for torrent_tr in document.cssselect('#serps > table > tbody > tr'):
            torrent = Torrent()
            torrent.name = torrent_tr.cssselect('td.title-row > a > span')[0].text_content().strip()
            torrent.detail_url = 'https://isohunt.to' + torrent_tr.cssselect('td.title-row > a')[0].get('href')
            torrent.path = [x.text_content().strip() for x in torrent_tr.cssselect('td.title-row > em > small > a')]
            age, unit = torrent_tr.cssselect('td.date-row')[0].text_content().strip().split(' ')  # TODO convert
            torrent.size = byte_sized(torrent_tr.cssselect('td.size-row')[0].text_content().strip().split(' '))
            seeders = (torrent_tr.cssselect('td.sy') + torrent_tr.cssselect('td.sn'))[0]
            torrent.seeders = int(seeders.text_content().strip())
            torrent.rating = int(torrent_tr.cssselect('td.rating-row')[0].text_content().strip())  # TODO convert
            torrents.append(torrent)
        return torrents
