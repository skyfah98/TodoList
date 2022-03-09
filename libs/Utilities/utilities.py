""" 
This module provides utility keywords.
"""

import os
from os.path import isfile, join
import re
from json import loads
from dictdiffer import diff
from robot.api import logger
import requests
from robot.api.deco import keyword
from datetime import date
from random import randint

TAG = 'utilities'
__all__ = ['load_json_from_file',
           'verify_text_with_regEx',
           'get_list_testdata',
           'upload_image_without_data',
           'generate_request_uid']


@keyword(name="Load JSON From File", tags=(TAG,))
def load_json_from_file(file_path):
    """Loads and returns json from a given file."""
    return loads(open(file_path, encoding='utf-8').read())


def print_friendly_message(result):
    """
    Customize returning message after comparing the value between two dictionaries.

    Result: The result after comparing two dictionaries.
    """
    try:
        message = ""
        for arr in result:
            msg = ""
            if str(arr[0]) == 'change':
                elements = ""
                flags = False
                if isinstance(arr[1], str):
                    msg = "The value of \"{}\" is changed from \"{}\" to \"{}\"\n".format(str(arr[1]), str(arr[2][0]),
                                                                                          str(arr[2][1]))
                elif isinstance(arr[1], list):
                    narr = arr[1]
                    for i in range(len(narr)):
                        elements += str(narr[i]) + "."
                        if isinstance(narr[i], int):
                            flags = True
                            list1 = narr[0:i]
                            for j in range(len(list1)):
                                nlist1 = ".".join(list1)
                            list2 = narr[i + 1:]
                            for k in range(len(list2)):
                                nlist2 = ".".join(list2)
                            msg = "The value of \"{}\" at index \"{}\" of \"{}\" is changed from \"{}\" to \"{}\"\n".format(
                                nlist2, narr[i], nlist1, str(arr[2][0]), str(arr[2][1]))
                            break
                    if flags == False:
                        elements = elements[:-1]
                        msg = "The value of \"{}\" is changed from \"{}\" to \"{}\"\n".format(elements, str(arr[2][0]),
                                                                                              str(arr[2][1]))
            elif str(arr[0]) == "remove":
                if str(arr[1]) == "":
                    msg = "The attribute \"{}\" is removed from actual result\n".format(str(arr[2][0][0]))
                elif isinstance(arr[1], list):
                    msg = "The attribute \"{}\" at index \"{}\" of \"{}.{}\" is removed into actual result\n".format(
                        str(arr[2][0][0]), str(arr[1][2]), str(arr[1][0]), str(arr[1][1]))
                else:
                    msg = "The attribute \"{}.{}\" is removed from actual result\n".format(str(arr[1]),
                                                                                           str(arr[2][0][0]))
            elif str(arr[0]) == "add":
                if str(arr[1]) == "":
                    msg = "The attribute \"{}\" is added into actual result\n".format(str(arr[2][0][0]))
                elif isinstance(arr[1], list):
                    msg = "The attribute \"{}\" at index \"{}\" of \"{}.{}\" is added into actual result\n".format(
                        str(arr[2][0][0]), str(arr[1][2]), str(arr[1][0]), str(arr[1][1]))
                else:
                    msg = "The attribute \"{}.{}\" is added into actual result\n".format(str(arr[1]), str(arr[2][0][0]))
            message += msg
        message = message[:-1]
        return message
    except Exception as e:
        logger.error('Print Message Value method: ' + str(e))


def check_type(actual, expect):
    try:
        diffs = list(diff(expect, actual))
        diffs = list(d for d in diffs if d[0] == 'change')
        for d in diffs:
            if isinstance(d[2][0], (dict, list)) or isinstance(d[2][1], (dict, list)):
                if type(d[2][0]) != type(d[2][1]):
                    raise AssertionError(
                        "Check Type method: Two dictionaries have different Format: type of \"{}\" is {} in actual result while it is {} in expected result.".format(
                            d[1], type(d[2][1]), type(d[2][0])))
    except Exception as e:
        raise AssertionError("Check Type method: " + str(e))


@keyword(name="Verify Text With RegEx", tags=(TAG,))
def verify_text_with_regEx(expected: str, actual: str, conj="??????") -> bool:
    """
    Verify expected text with regular expression that have conjunction is ${conj}.\n
    Return type: bool
    """
    expected = str(expected).replace("[", "\[")
    expected = str(expected).replace("]", "\]")
    expected = str(expected).replace("(", "\(")
    expected = str(expected).replace(")", "\)")
    expected = str(expected).replace(".", "\.")
    expected = str(expected).split(conj)
    size = len(expected)
    ex_reg = ''
    for i in range(size):
        if i == 0:
            ex_reg = '^' + ex_reg + expected[i] + '.*'
        elif i == size - 1:
            ex_reg = ex_reg + expected[i]
        else:
            ex_reg = ex_reg + expected[i] + '.*'
    result = re.search(ex_reg, actual)
    if result:
        return True
    else:
        return False


@keyword(name="Get File List As Same Type", tags=(TAG,))
def get_list_testdata(path: str, filetype: str) -> list:
    """
    Get a file list as same type from the path given.

    Return Type: List
    """
    all_files = [
        f for f in os.listdir(f'{path}/') if isfile(
            join(f"{path}", f)
        )
    ]
    only_files = []
    for file in all_files:
        filename = file
        file = str(file).split('.')
        if file[1] == filetype and file[0][0] != '~':
            only_files.append(filename)
    return only_files


@keyword(name="Upload Image Without Data", tags=(TAG,))
def upload_image_without_data(url, filepath):
    """
    Upload an image without data from the path given.

    Example:

    | Upload Image Without Data | http://localhost:8080/APP/API | Images/image1.png |

    Return: HTML Status Code (Ex: 200, 400, 500 . . .)
    """
    files = {'media': open(filepath, 'rb')}
    response = requests.post(url, files=files, verify=False)
    return response.status_code


@keyword(name="Generate Request UID", tags=(TAG,))
def generate_request_uid(app_id) -> str:
    """
*Format*: <Application ID in Kbank's Application Portfolio>_<System Date YYYYMMDD>_<Unique ID>

1. RqUID is propagated through the chain of systems involved in a transaction.

2. If an intermediary cannot propagate the RqUID, it must maintain a correlation between original RqUID and new RqUID in its audit trails.

3. Unique ID needs to be unique for one application for one day.

    *Argument*:

    - ``app_id``: Application ID of project

    Example:

    | request_uid = | Generate Request UID |

    =>

    | request_uid = 772_20200701_000000000000102

    """
    try:
        today = date.today()
        system_date = today.strftime("%Y%m%d")
        range_start = 10 ** (15 - 1)
        range_end = (10 ** 15) - 1
        randint(range_start, range_end)
        unique_id = randint(range_start, range_end)
        return str(app_id) + "_" + str(system_date) + "_" + str(unique_id)
    except Exception as info:
        logger.error(f"{__name__} Can not generate request uid : {info}")
        raise
