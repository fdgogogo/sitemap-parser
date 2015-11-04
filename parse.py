# coding: utf-8
import time
import argparse
import concurrent
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests

longest = 0
counter = 0
total = 0
longest_url = ''
time_total = 0


def get_urls(sitemaps):
    for sitemap in sitemaps:
        print('Parsing: %s' % sitemap)
        xml = requests.get(sitemap).text
        soup = BeautifulSoup(xml, 'html5lib')
        nodes = soup.findAll('loc')
        for node in nodes:
            url = node.text
            yield url


def parse(url):
    if args.full_url:
        output_url = url[:]
    else:
        output_url = url.replace('http://', '')
        output_url = output_url.replace('https://', '')
        if len(output_url) > 80:
            output_url = output_url[:40] + '...' + output_url[-40:]

    r = requests.get(url)

    global counter, longest, total, longest_url, time_total

    counter += 1

    info = '[%5s/%5s]' % (counter, total)
    elapsed = r.elapsed.total_seconds()
    if elapsed > longest:
        longest = elapsed
        longest_url = url
    time_total += elapsed
    print('%s\tParsed %s' % (info, output_url))
    print('%s\t status: %s\t length: %s\t time: %.2fms' % (
        info, r.status_code, len(r.content),
        elapsed * 1000))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse urls from sitemap, support multiple domain, '
                    'separate by space.',
        # usage='get_urls.py example.com example2.com example3.com'
    )
    parser.add_argument('sitemaps', metavar='sitemaps', type=str, nargs='*',
                        help='sitemap urls separated by space.')
    parser.add_argument('-w', '--workers', dest='workers', type=int,
                        default=20, help='Concurrent workers, default 20')
    parser.add_argument('-F', '--full', dest='full_url',
                        action='store_true',
                        help='Print full url',
                        default=False)

    args = parser.parse_args()

    urls = [url for url in get_urls(args.sitemaps)]

    print('Parsing start')
    start = time.time()
    total = len(urls)
    print('Url count: %s' % total)

    with concurrent.futures.ThreadPoolExecutor(
            max_workers=args.workers) as executor:
        future_to_url = {executor.submit(parse, url): url for url in
                         urls}
        for future in concurrent.futures.as_completed(future_to_url):
            _url = future_to_url[future]

    avg = time_total / total

    print('------------------------------------------')
    print('Done')
    print('Count: %(count)s, total time: %(time_total).2fs, '
          'average_time: %(avg).2fms' % {
              'count': total,
              'time_total': time_total,
              'avg': avg * 1000
          })
