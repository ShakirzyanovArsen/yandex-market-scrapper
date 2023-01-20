from typing import List, Dict, Tuple

from scrapper_lib.exceptions import TableError


class Table:
    def __init__(self, schema: List[Tuple[str, type]]):
        self.__data: List[tuple] = []
        if len(schema) == 0:
            raise TableError(f"Empty schema provided")
        for name, t in schema:
            if type(t) is not type:
                raise TableError(f"{str(type(t))} is not a valid type")
        self.__schema = schema
        self.__str_max_lengths = [len(name) for name, t in schema]

    def add_row(self, row: tuple):
        if len(row) != len(self.__schema):
            raise TableError(f"Schema missmatch. Expected {len(self.__schema)} fields, but found {len(row)} fields")
        for idx, cell in enumerate(row):
            expected_type = self.__schema[idx][1]
            if type(cell) is not expected_type:
                raise TableError(f"Schema is not matching at cell {idx}. "
                                 f"Expected type - {expected_type}, actual type - {type(cell)}"
                                 )
            cell_str_len = len(str(cell))
            if self.__str_max_lengths[idx] < cell_str_len:
                self.__str_max_lengths[idx] = cell_str_len

        self.__data.append(row)

    def __str__(self):
        cell_strs = [" " + name_t[0].ljust(self.__str_max_lengths[idx] + 1)
                     for idx, name_t in enumerate(self.__schema)]
        result = '|' + '|'.join(cell_strs) + '|\n'
        devider = []
        for idx, name_t in enumerate(self.__schema):
            if idx == 0:
                devider.append(":".ljust(self.__str_max_lengths[idx] + 2, "-"))
            elif idx == len(self.__schema) - 1:
                devider.append(":".rjust(self.__str_max_lengths[idx] + 2, "-"))
            else:
                devider.append("-".ljust(self.__str_max_lengths[idx] + 2, "-"))
        result += "|" + "|".join(devider) + "|\n"
        for row in self.__data:
            cell_strs = []
            for idx, cell in enumerate(row):
                if self.__schema[idx][1] == int:
                    cell_strs.append(str(cell).rjust(self.__str_max_lengths[idx] + 1) + " ")
                else:
                    cell_strs.append(" " + str(cell).ljust(self.__str_max_lengths[idx] + 1))
            result += "|" + "|".join(cell_strs) + "|\n"
        return result
