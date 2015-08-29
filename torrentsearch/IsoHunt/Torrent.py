# -*- coding: utf-8 -*-

from ..BaseTorrent import BaseTorrent
from ..utils import *
import requests
import json
import time
from lxml import html


class Torrent(BaseTorrent):

    def _pull_detail(self):
        if not self.session:
            self.session = requests.Session()
        response = self.session.get(self.detail_url)
        if 'Sorry, but requested page is not available' in response.text:
            return
        document = html.fromstring(response.text)

        description = document.cssselect('#torrent_details > .torrent-description')
        if description:
            self.description = description[0].text_content().strip()
        else:
            self.description = False

        magnet = document.cssselect('a.btn-magnet')
        if magnet:
            self.magnet = magnet[0].get('href')
        else:
            # TODO Removed by the request of copyright owner - or something else ?
            self.magnet = False

        details = document.cssselect('div.p > p.text-lg.mb2')
        if details:
            details = details[0].text_content().strip()
            if 'Added' in details:
                self.uploaded = time.strptime(details.split('Added\xa0')[1].strip(), '%Y-%m-%d %H:%M:%S')

        # pull trackers information
        tracker_post_keys = {' id: ': 'id', ' hash: ': 'hash', ' scrapeDate: ': 'date'}
        data = {'_csrf': document.cssselect('meta[name="csrf-token"]')[0].get('content')}
        for script_line in '\n'.join(text(document, 'script')).split('\n'):
            for key in tracker_post_keys:
                if key not in script_line:
                    continue
                data[tracker_post_keys[key]] = script_line.split('\'')[1]
        try:
            self.hash = data['hash']
        except KeyError:
            print('\n'.join(text(document, 'script')))
            print()
            print(self.detail_url)
            quit()
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRF-Token': data['_csrf'],
            'Referer': self.detail_url,
        }
        response = self.session.post('https://isohunt.to/torrents/trackers', data=data, headers=headers)
        tracker_info = json.loads(response.text)
        if 'status' in tracker_info:
            self.trackers_count = 0
            self.trackers = []
        else:
            self.seeders = tracker_info['seeders']
            self.leechers = tracker_info['leechers']
            self.trackers_count = tracker_info['trackersCount']
            self.trackers = [
                dict(zip(
                    ['name', 'status', 'statistics', 'overall'],
                    [td.text_content().strip() for td in tracker.xpath('td')]
                ))
                for tracker in html.fromstring(tracker_info['html']).xpath('tr')[1:]
            ]
