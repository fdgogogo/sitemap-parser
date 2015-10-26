# sitemap-parser

Simple script to parse all urls from sitemap.xml, then print some useful metadata.

Only tested with django's sitemap.

## Usage

```
usage: parse.py [-h] [-w WORKERS] [-F] [sitemaps [sitemaps ...]]

Parse urls from sitemap, support multiple domain, separate by space.

positional arguments:
  sitemaps              sitemap urls separated by space.

optional arguments:
  -h, --help            show this help message and exit
  -w WORKERS, --workers WORKERS
                        Concurrent workers, default 20
  -F, --full            Print full url
```