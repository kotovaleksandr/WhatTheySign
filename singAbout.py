__author__ = 'kotov'

import lyricsfreakclient

artist = 'two door cinema club'

page = lyricsfreakclient.getArtistPage(artist)
links = lyricsfreakclient.getSongsLinksFromPage(page, artist)

result = {}

current = 0
from WordCounter import WordCounter

wordCounter = WordCounter()

for link in links:
    try:
        print('link: {0}, {1}%'.format(link, round((current / len(links)) * 100)))
        lyrics = lyricsfreakclient.getLyricsFromPage(link)
        if lyrics == '' or lyrics is None:
            print('error on song: ', link)
            continue

        wordCounter.countpopularwords(lyrics, result)
    except Exception as e:
        print('error, lyrics', e)
    # print('Result: ', collections.OrderedDict(result, reversed = True))
    # wordCounter.printOrdered(result)
    # time.sleep(5)
    current += 1
# print(result)
print('Done')
result = wordCounter.sortdictionarybyvalue(words=result)
print(result[:15])
# wordCounter.printordered(result)