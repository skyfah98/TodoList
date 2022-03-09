from .ExcelImport import ExcelImport
from .ColumnData import ColumnData
from .RowData import RowData

__version__ = '0.1'


class ExcelImportLibrary(ExcelImport, ColumnData, RowData):
    ROBOT_LIBRARY_VERSION = __version__
