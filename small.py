import feedparser 

def main():
    data = feedparser.parse('http://tass.ru/rss/v2.xml')
    for e in data.entries:
        if e['summary']:
            print(e['summary'])
        else:
            pass
main()
