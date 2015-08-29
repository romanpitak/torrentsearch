# -*- coding: utf-8 -*-


class Comment:

    def __init__(self):
        self.user = ''
        self.time = None
        self.message = ''

    def __str__(self):
        return str(self.message)
