import bs4
import requests
import re
import urlparse

URL_BASE = 'http://www.mpibpc.mpg.de/kantine'
RE_MENU = re.compile(r'/\d+/speise-\d+-?kw\.pdf', re.IGNORECASE)


def get_menu_urls():
    """Download a list of absolute URLs to menus from the start website"""

    r = requests.get(URL_BASE)
    if r.status_code != 200:
        raise Exception("Code {0} downloading base website: {1}".format(r.status_code, r.text))

    soup = bs4.BeautifulSoup(r.text)

    file_list = soup.select("ul.file_list")[0]
    file_links = [a['href'] for a in file_list.select('a.pdf_file') if RE_MENU.match(a['href'])]

    return [urlparse.urljoin(URL_BASE, fl) for fl in file_links]


def download_menu(url, f):
    """Download a menu at URL url into file f"""
    r = requests.get(url, stream=True)
    if not r.ok:
        raise Exception("Code {0} downloading menu: {1}".format(r.status_code, r.text))

    for block in r.iter_content(1024):
        if not block:
            break
        f.write(block)

    f.flush()
