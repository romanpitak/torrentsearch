# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()

setup(
    name='torrentsearch',
    version='0.0.0',
    description='Torrent search library.',
    long_description=readme(),
    url='https://github.com/romanpitak/torrentsearch',
    author='Roman Piták',
    author_email='roman@pitak.net',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
    keywords='torrent',
    packages=['torrentsearch'],
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False,
)
