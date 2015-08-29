# -*- coding: utf-8 -*-

from ..BaseTorrent import BaseTorrent
from ..Comment import Comment
from ..File import File
import requests
import time
from lxml import html
from ..utils import *


class Torrent(BaseTorrent):

    def _pull_detail(self):

        if not self.session:
            self.session = requests.Session()

        document = html.fromstring(self.session.get(self.detail_url).text)

        # description
        description = document.cssselect('#details > div > .nfo > pre')
        if description:
            self.description = description[0].text_content().strip()
            # TODO HTML description?
        else:
            self.description = False

        # hash size uploaded tags seeders leechers
        details = dict(zip(
            [x.text_content().strip()[:-1] for x in document.cssselect('#details > dl > dt')],
            document.cssselect('#details > dl > dd')
        ))
        self.hash = details['Info Hash'].text_content().strip()
        if not self.hash:
            self.hash = ''.join(text(document, '#details > dl')).split('Info Hash:')[1].strip()
        self.size = byte_sized(details['Size'].text_content().split('(')[1].split(')')[0].split('\xa0'))
        self.uploaded = time.strptime(details['Uploaded'].text_content().strip(), '%Y-%m-%d %H:%M:%S GMT')
        self.tags = []
        if 'Tag(s)' in details:
            # TODO tag links (urls)?
            self.tags = [x.text_content().strip() for x in details['Tag(s)'].xpath('a')]
        self.seeders = details['Seeders'].text_content().strip()
        self.leechers = details['Leechers'].text_content().strip()

        # comments
        self.comments = []
        for comment_div in document.cssselect('#comments > div'):
            # TODO user url
            comment = Comment()
            comment_user, comment_time = text(comment_div, 'p.byline')[0].split(' at ')
            comment.user = comment_user
            comment.time = time.strptime(comment_time, '%Y-%m-%d %H:%M CET:')
            comment.message = text(comment_div, 'div.comment')[0]
            self.comments.append(comment)

        # files
        url = 'https://thepiratebay.mn/ajax_details_filelist.php'
        params = {'id': self.detail_url.split('/')[4]}
        response = self.session.get(url, params=params)
        self.files = []
        if 'File list not available' not in response.text:
            document = html.fromstring(response.text)
            for file_tr in document.cssselect('table > tr'):
                file_name, file_size = text(file_tr, 'td')
                file = File()
                file.name = file_name
                file.size = byte_sized(file_size.split('\xa0'))
                self.files.append(file)
