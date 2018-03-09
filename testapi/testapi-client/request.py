import requests
import httplib
import sys


r = requests.get('http://127.0.0.1:8000/versions')

if r.status_code == httplib.SERVICE_UNAVAILABLE:
    sys.exit(1)

print r.text