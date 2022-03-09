from JSONLibrary import JSONLibrary
from robot.api import logger
from robot.api.deco import keyword
from urllib.parse import urlencode
from .TagGenerate import TagGenerate
from ExcelImportLibrary import ExcelImportLibrary


class DataSolution(TagGenerate, ExcelImportLibrary):
    """
    DataSolution have function about Fetch data from test data (Excel file .xlsx),
    Generate data, Verify value. and store data from test data inside.

    *Version*: 1.0.1

    *Last Updated*: 22-Sep-2020

    *Author*: Yannawat Jaengsawang

    *Email*: yannawat.j@kbtg.tech
    """

    def __init__(self):
        self.__sheetname_prevent = [
            ':', '\\', '/', '?', '*', '[', ']'
        ]
        self.__starter = {
            "indicator": {
                "key_start": None,
                "flag": None
            },
            "headers": {
                "key_start": None,
                "flag": None
            },
            "body": {
                "key_start": None,
                "flag": None
            },
            "file": {
                "key_start": None,
                "flag": None
            }
        }
        self.RAW_DATA = {
            'main': {
                'vars': {},
            },
            'req': {
                'indicator': {},
                'headers': {},
                'body': {},
                'file': {}
            },
            'res': {
                'indicator': {},
                'headers': {},
                'body': {},
                'file': {}
            }
        }
        self.RAW_CONFIG = {
            'endpoint_list': {},
            'setting': {},
            'template': {},
            'sql': {}
        }

    @keyword("Clear Data Solution")
    def clear_data_solution(self):
        """
        Clear parameters in use in data solution.
        """
        self.test_data_path = None
        self.fetch_position = None
        self.__flag = None
        self.__set_default_flag()

    @keyword("Direct Update Raw Test Data")
    def direct_update_raw_test_data(self, message_type: str, message_part: str, key_name: str, new_value):
        """
        Update value in  RAW_DATA (data dict stored test data after fectch) direcly

        *Options*

        ``message_type``: message_type of data are "req" or "res"

        ``mmessage_part``: message_part are "body" or "headers"

        ``key_name``: Keyname that need to update value

        ``new_value``: New value need to update

        *Examples*

        | `Direct Update Raw Test Data` | message_type=req | message_part=body | key_name=name | new_value=mithra |
        """
        self.RAW_DATA[message_type][message_part][key_name] = new_value

    @keyword("Open Test Data File")
    def open_test_data_file(self, path: str) -> None:
        """
        Open test data file for fetch after

        *Options*

        ``path``: Test data file path (.xlsx) that need to select

        *Examples*

        | `Open Test Data File` | ~\\Desktop\\test1_data.xlsx |
        """
        self.test_data_path = path
        self.open_excel_file(self.test_data_path)
        self.RAW_DATA = {
            'main': {
                'vars': {},
            },
            'req': {
                'indicator': {},
                'headers': {},
                'body': {},
                'file': {}
            },
            'res': {
                'indicator': {},
                'headers': {},
                'body': {},
                'file': {}
            }
        }

    def __update_group_with_properties(self, data):
        """
        Get keyname that start body group in excel (Used in Fetch Raw Test Data)

        *Options*

        ``data``: Data from find FCISDebitBankAcc cases (ExcelImportLibrary)

        *Examples*

        | `__get_keyname_start_body` | raw_data |
        """
        max_column = self.get_max_column()
        found_body = False
        position = 0
        # logger.console("__update_group_with_properties")
        for i in range(max_column):
            group_name = str(self.get_cell(1, i + 1)).lower()
            # logger.console(f'{i} > {group_name} > {self.get_cell(2, i + 1)}')
            if group_name == 'headers':
                self.__starter['headers']['key_start'] = self.get_cell(2, i + 1)
                # logger.console(f"! start headers : {self.__starter['headers']['key_start']}")
            elif group_name == 'body':
                self.__starter['body']['key_start'] = self.get_cell(2, i + 1)
                # logger.console(f"! start body : {self.__starter['body']['key_start']}")
            elif group_name == 'file':
                self.__starter['file']['key_start'] = self.get_cell(2, i + 1)
                # logger.console(f"! start file : {self.__starter['file']['key_start']}")
            elif group_name == 'indicator':
                self.__starter['indicator']['key_start'] = self.get_cell(2, i + 1)

    @keyword("Fetch Raw Config")
    def fetch_raw_config(self, sheet_name: str) -> None:
        """
        Fetch configuration data from excel sheet

        *Options*

        ``sheet_name``: sheet name that contained config data such as template, setting, endpoint_list

        *Examples*

        | `Fetch Raw Config`    | setting                   |
        | ${RAW_CONFIG}         | `Get Raw Config`          |
        | `Log to console`      | ${RAW_CONFIG['setting']}  |
        """
        self.RAW_CONFIG[sheet_name] = {}
        self.select_excel_sheet(sheet_name)
        max_row = self.get_max_row()
        max_row = max_row + 1
        for index in range(2, max_row):
            name = self.get_cell(index, 1)
            value = self.get_cell(index, 2)
            if name == None: continue
            try:
                self.RAW_CONFIG[sheet_name][name] = value
            except(IndexError):
                logger.error(IndexError)
                continue

    def __set_default_flag(self):
        self.__starter['headers']['flag'] = False
        self.__starter['body']['flag'] = False
        self.__starter['file']['flag'] = False

    def __check_data_part(self, part, key):
        part = str(part).lower()
        if self.__starter[part]['key_start'] == key or self.__starter[part]['flag']:
            self.__starter[part]['flag'] = True
            return True

    @keyword("Fetch Raw Test Data")
    def fetch_raw_test_data(self, sheet_name: str, search: str,
                            var_name_row=2, search_col=1, join_name=None) -> None:
        """
        Fetch raw test data from Excel file (.xlsx) to save into RAW_DATA

        *Options*

        ``sheet_name``: Sheet's name to start fetch ("req" or "res").

        ``search``: Search key (Search value) to find row contained test data ( in this case is Test ID = first column ).

        ``var_name_row``: Row index to contain keyname (index start with 1).

        ``search_col``: Column index to contain expected search key (index start with 1).

        ``join_name``: Used in Sub-Sheet. used in join keyname from parent column name and current column name (recursive inside).

        *Examples*

        | `Fetch Raw Test Data` | sheet_name=req | search=TC_001 | var_name_row=2 | search_col=1 | join_name=${None} |
        """

        self.select_excel_sheet(sheet_name)
        try:
            raw_data = self.find_test_case(sheet_name, search, var_name_row, search_col)
            raw_data = raw_data[0]['values']
            raw_data.pop(None, None)
        except Exception:
            logger.error(f'can not read data from sheet: {sheet_name} with ID: {search} ({Exception})')
            raise AssertionError(f'can not read data from sheet: {sheet_name} with ID: {search} ({Exception})')
        if join_name is None:  # first time join name will be None (when recusive join_name != None
            self.__update_group_with_properties(raw_data)
            self.__set_default_flag()
            # message_parth sheet ("req" or "res")
            self.fetch_position = sheet_name
        index = 1
        for key in raw_data:
            value = raw_data[key]

            # solve excel send more than use value ex. [ 'dong', '', '', '', '' ]
            if self.fetch_position != "main":
                if len(value) == 1:
                    value = value[0]
                elif value[-1] == '':
                    value = value[0]
                else:
                    value = value

            # check keyname with start body keyname or check __flag that found body already or not
            self.__check_data_part('indicator', key)
            self.__check_data_part('headers', key)
            self.__check_data_part('body', key)
            self.__check_data_part('file', key)

            # join column name to be real path
            new_key = f"{join_name}.{key}" if join_name is not None else f"{key}"
            # remove duplicate tag (res) or (req)
            new_key = str(new_key).replace('(' + self.fetch_position + ')', '')

            # condition about cell value (data in cell) and column name (* or not)
            # logger.console(f'new_key: {new_key}')
            # that column is not link just a normal value
            if new_key[-1] != '*':
                # not use first column data
                if sheet_name != self.fetch_position and index == 1:
                    pass
                else:
                    try:
                        if self.__starter['file']['flag']:
                            self.RAW_DATA[self.fetch_position]['file'][new_key] = value
                        elif self.__starter['body']['flag']:
                            self.RAW_DATA[self.fetch_position]['body'][new_key] = value
                        elif self.__starter['headers']['flag']:
                            self.RAW_DATA[self.fetch_position]['headers'][new_key] = value
                        elif self.__starter['indicator']['flag']:
                            self.RAW_DATA[self.fetch_position]['indicator'][new_key] = value
                        else:
                            # main sheet, data will append in 'vars'
                            self.RAW_DATA[self.fetch_position]['vars'][new_key] = value
                    except KeyError:
                        logger.error("Please check test data file! attritue name or group may missing.")
                        raise
            # linked data column (*), value in cell is blank (None)
            elif value is None:
                if self.__check_data_part('body', new_key):
                    self.RAW_DATA[self.fetch_position]['body'][new_key] = value
                elif self.__check_data_part('headers', new_key):
                    self.RAW_DATA[self.fetch_position]['headers'][new_key] = value
                elif self.__check_data_part('indicator', new_key):
                    self.RAW_DATA[self.fetch_position]['indicator'][new_key] = value
            # linked data column (*)
            else:
                # value in cell is "[REMOVE]"
                if value == '[REMOVE]':
                    new_key = new_key.replace('*', '')
                    if self.__check_data_part('body', new_key):
                        self.RAW_DATA[self.fetch_position]['body'][new_key] = value
                    else:
                        self.RAW_DATA[self.fetch_position]['headers'][new_key] = value
                    index = index + 1
                    continue
                # value in cell is "[IGNORE]"
                elif value == '[IGNORE]':
                    index = index + 1
                    continue
                # value in cell is "null"
                elif str(value).lower() == 'null':
                    if self.__check_data_part('body', new_key):
                        self.RAW_DATA[self.fetch_position]['body'][new_key] = value
                    else:
                        self.RAW_DATA[self.fetch_position]['headers'][new_key] = value
                    index = index + 1
                    continue
                # value in cell is "{}"
                elif value == '{}':
                    if self.__check_data_part('body', new_key):
                        self.RAW_DATA[self.fetch_position]['body'][new_key] = value
                    else:
                        self.RAW_DATA[self.fetch_position]['headers'][new_key] = value
                    index = index + 1
                    continue
                # value in cell is "[]"
                elif value == '[]':
                    if self.__check_data_part('body', new_key):
                        self.RAW_DATA[self.fetch_position]['body'][new_key] = value
                    else:
                        self.RAW_DATA[self.fetch_position]['headers'][new_key] = value
                    index = index + 1
                    continue

                # value in cell is index value "[index1,index2]" or "index1,index2"
                # prepare for recursive
                sheet_name = key[0:-1]
                for prevent in self.__sheetname_prevent:
                    find = sheet_name.find(prevent)
                    if find != -1:
                        sheet_name = sheet_name.replace(prevent, '!')
                found = str(value).find('[')
                is_list = False
                if found > -1:
                    is_list = True
                    value = str(value).replace("[", "").replace("]", "")
                value = str(value).split(",")
                sub_index = 0
                for link_value in value:
                    link_value = link_value.strip()
                    new_name = new_key.replace("*", "")
                    new_name = f"{new_name}[{sub_index}]" if is_list else new_name
                    self.fetch_raw_test_data(sheet_name, link_value,
                                             var_name_row=1, search_col=1, join_name=new_name)
                    sub_index = sub_index + 1
            index = index + 1

    @keyword("Generate Request Body With Raw Test Data")
    def generate_request_body_with_test_data(self, json_data: dict, message_type: str = 'req', message_part: str = 'body'):
        """
        Generate request body with Raw Test Data (data was collected from Fetct Raw Test Data keywords) :
        Patch template request body json with data from excel.
        Then return JSON data after re-generate with data from excel.

        *Options*

        ``json_data``: Template request body that need to re-gerante value inside (require to convert to json type before).

        ``message_type``: message_type of data is "req" or "res" (default is "req" : because res have no need to generate request body).

        ``message_part``: message_part of data is "headers" or "body" (default is "body" : because res have no need to generate request body).

        *Examples*

        | ${REQUEST_BODY} = | `Generate Request Body With Raw Test Data` | ${RAW_REQUEST_BODY} |
        """
        keys = self.RAW_DATA[message_type][message_part].keys()
        for key in keys:
            value = self.RAW_DATA[message_type][message_part][key]
            json_data = self.__update_possible_value_to_json(json_data, key, value)
        return json_data

    def __update_possible_value_to_json(self, json_data, key, value, pass_ignore: bool = True):
        """
        Update possible value to json :
        Convert some excel data in correct data and generate value from tag.

        *Options*

        ``json_data``: Template request body that need to re-gerante value inside

        ``key``: Keyname that need to update value

        ``value``: Value from ``RAW_DATA``

        ``pass_ignore``: Function need to pass when found [INGORE] tag if set false it will set blank string to value

        *Examples*

        | json_data = | `__update_posible_value_to_json` | json_data | body.name | superteemo |
        """
        # support tag (RQ) for sheetname have same with response
        key = str(key).replace('(RQ)', '').replace('*', '')
        # cover key's name with ""
        key = f'"{key}"'.replace('.', '"."')
        key = str(key).replace('[', '"[')
        key = str(key).replace(']"', ']')
        if type(value) is type(None):
            json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, '')
        elif type(value) is float or type(value) is int:
            json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, value)
        elif type(value) is bool:
            json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, value)
        elif type(value) is str:
            # [REMOVE] : remove key and value from template body
            if value == '[REMOVE]':
                json_data = JSONLibrary().delete_object_from_json(json_data, '$..' + key)
            # [IGNORE] : use default value in template body
            elif value == '[IGNORE]':
                if pass_ignore:
                    pass
                else:
                    json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, '')
            # '[] need to set empty dict
            elif value == '[]':
                json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, [])
            # [SPECIAL_TAG] : tag need to generate new value
            elif str(value).find('[') > -1 and str(value).find(']') > -1:
                try:
                    temp = self.generate_value_for_tag(value)
                    # correct tag that can generate
                    if temp != value:
                        json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, temp)
                    # update list to value ! NEW !
                    elif value[0] == '[' and value[-1] == ']':
                        value = str(value[1:-1])
                        value = str(value).split(',')
                        list_size = len(value)
                        real_list = []
                        for i in range(list_size):
                            value[i] = value[i].strip()
                            # use string value in list ( ' ' or " " )
                            if value[i].find("'") > -1 or value[i].find('"') > -1:
                                value[i] = value[i].replace("'", "").replace('"', "")
                                value[i] = str(value[i])
                            # use tag in list datatype
                            elif value[i].find('[') > -1 and value[i].find(']'):
                                value[i] = self.generate_value_for_tag(value[i])
                            # use number value in list
                            else:
                                if value[i].find('.') > -1:
                                    value[i] = float(value[i])
                                else:
                                    value[i] = int(value[i])
                            real_list.append(value[i])
                        json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, real_list)
                except Exception:
                    logger.error(f'Please check test data. may be data was set with wrong tag : {value}')
                    raise
            # 'null need to set value to null (json) or None (dict)
            elif value == 'null':
                json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, None)
            # '{} need to set empty dict
            elif value == '{}':
                json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, {})
            # "string", number : just update
            else:
                value = str(value)
                json_data = JSONLibrary().update_value_to_json(json_data, '$..' + key, value)
        return json_data

    def convert_path_to_JSONLibrary_path(self, path):
        """
        Convert path to JSONLibrary path. For solved problem duplicate fields name and multiple value (list) in json data.
        """
        path = str(path).split(".")
        new_path = "'"
        for p in path:
            if new_path == "'":
                new_path = new_path + p + "'"
            else:
                new_path = new_path + ".'" + p + "'"
        return new_path

    @keyword("Verify Data With Raw Test Data")
    def verify_data_with_raw_test_data(self, actual_data, message_type: str = 'res', message_part: str = 'body'):
        """
        Verify data with raw test data was fetch from excel file :
        In default it will verify with value in res sheet.

        *Options*

        ``actual_data``: JSON data that need to verify with raw data ``RAW_DATA``.

        ``message_type``: message_type of data ("req" or "res") (Default is "res" : because req have no need to used in verify).

        ``message_part``: message_part of data ("headers" or "body").

        *Examples*

        | ${RESULT} = | `Verify Data With Raw Test Data` | ${RESPONSE_BODY} | message_type=res | message_part=body |
        """
        expected_data = self.RAW_DATA[message_type][message_part]
        expected_keys = expected_data.keys()
        error_list = []
        self.__flag = True
        for key in expected_keys:
            expected_value = expected_data[key]
            new_key = str(key).replace('(RS)', '').replace('*', '')
            new_key = f'"{new_key}"'.replace('.', '"."')
            new_key = new_key.replace('[', '"[').replace(']"', ']')
            try:
                actual_value = JSONLibrary().get_value_from_json(actual_data, '$..' + new_key)
            except KeyError:
                raise AssertionError(f'Not found {new_key} in response body. please check key name, properties and data type inside test data and try again')
            except TypeError:
                self.__flag = False
            key_result = self.__verify_value_by_value(actual_value, expected_value)
            if not key_result:
                if len(actual_value) >= 1:
                    actual_value = actual_value[0]
                else:
                    actual_value = 'NOT FOUND'
                # logger.error(f"\"{key}\" is {actual_value} , it should be {expected_value}")
                error_list.append(f"\"{key}\" is {actual_value} , it should be {expected_value} <{key_result}>")
                self.__flag = False
        error_message = ""
        if len(error_list) > 0:
            for error in error_list:
                error_message = str(error_message) + "\n" + str(error)
        return self.__flag, str(error_message)

    def __verify_value_by_value(self, actual_value, expected_value):
        """
        Verify value by value :
        If expect value is tag format it will call TagGenerate to get verify value suddenly.

        *Options*

        ``actual_value``: Value from actual JSON

        ``expected_value``: Value from ``RAW_DATA`` (Data was fetch from Excel file)

        *Examples*

        |  result = | `__verify_value_by_value` | body.name | supertommy | supertommo |
        """
        # empty string ''
        if type(expected_value) is type(None):
            expected_value = ''
            if len(actual_value) >= 1:
                if expected_value == actual_value[0]:
                    return True
                elif type(actual_value[0]) is dict:
                    return True
            return False
        # bool
        elif type(expected_value) is bool:
            expected_value = bool(expected_value)
            if len(actual_value) >= 1:
                if expected_value == actual_value[0]:
                    return True
            return False
        # numbers
        elif type(expected_value) is float or type(expected_value) is int:
            if len(actual_value) >= 1:
                if expected_value == actual_value[0]:
                    return True
            return False
        # string or [tag]
        elif type(expected_value) is str:
            # tag [REMOVE]
            if expected_value == '[REMOVE]':
                if len(actual_value) == 0:
                    return True
                return False
            # tag [IGNORE]
            elif expected_value == '[IGNORE]':
                if len(actual_value) >= 1:
                    return True
                return False
            # 'null need to set value to null (json) or None (dict)
            elif expected_value == 'null':
                expected_value = None
                if len(actual_value) >= 1:
                    if expected_value == actual_value[0]:
                        return True
                return False
            # '{} empty dict
            elif expected_value == '{}':  # '{} empty dict
                if len(actual_value) >= 1 and type(actual_value[0]) is dict:
                    return True
                return False
            # <or> condition in string
            elif str(expected_value).find('<or>') > -1:
                expected_value = str(expected_value).split('<or>')
                for value in expected_value:
                    value = str(value).strip()
                    if len(actual_value) >= 1:
                        new_value = str(actual_value[0])
                        if value == new_value:
                            return True
                return False
            # '[] empty dict
            elif expected_value == '[]':
                if len(actual_value) >= 1 and type(actual_value[0]) is list and len(actual_value[0]) == 0:
                    return True
                return False
            elif str(expected_value).find('[') > -1 and str(expected_value).find(']') > -1:
                if len(actual_value) >= 1:

                    # tag [SAVE...]
                    if str(expected_value).find('[SAVE') > -1 and str(expected_value).find(']') == len(expected_value)-1:
                        self.generate_value_for_tag(expected_value, actual_value[0])
                        return True

                    # tag [LOAD...]
                    elif str(expected_value).find('[LOAD') > -1 and str(expected_value).find(']') == len(expected_value)-1:
                        expected_value = self.generate_value_for_tag(expected_value, actual_value[0])
                        if type(expected_value) is float or type(expected_value) is int:
                            expected_value = float(expected_value)
                            actual_value[0] = float(actual_value[0])
                        if expected_value == actual_value[0]:
                            return True

                    else:

                        # tag [AUTO_GEN...]
                        temp = expected_value
                        expected_value = self.generate_value_for_tag(expected_value, actual_value[0])
                        if str(expected_value) == str(actual_value[0]):
                            return True

                        # ['a', 10] datatype=list, not tag
                        else:
                            expected_value = str(expected_value).replace('[', '').replace(']', '')
                            expected_value = str(expected_value).split(',')
                            list_size = len(expected_value)
                            check_status = True
                            for i in range(list_size):
                                expected_value[i] = expected_value[i].strip()
                                try:
                                    if type(expected_value[i]) is float or type(expected_value[i]) is int:
                                        actual_value[0][i] = float(actual_value[0][i])
                                        expected_value[i] = float(expected_value[i])
                                    else:
                                        expected_value[i] = expected_value[i].replace("'", "")
                                    if expected_value[i] != actual_value[0][i]:
                                        check_status = False
                                except TypeError:
                                    check_status = False
                            return check_status

                    return expected_value

                return False

            # verify string with regular expression
            elif str(expected_value).find("??????") > -1:
                if len(actual_value) >= 1:
                    if self.verify_tag_by_regular_expression(expected_value, actual_value[0], "??????"):
                        return True
                return False

            # "string" normal
            else:
                if len(actual_value) >= 1:
                    if expected_value == actual_value[0]:
                        return True
                return False
        return False

    @keyword("Generate Request Headers From Raw Test Data")
    def generate_request_headers_with_raw_test_data(self, message_type: str = 'req', message_part: str = 'headers'):
        """
        Generate headers from raw test data

        *Options*

        ``message_type``: message_type of data ("req")

        ``message_part``: message_part of data ("headers")

        *Examples*

        | ${REQUEST_HEADERS} = | `Generate Request Headers From Raw Test Data` |
        """
        new_headers = self.RAW_DATA[message_type][message_part].copy()
        keys = self.RAW_DATA[message_type][message_part].keys()
        for key in keys:
            value = self.RAW_DATA[message_type][message_part][key]
            # if str(key).lower() == "cookie":
            #     cookie_value = self.generate_value_for_tag(tag=value)
            #     # logger.console(f'SAVE_COOKIE_LAST << {cookie_value}')
            #     self.generate_value_for_tag(tag="[SAVE_COOKIE_LAST]", value=str(cookie_value))
            new_headers = self.__update_possible_value_to_json(new_headers, key, value, pass_ignore=False)
        return new_headers

    @keyword("Get Raw Test Data")
    def get_raw_test_data(self):
        """
        Get Raw Test Data :
        Need to Fetch Raw Test Data first

        *Examples*

        | ${RAW_DATA} = | `Get Raw Test Data` |
        """
        return self.RAW_DATA

    @keyword("Get Raw Config")
    def get_raw_config(self):
        """
        Get Raw Config dict that use to `Fetch Raw Config` before

        *Examples*

        | ${RAW_CONFIG} = | `Get Raw CONFIG` |
        """
        return self.RAW_CONFIG

    @keyword("Generate Value For Tag In Meta")
    def generate_value_for_tag_in_meta(self, meta_string):
        """
        Generate value for tag in meta
        ex1. \"<<req:body:name>>\"      = use value in same row (same test data)
        ex2. \"<<[EXIST_PARTNER_ID]>>\" = generate tag to use in meta
        *Examples*

        | ${RAW_CONFIG} = | `Get Raw CONFIG` |
        """
        find_front = str(meta_string).find("<<")
        find_rear = str(meta_string).find(">>")
        while find_front != -1 or find_rear != -1:
            temp = str(meta_string).split("<<", maxsplit=1)
            temp = str(temp[1]).split(">>", maxsplit=1)
            key_focus = temp[0]
            if key_focus[0] == '[' and key_focus[-1] == ']':
                meta_string = str(meta_string).replace(
                    '<<' + key_focus + '>>',
                    self.generate_value_for_tag(
                        key_focus,
                        None
                    )
                )
            else:
                split_focus = key_focus.split(":")
                split_focus[0] = str(split_focus[0]).lower()
                split_focus[1] = str(split_focus[1]).lower()
                meta_string = str(meta_string).replace(
                    '<<' + key_focus + '>>',
                    self.generate_value_for_tag(
                        self.RAW_DATA[split_focus[0]][split_focus[1]][split_focus[2]],
                        None
                    )
                )
            find_front = str(meta_string).find("<<")
            find_rear = str(meta_string).find(">>")
        return meta_string

    @keyword("Generate Value For Tag In String")
    def generate_value_for_tag_in_string(self, string, open='[', close=']'):
        """
        Generate value from string tag.
        """
        tags = self.get_tags_in_string(string)
        for tag in tags:
            value = self.generate_value_for_tag(tag, None)
            string = str(string).replace(tag, value)
        return string