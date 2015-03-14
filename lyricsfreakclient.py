__author__ = 'kotov.a'

import http.client
import re
import logging

from html.parser import HTMLParser

logging.basicConfig(level=logging.DEBUG)

mainUrl = "http://www.lyricsfreak.com"
# conn = http.client.HTTPConnection(mainUrl, 80)
headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
    'Content-type': 'text\html',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}


class ParseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class LyricsPageParser(HTMLParser):
    def __init__(self):
        self.save = 0
        self.lyrics = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag != 'div':
            return

        for name, value in attrs:
            if name == 'id' and 'content_h' in value:
                self.save = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.save:
            self.save = 0

    def handle_data(self, data):
        if self.save:
            self.lyrics += bytes(data, 'utf8').decode("unicode_escape").strip().lower() + ' '


def get_artist_page(artist_name):
    artist_url = '{2}/{0}/{1}/'.format(artist_name[0], artist_name.replace('  ', ' ').replace(' ', '+'), mainUrl)

    # http://www.lyricsfreak.com/a/a+pink/
    logging.debug('get artist page %s', artist_url)
    # conn.set_debuglevel(0)
    # http://www.lyricsfreak.com/m/metallica/
    conn = http.client.HTTPConnection(mainUrl, 80)
    conn.request('GET', artist_url, headers=headers)
    r = conn.getresponse()
    if r.status == 200:
        artist_page = r.read()
        conn.close()
        return str(artist_page)
    logging.error('error from server: %s', r.reason)


def get_artist_page_by_url(artist_page_url):
    logging.debug('get artist page %s', artist_page_url)
    # conn.set_debuglevel(0)
    # http://www.lyricsfreak.com/m/metallica/
    conn = http.client.HTTPConnection(mainUrl, 80)
    conn.request('GET', mainUrl + artist_page_url, headers=headers)
    r = conn.getresponse()
    if r.status == 200:
        artist_page = r.read()
        conn.close()
        return str(artist_page)
    else:
        raise ParseError('http error, code {0}, url {1}'.format(r.reason, artist_page_url))

def get_songs_links_from_page(page, artist_name):
    result = []
    match = re.findall('<a href=\"' + artist_name + '(.+?)\"', page, re.MULTILINE)
    for g in match:
        url = artist_name + g
        result.append(url)
    return result


def get_lyrics_from_page(song_name):
    song_url = '{0}{1}'.format(mainUrl, song_name)
    # print('current song: ', song_url)
    # conn = http.client.HTTPConnection(mainUrl, 80)
    conn = http.client.HTTPConnection(mainUrl, 80)
    conn.request('GET', song_url)
    try:
        r = conn.getresponse()
        if r.status == 200:
            text = r.read()
            html_parser = LyricsPageParser()
            html_parser.feed(str(text))
            # print(html_parser.lyrics)
            return html_parser.lyrics
        else:
            raise ParseError('error on song {0}, http error, code {1}, reason {2}'.format(song_name, r.code, r.reason))
            # logging.error('error on song %s, http code: %s', song_url, r.reason)
            # return ''
    finally:
        conn.close()


def get_artists_list():
    result = []
    conn = http.client.HTTPConnection(mainUrl, 80)
    try:
        for char in 'abcdefghijklmnopqrstuvwxyz':
            pattern = 'http://www.lyricsfreak.com/{0}_top.html'
            letter_url = pattern.format(char)
            conn.request('GET', letter_url)
            r = conn.getresponse()
            if r.status == 200:
                page = r.read()
                page = bytes(str(page), 'utf8').decode("unicode_escape")
                re_pattern = '<a href=\"(.+?)\" title=\"{0}'.format(char.upper())
                match = re.findall(re_pattern, str(page), re.MULTILINE)
                for g in match:
                    result.append(g)
                    logging.debug('artist %s', g)
            else:
                raise ParseError('http error {0}, url {1}'.format(r.reason, letter_url))
    finally:
        conn.close()
    return result

# page = get_artist_page(artistName)
# links = get_songs_links_from_page(page, artistName)
# for link in links:
# get_lyrics_from_page(link)
# break

def get_artist_name(artist):
    page = get_artist_page_by_url(artist)
    match = re.findall('<h2>Lyrics to (.+?)</h2>', page, re.MULTILINE)
    for m in match:
        return m
