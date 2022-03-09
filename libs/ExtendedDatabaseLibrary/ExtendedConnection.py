import importlib

try:
    import ConfigParser
except:
    import configparser as ConfigParser

from robot.api import logger
from robot.api.deco import keyword

class ExtendedConnection:

    def __init__(self):
        """
        Initializes _dbconnection to None.
        """
        self._dbconnection = None
        self.db_module_name = None

    @keyword("Connect Sql Server")
    def connect_sql_server(
            self,
            db_module=None,
            db_name=None,
            db_username=None,
            db_password=None,
            db_host=None,
            db_port=None,
            db_driver=None,
            db_config_file="./resources/db.cfg"
    ):
        """
        Example db.cfg file
        | [default]
        | dbapiModuleName=pymysqlforexample
        | dbName=yourdbname
        | dbUsername=yourusername
        | dbPassword=yourpassword
        | dbHost=yourhost
        | dbPort=yourport
        | dbDriver=yourdriver

        Example usage:
        | # explicitly specifies all db property values |
        | Connect Sql Server | pyodbc | PGW | pgwuser01 | pgwuser01 | 172.30.74.33 | 1433 | {ODBC Driver 17 for SQL Server}

        | # loads all property values from default.cfg |
        | Connect To Database | dbConfigFile=default.cfg |

        | # loads all property values from ./resources/db.cfg |
        | Connect To Database |
        """

        config = ConfigParser.ConfigParser()
        config.read([db_config_file])

        module_name = 'pyodbc' or db_module or config.get('default', 'dbapiModuleName')
        database = db_name or config.get('default', 'dbName')
        username = db_username or config.get('default', 'dbUsername')
        password = db_password if db_password is not None else config.get('default', 'dbPassword')
        host = db_host or config.get('default', 'dbHost') or 'localhost'
        port = int(db_port or config.get('default', 'dbPort')) or 1433
        driver = '{SQL Server}' or db_driver or config.get('default', 'dbDriver')

        self.db_module_name = module_name
        db_api_2 = importlib.import_module(module_name)

        try:
            logger.info(
                'Connecting using : %s.connect(DRIVER=%s;SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s)' % (
                module_name, driver, host, port, database, username, password))
            self._dbconnection = db_api_2.connect(
                'DRIVER=%s;SERVER=%s,%s;DATABASE=%s;UID=%s;PWD=%s' % (
                driver, host, port, database, username, password))
        except ConnectionError:
            logger.error('Connect SQL Server Fail')

