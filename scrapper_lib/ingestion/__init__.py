import requests
from xml.etree import ElementTree


def requests_catalog(url: str) -> str:
    response = requests.get(url)
    return response.content

