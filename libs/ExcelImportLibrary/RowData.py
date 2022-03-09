class RowData:
    """
    This is a class for recording a test case in the excel file.
    """
    def __init__(self, row_id: int):
        self.__start_row: int = row_id
        self.__end_row: int = row_id
        self.__ColumnData: list = []

    def add_column(self, value: object):
        """
        One row has many columns, we would like to add ColumnData object into a list.

        :param value: the object of ColumnData
        """
        self.__ColumnData.append(value)

    def increase_row(self):
        """
        The test case has many rows, this method is count a row in the test case.
        """
        self.__end_row += 1

    def get_start_row(self) -> int:
        """
        First rows of the test case.

        :return: index of first row
        """
        return self.__start_row

    def get_end_row(self) -> int:
        """
        Last rows of the test case.

        :return: index of last row
        """
        return self.__end_row

    def get_columns(self) -> list:
        """
        List of ColumnData.

        :return: ColumnData
        """
        return self.__ColumnData

    def get_columns_dict(self) -> dict:
        """
        This method makes a dictionary that keys are header and values are a list of value in a test case.
        Please be reminded that headers in the excel file should be a unique because the keys will be replaced.
        :return: dictionary of headers and values.
        """
        values = {}
        for value in self.__ColumnData:
            values[value.get_header()] = value.get_values()
        return values

    def __str__(self):
        values_str = ""
        for value in self.__ColumnData:
            values_str += value.__str__() + "\n"
        return f'row_id: {self.__start_row}\trow_count: {self.__end_row}\n{values_str}'
