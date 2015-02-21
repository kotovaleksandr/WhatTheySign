__author__ = 'kotov'

import http.client
import re

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


def getArtistPage(artistName):
    artistUrl = '{2}/{0}/{1}/'.format(artistName[0], artistName.replace(' ', '+'), mainUrl)
    print(artistUrl)

    conn.set_debuglevel(0)
    # http://www.lyricsfreak.com/m/metallica/
    conn.request('GET', artistUrl, headers=headers)
    r = conn.getresponse()
    if r.status == 200:
        artistPage = r.read()
        print(artistPage)
        conn.close()
        return str(artistPage)
    print('error from server:', r.reason)


def getSongsLinksFromPage(page, artistName):
    artistPrefixRe = '/{0}/{1}'.format(artistName[0], artistName.replace(' ', '\+'))
    artistPrefix = '/{0}/{1}'.format(artistName[0], artistName.replace(' ', '+'))
    result = []
    match = re.findall('href=\"' + artistPrefixRe + '(.+?)\"', page, re.MULTILINE)
    for g in match:
        url = artistPrefix + g
        print(url)
        result.append(url)
    return result


def getLyricsFromPage(songName):
    songUrl = '{0}/{1}'.format(mainUrl, songName)
    # print('current song: ', songUrl)
    # conn = http.client.HTTPConnection(mainUrl, 80)
    conn.request('GET', songUrl)
    try:
        r = conn.getresponse()
        if r.status == 200:
            text = r.read()
            myHtmlParser = LyricsPageParser()
            myHtmlParser.feed(str(text))
            # print(myHtmlParser.lyrics)
            return myHtmlParser.lyrics
        else:
            return ''
    except Exception as e:
        print(e)
    finally:
        conn.close()


# page = getArtistPage(artistName)
# links = getSongsLinksFromPage(page, artistName)
# for link in links:
# getLyricsFromPage(link)
# break
