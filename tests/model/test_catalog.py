import pytest

from scrapper_lib.exceptions import ScrapperError
from scrapper_lib.model import YmlCatalog, Offer, CategoryTree


class TestYmlCatalog:

    def test_list_childs_first(self):
        actual_catalog = YmlCatalog.from_xml_str("""<?xml version="1.0" encoding="UTF-8"?>
        <yml_catalog date="2023-01-19 20:35" >
            <shop>
                <categories>
                    <category id="5" parentId="4">test5</category>
                    <category id="4" parentId="3">test4</category>
                    <category id="3" parentId="2">test3</category>
                    <category id="2" parentId="1">test2</category>
                    <category id="1">test1</category>
                </categories>
                <offers>
                    <offer id="22" available="true" bid="10">
                        <name>test_offer</name>
                        <categoryId>4</categoryId>
                    </offer>
                </offers>
            </shop>
        </yml_catalog>
        """)
        expected_catalog = YmlCatalog(
            offers=[Offer("4", "test_offer")],
            category_tries=[
                CategoryTree("1", None, "test1", child=[
                    CategoryTree("2", "1", "test2", child=[
                        CategoryTree("3", "2", "test3", child=[
                            CategoryTree("4", "3", "test4", child=[
                                CategoryTree("5", "4", "test5")
                            ])
                        ])
                    ])
                ])
            ]
        )
        assert actual_catalog == expected_catalog

    def test_wide_tree(self):
        actual_catalog = YmlCatalog.from_xml_str("""<?xml version="1.0" encoding="UTF-8"?>
                <yml_catalog date="2023-01-19 20:35" >
                    <shop>
                        <categories>
                            <category id="1">test_l1</category>
                            <category id="2" parentId="1">test_l2_1</category>
                            <category id="3" parentId="1">test_l2_2</category>
                            <category id="4" parentId="1">test_l2_3</category>
                            <category id="5" parentId="1">test_l2_4</category>
                        </categories>
                        <offers>
                            <offer id="22" available="true" bid="10">
                                <name>test_offer</name>
                                <categoryId>3</categoryId>
                            </offer>
                        </offers>
                    </shop>
                </yml_catalog>
                """)
        expected_catalog = YmlCatalog(
            offers=[Offer("3", "test_offer")],
            category_tries=[
                CategoryTree("1", None, "test_l1", child=[
                    CategoryTree("2", "1", "test_l2_1"), CategoryTree("3", "1", "test_l2_2"),
                    CategoryTree("4", "1", "test_l2_3"), CategoryTree("5", "1", "test_l2_4")
                ])
            ]
        )
        assert actual_catalog == expected_catalog

    def test_unknown_category_in_offer_raises_exception(self):
        xml_broken_tree = """<?xml version="1.0" encoding="UTF-8"?>
                        <yml_catalog date="2023-01-19 20:35" >
                            <shop>
                                <categories>
                                    <category id="1">test_l1</category>
                                    <category id="2" parentId="1">test_l2</category>
                                </categories>
                                <offers>
                                    <offer id="22" available="true" bid="10">
                                        <name>broken_offer</name>
                                        <categoryId>100500</categoryId>
                                    </offer>
                                </offers>
                            </shop>
                        </yml_catalog>
                        """
        with pytest.raises(ScrapperError) as exc_info:
            YmlCatalog.from_xml_str(xml_broken_tree)
        assert str(exc_info.value) == "Cannot find offer's category id - 100500"
