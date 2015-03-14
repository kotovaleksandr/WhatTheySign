__author__ = 'kotov.a'

import logging

import lyricsfreakclient


def get_artists():
    return lyricsfreakclient.get_artists_list()


def get_words(artist):
    top_count = 50

    # artist = 'two door cinema club'

    logging.info('artist name: %s', artist)

    page = lyricsfreakclient.get_artist_page_by_url(artist)
    links = lyricsfreakclient.get_songs_links_from_page(page, artist)

    result = {}

    current = 0
    from WordCounter import WordCounter, sort_dictionary_by_value

    wordCounter = WordCounter()
    logging.info('songs count: %d', len(links))

    for link in links:
        logging.debug('link: {0}, {1}%'.format(link, round((current / len(links)) * 100)))
        lyrics = lyricsfreakclient.get_lyrics_from_page(link)
        if lyrics == '' or lyrics is None:
            # raise lyricsfreakclient.ParseError('empty lyrics on link {0}'.format(link))
            logging.warning('emtpy lyrics on url %s', link)
        else:
            wordCounter.count_popular_words(lyrics, result)
        current += 1
    logging.info('Done')
    result = sort_dictionary_by_value(words=result)
    logging.info('Top %d words in the lyrics %s', top_count, artist)
    logging.info(','.join(s[0] for s in result[:top_count]))
    return result[:top_count]


def get_artist_name(artist):
    return lyricsfreakclient.get_artist_name(artist)