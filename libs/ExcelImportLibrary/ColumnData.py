class ColumnData:
    """
    This is a class for recording header and values in the excel file.
    """
    def __init__(self):
        self.__header: str = ""
        self.__values: list = []

    def set_header(self, header: str):
        self.__header = header

    def add_value(self, value: object):
        self.__values.append(value)

    def get_header(self) -> str:
        return self.__header

    def get_values(self) -> list:
        return self.__values

    def __str__(self):
        return f'id: {self.__header}, name: {self.__values}'
