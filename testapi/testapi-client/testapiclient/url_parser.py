import os
import urlparse


def path_join(base, url):
    if not base.endswith('/'):
        base = base +'/'
    return urlparse.urljoin(base, url)

def query_join(base, url):
    return urlparse.urljoin(base, url)

def resource_join(url):
    testapi_url = os.environ.get('testapi_url')
    return path_join(testapi_url, url)
