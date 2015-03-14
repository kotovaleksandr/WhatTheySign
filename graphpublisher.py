import logging

import coloredlogs

import worker


__author__ = 'kotov'

from py2neo import Graph
from py2neo import Relationship

coloredlogs.install()
logging.basicConfig(level=logging.DEBUG)

graph = Graph()


def get_artist_node(artist):
    return graph.merge_one("Artist", "name", artist)


def get_word_node(word):
    return graph.merge_one("Word", "name", word)


processed = open('log.txt').readlines()
processed = [line.strip() for line in processed]

artists_urls = worker.get_artists()
for artist_url in artists_urls:
    try:
        artist_real_name = worker.get_artist_name(artist_url)
        logging.debug('current artist %s', artist_real_name)

        if artist_real_name in processed:
            logging.info('skip %s artist', artist_real_name)
            continue

        words = worker.get_words(artist_url)

        artistNode = get_artist_node(artist_real_name)
        for word in dict(words).keys():
            rel = Relationship(artistNode, 'sign', get_word_node(word))
            graph.create_unique(rel)
        with open("log.txt", "a") as myfile:
            myfile.write(artist_real_name + '\n')
    except Exception as e:
        logging.exception('common error', e)
        with open("errors.txt", "a") as myfile:
            myfile.write(artist_url + '\n')

            # http://www.lyricsfreak.com/a/alison++krauss/
            # http://www.lyricsfreak.com/a/alison+krauss/