from urllib.request import urlopen


def url_exists(url):
    try:
        urlopen(url)
        return True
    except Exception:
        return False
