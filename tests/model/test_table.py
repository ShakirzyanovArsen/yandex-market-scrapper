from scrapper_lib.exceptions import TableError
from scrapper_lib.model.table import Table
import pytest


class TestTable:

    def test_raise_exception_on_empty_schema(self):
        with pytest.raises(TableError) as exc_info:
            Table([])
        assert str(exc_info.value) == "Empty schema provided"

    def test_raise_exception_on_invalid_schema(self):
        with pytest.raises(TableError) as exc_info:
            Table([("broken_field", "not type")])
        assert str(exc_info.value) == "<class 'str'> is not a valid type"

    def test_raise_exception_on_different_number_of_fields_in_data_and_schema(self):
        t = Table([("field1", str), ("field2", str)])
        with pytest.raises(TableError) as exc_info:
            t.add_row(("str1", "str2", "str3"))
        assert str(exc_info.value) == "Schema missmatch. Expected 2 fields, but found 3 fields"

    def test_raise_exception_on_different_type_in_schema_and_data(self):
        t = Table([("field1", int), ("field2", str)])
        with pytest.raises(TableError) as exc_info:
            t.add_row(("wrong_type", "correct_type"))
        assert str(exc_info.value) == "Schema is not matching at cell 0. Expected type - <class 'int'>, actual type - <class 'str'>"

    def test_str(self):
        t = Table([("category", str), ("offers", int)])
        t.add_row(("short", 100))
        t.add_row(("loooooooong_category", 100500))

        expected_str = (
                "| category             | offers |\n" +
                "|:---------------------|-------:|\n" +
                "| short                |    100 |\n" +
                "| loooooooong_category | 100500 |\n"
        )
        assert str(t) == expected_str
