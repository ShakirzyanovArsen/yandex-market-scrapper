class ScrapperError(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class TableError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
