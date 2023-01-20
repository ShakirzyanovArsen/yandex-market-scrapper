from typing import List

from scrapper_lib.model import YmlCatalog, CategoryTree
from scrapper_lib.model.table import Table


def convert_catalog_to_table(catalog: YmlCatalog):
    result_table = Table([("category", str), ("offers", int)])
    _build_recursively(catalog.category_tries, result_table, catalog, "")
    return result_table


def _build_recursively(tries: List[CategoryTree], table: Table, catalog: YmlCatalog, category_full_name: str):
    for tree in tries:
        if category_full_name != "":
            new_category_full_name = category_full_name + " / " + tree.name
        else:
            new_category_full_name = tree.name
        offers = len(catalog.get_offers_by_category_id(tree.tree_id))
        table.add_row((new_category_full_name, offers))
        _build_recursively(tree.child, table, catalog, new_category_full_name)
    return table
