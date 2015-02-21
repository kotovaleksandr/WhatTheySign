__author__ = 'kotov'

import http.client
import re

from html.parser import HTMLParser

mainUrl = "www.azlyrics.com"
# conn = http.client.HTTPConnection(mainUrl, 80)


class LyricsPageParser(HTMLParser):
    def __init__(self):
        self.save = 0
        self.lyrics = ''
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag != 'div':
            return

        for name, value in attrs:
            if name == 'style' and value == 'margin-left:10px;margin-right:10px;':
                self.save = 1
        if 'style' in attrs:
            self.save = 1

    def handle_endtag(self, tag):
        if tag == 'div' and self.save:
            self.save = 0

    def handle_data(self, data):
        if self.save:
            self.lyrics += str(data) + ' '


def getArtistPage(artistName):
    artistUrl = '/{0}/{1}.html'.format(artistName[0], artistName)
    print(artistUrl)
    conn = http.client.HTTPConnection(mainUrl, 80)
    conn.request('GET', artistUrl)
    r = conn.getresponse()
    if r.status == 200:
        artistPage = r.read()
        print(artistPage)
        conn.close()
        return str(artistPage)


def getSongsLinksFromPage(page):
    result = []
    match = re.findall('href=\"../lyrics(.+?)\"', page, re.MULTILINE)
    for g in match:
        print(g)
        result.append(g)
    return result


def getLyricsFromPage(songName):
    songUrl = '/lyrics{0}'.format(songName)
    # print('current song: ', songUrl)
    conn = http.client.HTTPConnection(mainUrl, 80)
    conn.request('GET', songUrl)
    try:
        r = conn.getresponse()
        if r.status == 200:
            text = r.read()
            myHtmlParser = LyricsPageParser()
            myHtmlParser.feed(str(text))
            print(myHtmlParser.lyrics)
            return myHtmlParser.lyrics
        else:
            return ''
    except Exception as e:
        print(e)
    finally:
        conn.close()


