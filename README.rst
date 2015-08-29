Torrent Search
==============

Simple library to help me search for torrents (magnet links).

Usage
-----

.. code:: python

    import torrentsearch
    tpb = torrentsearch.ThePirateBay()
    for torrent in tpb.search('legal torrent ;) 1080p'):
        print(torrent)

Notes
-----

- code suggestions welcome
