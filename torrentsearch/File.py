# -*- coding: utf-8 -*-

from .utils import *


class File:

    def __init__(self):
        self.name = ''
        self.size = 0.0

    def __str__(self):
        return '{} ({})'.format(self.name, human_sized(self.size))
