# -*- coding: utf-8 -*-

size_units = {
    'B': 1,
    'Bytes': 1,
    'KB': 1024 ** 1,
    'MB': 1024 ** 2,
    'GB': 1024 ** 3,
    'KiB': 1024 ** 1,
    'MiB': 1024 ** 2,
    'GiB': 1024 ** 3,
}


def byte_sized(size):
    return float(size[0]) * size_units[size[1]]


def human_sized(size):
    return str(size)  # TODO


def text(element, selector):
    return [x.text_content().strip() for x in element.cssselect(selector)]


def xtext(element, selector):
    return [x.text_content().strip() for x in element.xpath(selector)]
