from DatabaseLibrary import DatabaseLibrary
from .ExtendedConnection import ExtendedConnection

__version__ = '1.0'

class ExtendedDatabaseLibrary(DatabaseLibrary, ExtendedConnection):
    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_VERSION = __version__



