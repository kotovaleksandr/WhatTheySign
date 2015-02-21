__author__ = 'kotov.a'

import sys
import logging

import coloredlogs

import lyricsfreakclient


topCount = 20

coloredlogs.install()
logging.basicConfig(level=logging.DEBUG)

# artist = 'two door cinema club'

if len(sys.argv) == 0:
    logging.error('Please, enter artist name...')
    exit()

artist = sys.argv[-1]

logging.info('artist name: %s', artist)

page = lyricsfreakclient.get_artist_page(artist)
links = lyricsfreakclient.get_songs_links_from_page(page, artist)

result = {}

current = 0
from WordCounter import WordCounter, sort_dictionary_by_value

wordCounter = WordCounter()
logging.info('songs count: %d', len(links))

for link in links:
    try:
        logging.debug('link: {0}, {1}%'.format(link, round((current / len(links)) * 100)))
        lyrics = lyricsfreakclient.get_lyrics_from_page(link)
        if lyrics == '' or lyrics is None:
            logging.error('error on song %s', link)
            continue
        wordCounter.count_popular_words(lyrics, result)
    except Exception as e:
        logging.exception('common error', e)
    current += 1
logging.info('Done')
result = sort_dictionary_by_value(words=result)
logging.info('Top %d words in the lyrics %s', topCount, artist)
logging.info(','.join(s[0] for s in result[:topCount]))
