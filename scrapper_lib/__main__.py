import sys

from scrapper_lib.ingestion import requests_catalog
from scrapper_lib.model import YmlCatalog
from scrapper_lib.processing import convert_catalog_to_table
import argparse

parser = argparse.ArgumentParser(
    prog='Yandex market catalog scrapper',
    description='Scraps catalog by link and prints catalog in table format'
)
parser.add_argument("link", help="http/https link to yandex market catalog")
args = parser.parse_args()

xml_content = requests_catalog(args.link)
yml_catalog = YmlCatalog.from_xml_str(xml_content)
table = convert_catalog_to_table(yml_catalog)
print(table)