__author__ = 'kotov.a'

import http.client
import re
import logging

from html.parser import HTMLParser

mainUrl = "http://www.lyricsfreak.com"
# conn = http.client.HTTPConnection(mainUrl, 80)
headers = {
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
    'Content-type': 'text\html',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
}
conn = http.client.HTTPConnection(mainUrl, 80)


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
    artist_url = '{2}/{0}/{1}/'.format(artist_name[0], artist_name.replace(' ', '+'), mainUrl)

    conn.set_debuglevel(0)
    # http://www.lyricsfreak.com/m/metallica/
    conn.request('GET', artist_url, headers=headers)
    r = conn.getresponse()
    if r.status == 200:
        artist_page = r.read()
        conn.close()
        return str(artist_page)
    logging.error('error from server: %s', r.reason)


def get_songs_links_from_page(page, artist_name):
    artist_prefix_re = '/{0}/{1}'.format(artist_name[0], artist_name.replace(' ', '\+'))
    artist_prefix = '/{0}/{1}'.format(artist_name[0], artist_name.replace(' ', '+'))
    result = []
    match = re.findall('href=\"' + artist_prefix_re + '(.+?)\"', page, re.MULTILINE)
    for g in match:
        url = artist_prefix + g
        result.append(url)
    return result


def get_lyrics_from_page(song_name):
    song_url = '{0}{1}'.format(mainUrl, song_name)
    # print('current song: ', song_url)
    # conn = http.client.HTTPConnection(mainUrl, 80)
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
            logging.error('error on song %s, http code: %s', song_url, r.reason)
            return ''
    except Exception as e:
        logging.exception(e)


# page = get_artist_page(artistName)
# links = get_songs_links_from_page(page, artistName)
# for link in links:
# get_lyrics_from_page(link)
# break
