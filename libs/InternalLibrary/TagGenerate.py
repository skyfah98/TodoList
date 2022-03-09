import os
from robot.api.deco import keyword
from datetime import datetime, timezone
from datetime import timedelta
from tzlocal import get_localzone
import re
import random
from robot.api import logger
import pytz
from base64 import urlsafe_b64decode
from ExtendedDatabaseLibrary import ExtendedDatabaseLibrary


class TagGenerate:

    """
    TagGenerate have function about generate value from special tag ``[TAGS]`` that set in FCISDebitBankAcc data file
    to return in generated value.

    *Version*: 1.1.0

    *Last Updated*: 31-Aug-2020

    *Author*: Yannawat Jaengsawang

    *Email*: yannawat.j@kbtg.tech

    == Supported Tag ==
    | *Tag*                     | *Generated Value*                                                                     |
    | [AUTO_GEN_ID]             | ROBOT202001290123456789                                                               |
    | [AUTO_GEN_DOC_ID]         | DOC2020012                                                                            |
    | [AUTO_GEN_{CUSTOM_ID}_ID  | {CUSTOM_ID}202001290123456789                                                         |
    | [EXIST_{CUSTOM_ID}_ID]    | << Last value from [AUTO_GEN_{CUSTOM_NAME}_ID] >>                                     |
    | [AUTO_GEN_PHONE]          | 099999????                                                                            |
    | [EXIST_PHONE]             | << Last value from [AUTO_GEN_PHONE] >>                                                |
    | [AUTO_GEN_{BOOK_TYPE}]    | IOS-93316074-4-055, ADR-93316074-4-055                                                |
    | [EXIST_{BOOK_TYPE}]       | << Last value from [AUTO_GEN_{BOOK_TYPE}] >>                                          |
    | [NOW_ISO_DT]              | 2020-01-07T14:29:02.567Z                                                              |
    | [NOW_UTC_DT]              | 2020-01-07T14:29:02.567+07:00                                                         |
    | [NOW_UTC_DATE]            | 2020-01-17                                                                            |
    | [NOW_DATE_NO_SYMBOL]      |                                                                               |
    | [NOW_TIME_NO_SYMBOL]      |
    | [AUTO_GET_INVOICE_NO]     | 202001071429  |
    | [EXIST_ISO_DT]            | << Last value from [NOW_ISO_DT] >>                                                    |
    | [EXIST_UTC_DT]            | << Last generated value from [NOW_UTC_DT] >>                                          |
    | [EXIST_UTC_DATE]          | << Last value from [NOW_UTC_DATE] >>                                                  |
    | [SAVE]                    | << Save actual value >>                                                               |
    | [LOAD]                    | << Load saved actual value >>                                                         |
    | [SAVE_COOKIE]             | convert to valid cooke then save                                                      |
    | [LOAD_COOKIE]             | load lasted valid form last saved cookie                                              |
    | [QUERY:??????]            | query sql database with sql statement on tag rear (statement support *Tag* inside)    |
    | [NOW_ISO8601_DT]          | 2020-01-02 14:29:02                                                                   |
    | [EXIST_ISO8601_DT]        | load existed datetime in format ISO8601 (now it come from [NOW_ISO8602_DT] tag        |
    | [NOW_BPA_DT]              | 20200102 14:29:02     |
    """

    __existed = {
        'ROBOT': None,
        'ISO_DT': None,
        'UTC_DT': None,
        'UTC_DATE': None,
        'IOS': None,
        'ADR': None,
        'PHONE': None
        # Space for other [AUTO_GEN_{CUSTOM_NAME}_ID] tag
    }
    __saved = {
        'UNDEFINED': False,
        'COOKIE_LAST': ''
        # Space for other [SAVE_{NAME}] tag
    }
    __cookies = {
        'COOKIE': {},
        'COOKIE_LAST': {}
    }

    @keyword("Get Saved Cookies")
    def get_saved_cookies(self):
        """
        Get all saved cookies
        """
        return self.__cookies

    @keyword("Clear Cookies")
    def clear_cookies(self):
        """
        Clear saved cookies
        """
        __cookies = {
            'COOKIE': {},
            'COOKIE_LAST': {}
        }

    @keyword("Clear Saved")
    def clear_saved(self):
        """
        Clear saved data
        """
        self.__saved = {
            'UNDEFINED': False
        }

    @keyword("Clear Existed")
    def clear_existed(self):
        """
        Clear existed data. Some generated tag will save data for reuse.
        """
        __existed = {
            'ROBOT': None,
            'ISO_DT': None,
            'UTC_DT': None,
            'UTC_DATE': None,
            'IOS': None,
            'ADR': None,
            'PHONE': None,
        }

    @keyword("Get Tags In String")
    def get_tags_in_string(self, string, open_symbol='[', close_symbol=']'):
        """
        Get only tag name from full string.
        """
        subs = str(string).split(close_symbol)
        tags = []
        for sub in subs:
            if sub.find('[') != -1:
                value = sub.split(open_symbol)
                tags.append('[' + value[-1] + ']')
        return tags

    @keyword("Verify Tag By Regular Expression")
    def verify_tag_by_regular_expression(self, expected: str, actual: str, conj: str = "??????"):
        """
        Verify tag by regular expression

        *Options*

        ``expected``: Tag string with conjunction combine with.

        ``actual``: Tag from FCISDebitBankAcc data need to check with expected tag.

        ``conj``: Conjunction word that need to set for ignore those space for regular expression.

        *Examples*

        |  ${RESULT} =       |  `Verify Tag By Regular Expression`   |  [AUTO_GEN_??????_ID]  |  [AUTO_GEN_PARTNER_ID]  |  ??????  |
        |  `log to console`  |  ${RESULT}                            |  #  True               |                         |          |
        """
        expected = str(expected).replace("[", "\[").replace("]", "\]").replace("(", "\(").replace(")", "\)").replace(".", "\.")
        expected = str(expected).split(conj)
        size = len(expected)
        ex_reg = ''
        if size == 1: ex_reg = '^' + ex_reg + expected[0] + '$'
        else:
            for i in range(size):
                if i == 0: ex_reg = '^' + ex_reg + expected[i] + '.*'
                elif i == size - 1: ex_reg = ex_reg + expected[i] + '$'
                else: ex_reg = ex_reg + expected[i] + '.*'
        result = re.search(ex_reg, actual)
        if result:
            return True
        else:
            return False

    @keyword("Generate Value For Tag")
    def generate_value_for_tag(self, tag: str, value=None, show_log=True):
        """
        Generate value for Tag

        *Options*

        ``tag``: Tag string from FCISDebitBankAcc data

        ``value``: actual value from data

        *Examples*

        |  ${GENERATED_VALUE} =      |  `Generate Value For Tag`     |  [AUTO_GEN_USER_ID]    |               | # ROBOT_20200221_1828392747 |
        |  ${GENERATED_VALUE} =      |  `Generate Value For Tag`     |  [SAVE]                |  12345698     | #                           |
        |  ${GENERATED_VALUE} =      |  `Generate Value For Tag`     |  [LOAD]                |               | # 12345698                  |
        """

        if self.verify_tag_by_regular_expression('[AUTO_GEN_DOC_ID]', tag):
            return self.__auto_gen_id(tag, 13)  # ex. DOC2020012

        elif self.verify_tag_by_regular_expression('[AUTO_GEN_INVOICE_NO]', tag):
            return self.__generate_invoice_number()  # ex. 20200102142902

        elif self.verify_tag_by_regular_expression('[NOW_DATE_NO_SYMBOL]', tag):
            return self.__now_date()  # ex. 120820

        elif self.verify_tag_by_regular_expression('[NOW_TIME_NO_SYMBOL]', tag):
            return self.__now_time()  # ex. 162359

        elif self.verify_tag_by_regular_expression('[AUTO_GEN_??????_ID]', tag, '_??????_'):
            return self.__auto_gen_id(tag)  # ex. ROBOT202001290123456789

        elif self.verify_tag_by_regular_expression('[EXIST_??????_ID]', tag, '_??????_'):
            return self.__exist_id(tag)  # ex. ROBOT202001290123456789

        elif self.verify_tag_by_regular_expression('[AUTO_GEN_PHONE]', tag):
            return self.__auto_gen_phone()  # ex. 099999????

        elif self.verify_tag_by_regular_expression('[EXIST_PHONE]', tag, ):
            return self.__exist_phone()  # ex. 099999????

        elif self.verify_tag_by_regular_expression('[AUTO_GEN_??????]', tag, '_??????'):
            return self.__auto_gen_booking(tag)  # ex. IOS-93316074-4-055, ADR-93316074-4-055

        elif self.verify_tag_by_regular_expression('[NOW_ISO_DT]', tag):
            return self.__now_iso_datetime()  # ex. 2020-01-07T14:29:02.567Z

        elif self.verify_tag_by_regular_expression('[NOW_UTC_DT]', tag):
            return self.__now_utc_datetime()  # ex. 2020-01-07T14:29:02.567+07:00

        elif self.verify_tag_by_regular_expression('[NOW_UTC_DATE_NO_SYMBOL]{+/-}{days}D', tag, '{+/-}{days}D'):
            return self.__now_utc_date(tag, False)

        elif self.verify_tag_by_regular_expression('[NOW_UTC_DATE]{+/-}{days}D', tag, '{+/-}{days}D'):
            return self.__now_utc_date(tag)  # ex. 2020-01-17

        elif self.verify_tag_by_regular_expression('[EXIST_UTC_DT]', tag):
            return self.__exist_utc_datetime()  # ex. 2020-01-07T14:29:02.567+07:00

        elif self.verify_tag_by_regular_expression('[EXIST_ISO_DT]', tag):
            return self.__exist_iso_datetime()  # ex. 2020-01-07T14:29:02.567Z

        elif self.verify_tag_by_regular_expression('[EXIST_UTC_DATE]', tag):
            return self.__exist_utc_date()  # ex. 2020-01-17

        elif self.verify_tag_by_regular_expression('[SAVE_COOKIE??????]', tag):
            return self.__cookie_modify(tag, value)  # save cookie

        elif self.verify_tag_by_regular_expression('[SAVE??????]', tag):
            return self.__save_value(tag, value)  # save return default value (tag)

        elif self.verify_tag_by_regular_expression('[LOAD??????]', tag):
            return self.load_value(tag)  # data from [SAVE] tag (possible return multiple data type)

        elif self.verify_tag_by_regular_expression('[IMAGE-FILE]??????', tag):
            return self.__read_image_file(tag)  # image binary

        elif self.verify_tag_by_regular_expression('[QUERY:??????]', tag):
            return self.__query_database_with_tag(tag, show_log)  # first result from query

        elif self.verify_tag_by_regular_expression('[NOW_ISO8601_DT]', tag):
            return self.__now_iso8601_datetime()  # ex. 2020-01-07T14:29:02

        elif self.verify_tag_by_regular_expression('[NOW_ISO8601_DT_NO_SYMBOL]', tag):
            return self.__now_iso8601_datetime(False)  # ex. 2020-01-07T14:29:02

        elif self.verify_tag_by_regular_expression('[NOW_BPA_DT]', tag):
            return self.__now_bpa_datetime()  # ex. 20200207 14:28:02

        elif str(tag).find('[') > 0 or str(tag).find(']') < len(tag)-1:
            return self.generate_tag_inside_string(tag)  # ex. The ID is [AUTO_GEN_ROBOT_ID]

        return tag

    def __now_date(self):
        date_format = "%d%m%Y"
        now_datetime = datetime.now()
        now_timezone = pytz.timezone('Asia/Bangkok')
        now_datetime = now_timezone.localize(now_datetime)
        now_datetime = now_datetime.strftime(date_format)
        return now_datetime

    def __now_time(self):
        date_format = "%H%M%S"
        now_datetime = datetime.now()
        now_timezone = pytz.timezone('Asia/Bangkok')
        now_datetime = now_timezone.localize(now_datetime)
        now_datetime = now_datetime.strftime(date_format)
        return now_datetime

    @keyword("Load Value")
    def load_value(self, tag):
        """
        Load saved value from last [SAVE_{name}] tag used.
        """
        key = 'UNDEFINED'
        new_tag = str(tag).replace("[", "").replace("]", "")
        if str(new_tag).find('_') > -1:  # load with specific name [LOAD_{NAME}]
            temp = str(new_tag).split("_", maxsplit=1)
            key = str(temp[1])
        if str(new_tag).find('+') == -1 and str(new_tag).find('-') == -1:
            # just load [LOAD_{NAME}]
            try:
                return self.__saved[key]
            except KeyError:
                logger.error(f'not found save key: {key}')
        elif str(new_tag).find('+') > -1:
            # load data with add-on [LOAD_{NAME}]+{INT_VALUE} (support saved data type int or float)
            new_tag = str(new_tag).split("+")
            new_key = str(key).split("+")
            action_value = float(new_tag[1])
            try:
                if type(action_value) is float or type(action_value) is int:
                    result = float(self.__saved[new_key[0]]) + float(action_value)
                    return result
                else:
                    return self.__saved[new_key[0]]
            except KeyError:
                logger.error(f'not found save key: {key}')
        elif str(new_tag).find('-') > -1:
            # load data with add-on [LOAD_{NAME}]-{INT_VALUE} (support saved data type int or float)
            new_tag = str(new_tag).split("-")
            new_key = str(key).split("-")
            action_value = float(new_tag[1])
            try:
                if type(action_value) is float or type(action_value) is int:
                    result = float(self.__saved[new_key[0]]) - float(action_value)
                    return result
                else:
                    return self.__saved[new_key[0]]
            except KeyError:
                logger.error(f'not found save key: {key}')
        else:
            return self.__saved[key]

    def __now_iso8601_datetime(self, symbol=True):
        """
        2020-01-02 14:29:02
        """
        tz = pytz.timezone('Asia/Bangkok')
        value = datetime.now(tz).isoformat()
        value = value.split('.')
        value[0] = value[0].replace('T', ' ')
        if symbol is False:
            value[0] = value[0].replace('-', '').replace(':', '').replace(' ', '')
        self.__existed['ISO8601_DT'] = str(value[0])
        return str(value[0])

    def __now_bpa_datetime(self):
        """
        20200102 14:29:02
        """
        tz = pytz.timezone('Asia/Bangkok')
        value = datetime.now(tz).isoformat()
        value = value.split('.')
        value[0] = value[0].replace('T', ' ').replace('-', '')
        self.__existed['BPA_DT'] = str(value[0])
        return str(value[0])

    def __generate_invoice_number(self):
        """
        20200102142902
        """
        tz = pytz.timezone('Asia/Bangkok')
        value = datetime.now(tz).isoformat()
        value = value.split('.')
        value[0] = value[0].replace('T', ' ')
        value[0] = value[0].replace('-', '').replace(':', '').replace(' ', '')
        value[0] = value[0][0:12]
        self.__existed['AUTO_GEN_INVOICE_NO'] = str(value[0])
        return str(value[0])

    # Require fetch sql sheet with "fetch raw config" first
    def __query_database_with_tag(self, tag, show_log):
        """
        [QUERY:??????] --> query sql statement for get first result from database
        CHANGE QUERY WITH CX_ORACLE TO BE PYODBC
        """
        temp = str(tag).split(':')
        sql_name = str(temp[-1]).split(']')
        sql_name = str(sql_name[0])
        try:
            sql = self.RAW_CONFIG['sql'][sql_name]
        except Exception as ex:
            if show_log == True:
                logger.warn(f'Have no SQL match with {tag} : {ex}')
                return ""
            return tag
        sql = self.generate_tag_inside_string(sql)
        sql = sql.replace(';', '')
        db_connector = ExtendedDatabaseLibrary()
        try:
            # decode for DB_PASSWORD only
            DECODE_DB_PASSWORD = urlsafe_b64decode(self.RAW_CONFIG['setting']['DB_PASSWORD']).decode()
            DB_MODILE = "pyodbc"
            db_connector.connect_sql_server(
                DB_MODILE,
                self.RAW_CONFIG['setting']['DB_NAME'],
                self.RAW_CONFIG['setting']['DB_USERNAME'],
                DECODE_DB_PASSWORD,
                self.RAW_CONFIG['setting']['DB_HOST'],
                self.RAW_CONFIG['setting']['DB_PORT']
            )
            # db_connector.connect_sql_server(db_config_file='./db.cfg')
        except KeyError:
            raise KeyError(f'sheet setting require DB_MODULE, DB_HOST, DB_NAME, DB_USERNAME, DB_PASSWORD, DB_PORT. please check test data and try again later.')
        result = db_connector.query(sql)
        db_connector.disconnect_from_database()
        try:
            one_result = result[0]
        except IndexError:
            one_result = result
        query_name = 'QUERY_' + sql_name
        self.__saved[query_name] = one_result
        return one_result

    def __read_image_file(self, tag):
        path = str(tag).replace("[IMAGE-FILE](", "").replace(")", "")
        logger.console(f'path: {path}')
        dir_path = os.getcwd()
        logger.console(f'dir_path: {dir_path}')
        path = dir_path + path
        with open(path, "rb") as imgFile:
            return imgFile.read()

    def __cookie_modify(self, tag, value):
        """
        [SAVE_COOKIE] --> Save cookie and modify cookie data
                          For now support keys = cpmsession, pmsession and vmsession
        """
        tag = str(tag).replace("[", "").replace("]", "")
        tag = str(tag).split("_", maxsplit=1)
        cookie_name = tag[-1]
        new_cookie = ""
        value = str(self.__saved['COOKIE_LAST']) + value
        value = value.replace(";", "; ")
        value = value.strip()
        list_value = value.split(" ")
        list_value = list(dict.fromkeys(list_value))
        re_value = []
        for i in range(len(list_value)):
            if str(list_value[i]) == '': continue
            if str(list_value[i][-1]) == ';' and len(list_value[i]) > 100:
                re_value.append(list_value[i])
        for i in range(len(re_value)):
            prop = str(re_value[i]).replace(";", "")
            prop = prop.split('=')
            try:
                self.__cookies[cookie_name][str(prop[0])] = str(prop[1])
            except KeyError:
                self.__cookies[cookie_name] = self.__cookies['COOKIE']
                self.__cookies[cookie_name][str(prop[0])] = str(prop[1])
        for key in self.__cookies[cookie_name]:
            new_cookie = new_cookie + str(key) + "=" + str(self.__cookies[cookie_name][key]) + ";"
        self.__saved[cookie_name] = str(new_cookie)
        return tag

    def __save_value(self, tag, value):
        """
        [SAVE] --> Save value.
        """
        new_tag = str(tag).replace("[", "").replace("]", "")
        if str(new_tag).find('_') == -1:  # save without name [SAVE]
            key = 'UNDEFINED'
            self.__saved[key] = value
        else:
            new_tag = str(new_tag).split("_", maxsplit=1)  # save with specific name [SAVE_{NAME}]
            key = new_tag[1]
            self.__saved[key] = value
        return tag

    def __auto_gen_id(self, tag, size: int = -1):
        """
        [AUTO_GEN_{CUSTOM}_ID] --> Auto generate ID.
        """
        id_name = str(tag).split('_')
        id_name = id_name[2] if id_name[2] != 'ID]' else 'ROBOT'
        now = datetime.now()
        now = now.strftime("%Y%m%d%H%M%S%f")
        now = str(now)[0:19]
        value = id_name + now
        if size != -1:
            start = len(value) - size
            value = value[start:len(value)]
        self.__existed[id_name] = str(value)
        return value

    def __exist_id(self, tag):
        """
        [EXIST_{CUSTOM}_ID] --> Last value from [AUTO_GEN_{CUSTOM_NAME}_ID]
        """
        id_name = str(tag).split('_')
        id_name = id_name[1] if id_name[1] != 'ID]' else 'ROBOT'
        value = self.__existed[id_name]
        return value

    def __now_iso_datetime(self):
        """
        [NOW_ISO_DT] --> Generater ISO Datetime
        ex. 2020-01-07T14:29:02.567Z
        """
        value = datetime.utcnow().isoformat()
        self.__existed['ISO_DT'] = str(value)
        return value

    def __exist_iso_datetime(self):
        """
        [EXIST_ISO_DT] --> Last value from [NOW_ISO_DT]
        """
        return self.__existed['ISO_DT']

    def __now_utc_datetime(self):
        """
        [NOW_UTC_DT] --> Generate UTC Datetime
        ex. 2020-01-07T14:29:02+07:00
        """
        utc_dt = datetime.utcnow()
        utc_dt = format(utc_dt.astimezone(get_localzone()).isoformat())
        value = str(utc_dt)[0:19] + str(utc_dt)[26:32]
        self.__existed['UTC_DT'] = str(value)
        return value

    def __exist_utc_datetime(self):
        """
        [EXIST_UTC_DT] --> Last value from [NOW_UTC_DT]
        """
        return self.__existed['UTC_DT']

    # NEW
    def __exist_iso8601_datetime(self):
        """
        [EXIST_ISO8601_DT] --> Last value from [QUERY:??????]<ISO8601>
        """
        return self.__existed['ISO8601_DT']

    def __now_utc_date(self, tag, symbol=True):
        """
        [NOW_UTC_DATE] --> Generate UTC Date
        ex. 2020-01-07
        """
        date_format = "%Y-%m-%d"
        if not symbol:
            date_format = "%Y%m%d"
        now_datetime = datetime.now()
        now_timezone = pytz.timezone('Asia/Bangkok')
        now_datetime = now_timezone.localize(now_datetime)
        if str(tag).find('+') == -1 and str(tag).find('-') == -1:
            now_datetime = now_datetime
        elif str(tag).find('+') > -1:
            value = str(tag).split("+")
            num_day = int(value[1][0:-1])
            now_datetime = now_datetime + timedelta(days=num_day)
        elif str(tag).find('-') > -1:
            value = str(tag).split("-")
            num_day = int(value[1][0:-1])
            now_datetime = now_datetime - timedelta(days=num_day)
        now_datetime = now_datetime.strftime(date_format)
        self.__existed['UTC_DATE'] = str(now_datetime)
        return now_datetime

    def __exist_utc_date(self):
        """
        [EXIST_UTC_DATE] --> Last value from [NOW_UTC_DATE]
        """
        return self.__existed['UTC_DATE']

    def __auto_gen_phone(self, size: int = 10):
        """
        [AUTO_GEN_PHONE] --> Generate phone number by random last 4 numbers.
        ex. 099999????
        """
        start = 10 ** 3
        stop = (10 ** 4) - 1
        phone_num = random.randint(start, stop)  # random.randint(1000, 9999)
        phone_num = f'099999{phone_num}'
        self.__existed['PHONE'] = phone_num
        return phone_num

    def __exist_phone(self):
        """
        [EXIST_PHONE] --> Last value from [AUTO_GEN_PHONE]
        """
        return self.__existed['PHONE']

    def __auto_gen_booking(self, tag, size: int = 12):
        """
        [AUTO_GEN_{CUSTOM}] --> Generate Booking Number.
        ex. IOS-93316074-4-055
            ADR-93316074-4-055
        """
        book_type = str(tag).split('_')
        book_type = book_type[2].replace(']', '')
        start = 10 ** (size - 1)
        stop = 10 ** size - 1
        n = f"%0.{size}d" % random.randint(start, stop)  # random.randint(100000000000, 999999999999)
        book_num = f'{book_type}-{n[:8]}-{n[8:9]}-{n[9:12]}'
        self.__existed[book_type] = book_num
        return book_num

    def __exist_booking(self, tag):
        """
        [EXIST_{BOOK_TYPE}] --> Last value from [AUTO_GEN_{BOOK_TYPE}]
        """
        book_type = str(tag).split('_')
        book_type = book_type[2].replace(']', '')
        return self.__existed[book_type]

    @keyword("Get Saved Data")
    def get_saved_data(self):
        """
        Direct to get all saved data from tag generated
        """
        return self.__saved

    @keyword("Split Tags")
    def split_tags(self, tags):
        """
        Split multiple tag into list
        """
        tags = str(tags).replace(" ", "").replace("\t", "").replace("\n", "").split('][')
        for i in range(len(tags)):
            if len(tags) == 1:
                return tags
            else:
                tags[i] = str(tags[i]).strip()
                if i == 0:
                    tags[i] = tags[i] + ']'
                elif i == len(tags)-1:
                    tags[i] = '[' + tags[i]
                else:
                    tags[i] = '[' + tags[i] + ']'
        return tags

    @keyword("Generate Tag Inside String")
    def generate_tag_inside_string(self, string_with_tag):
        """
        Generate tag inside string.
        before: [AUTO_GEN_ID] is generated ID [NOW_UTC_DT]
        after:  ROBOT12345678 is generated ID 2020-01-07T14:29:02.567+07:00
        """
        inside_tags = self.get_tags_in_string(string_with_tag)
        valid_string = string_with_tag
        for inside_tag in inside_tags:
            value = str(self.generate_value_for_tag(inside_tag, None))
            valid_string = str(valid_string).replace(inside_tag, value)
        return valid_string