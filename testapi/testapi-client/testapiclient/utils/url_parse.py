import os

from six.moves.urllib import parse


def path_join(base, *urls):
    def _path_join(base, url):
        if not base.endswith('/'):
            base += '/'
        return parse.urljoin(base, url)

    urls = (base,) + urls
    return reduce(_path_join, urls)


def query_join(base, **queries):
    return base + '?' + parse.urlencode(queries)


def resource_join(url):
    testapi_url = os.environ.get('testapi_url')
    return path_join(testapi_url, url)
