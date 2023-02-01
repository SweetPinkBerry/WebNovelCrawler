# WebNovelCrawler

An implementation that crawls through a fastnovel.net npovel and returns either a file containing the complete novel, or an html of each chapter with an index page.

## How to use

Requires the modules through pip:
- requests
- BeautifulSoup
- unidecode

Run with:
```python
python https://fastnovel.net/<novel> <file>.txt/html
```
