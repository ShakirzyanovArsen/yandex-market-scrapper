from __future__ import annotations

from typing import List, Dict, Set
from xml.etree import ElementTree
from logging import log, WARN

from scrapper_lib.exceptions import ScrapperError


class YmlCatalog:
    def __init__(self, offers: List[Offer], category_tries: List[CategoryTree]):
        self.__offers = offers
        self.__category_tries = category_tries
        self.__category_offer_index: Dict[str, List[Offer]] = {}
        for offer in self.__offers:
            if offer.category_id not in self.__category_offer_index:
                self.__category_offer_index[offer.category_id] = [offer]
            else:
                self.__category_offer_index[offer.category_id].append(offer)

    @property
    def offers(self) -> List[Offer]:
        return self.__offers

    @property
    def category_tries(self) -> List[CategoryTree]:
        return self.__category_tries

    @staticmethod
    def from_xml_str(xml_content: str):
        xml_etree = ElementTree.fromstring(xml_content)

        category_tags = xml_etree.findall('shop/categories/category')
        id_index: Dict[str, CategoryTree] = {}
        for category_tag in category_tags:
            if category_tag.attrib.get("parentId") is None:
                parent_id = None
            else:
                parent_id = category_tag.attrib.get("parentId")
            category = CategoryTree(
                tree_id=category_tag.attrib["id"],
                parent_id=parent_id,
                name=category_tag.text
            )
            id_index[category.tree_id] = category
        root_categories: List[CategoryTree] = []
        for tree_id, category in id_index.items():
            if category.parent_id is None:
                root_categories.append(category)
                continue
            if category.parent_id not in id_index:
                log(WARN, f"Broken category tree. Can't find parent category with id {category.parent_id}")
                continue
            id_index[category.parent_id].add_children(category)

        offer_tags = xml_etree.findall('shop/offers/offer')
        offers: List[Offer] = []
        for offer_tag in offer_tags:
            offer_name = offer_tag.find("name").text
            category_id = str(offer_tag.find("categoryId").text)
            if category_id not in id_index:
                raise ScrapperError(f"Cannot find offer's category id - {category_id}")
            offers.append(Offer(category_id, offer_name))

        return YmlCatalog(offers, root_categories)

    def get_offers_by_category_id(self, category_id: str) -> List[Offer]:
        return list(self.__category_offer_index.get(category_id, []))

    def __eq__(self, other):
        if isinstance(other, YmlCatalog):
            return self.__offers == other.__offers and self.__category_tries == other.__category_tries
        return False


class Offer:
    def __init__(self, category_id: str, name: str):
        self.__category_id = category_id
        self.__name = name

    @property
    def category_id(self) -> str:
        return self.__category_id

    @property
    def name(self) -> str:
        return self.__name

    def __eq__(self, other):
        if isinstance(other, Offer):
            return self.__category_id == other.__category_id and self.__name == other.__name
        return False


class CategoryTree:
    def __init__(self, tree_id: str, parent_id: str, name: str, child: List[CategoryTree] = None):
        if child is None:
            child = []
        self.__tree_id = tree_id
        self.__parent_id = parent_id
        self.__name = name
        self.__child = child

    def add_children(self, children: CategoryTree):
        self.__child.append(children)

    @property
    def tree_id(self) -> str:
        return self.__tree_id

    @property
    def parent_id(self) -> str:
        return self.__parent_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def child(self) -> List[CategoryTree]:
        return self.__child

    def __eq__(self, other):
        if isinstance(other, CategoryTree):
            return (
                    self.__tree_id == other.__tree_id
                    and self.__parent_id == other.__parent_id
                    and self.__name == other.__name
                    and set(self.__child) == set(other.__child)
            )
        return False

    def __hash__(self):
        return hash((self.tree_id, self.parent_id, self.name, tuple(set(self.child))))
