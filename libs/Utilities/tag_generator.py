"""
This module provides keywords to support updating dictionary by tags.
"""

import re
import copy
from robot.api.deco import keyword
from robot.api import logger
from Utilities import get_iso_datetime_tzcus
from Utilities import get_utc_datetime
from Utilities import generate_request_uid
from Utilities import get_iso_datetime_ml

TAG = 'tag'

IGNORE_TAGS = ['[IGNORES]', '[IGNORE]']
REMOVE_TAG = '[REMOVE]'
NULL_TAG = '[NULL]'
EMPTY_TAG = '[EMPTY]'
ISO_DATETIME_TZCUS_TAG = '[ISO_DATETIME_TZCUS]'
ISO_DATETIME_ML_TAG = '[ISO_DATETIME_ML]'
UTC_DATETIME_TAG = '[UTC_DATETIME]'
REQUEST_UID_PATTERN = r'^\[.*_DATE_UID\]$'

__all__ = [
    'remove_key_in_dictionary',
    'update_dictionary_by_tags']

def is_remove(value) -> bool:
    """
    Check if the tag is REMOVE.
    """
    if value == REMOVE_TAG:
        return True

def is_null(value) -> bool:
    """
    Check if the tag is NULL.
    """
    if value == NULL_TAG:
        return True

def is_empty(value) -> bool:
    """
    Check if the tag is EMPTY.
    """
    if value == EMPTY_TAG:
        return True

def is_ignores(value) -> bool:
    """
    Check if the tag is in IGNORE_TAGS
    """
    if value in IGNORE_TAGS:
        return True

def is_utc_datetime(value):
    """
    Check if the tag is UTC_DATETIME_TAG
    """
    if value == UTC_DATETIME_TAG:
        return True

def is_iso_datetime_tzcus(value):
    """
    Check if the tag is ISO_DATETIME_TZCUS
    """
    if value == ISO_DATETIME_TZCUS_TAG:
        return True

def is_iso_datetime_ml(value):
    """
    Check if the tag is ISO_DATETIME_ML_TAG
    """
    if value == ISO_DATETIME_ML_TAG:
        return True

def is_request_uid(value: str):
    """
    Check if the tag is matched the REQUEST_UID_PATTERN.

    | value = [772_DATE_UID]
    """
    if re.match(REQUEST_UID_PATTERN, value):
        return True

def recursive_update_dictionary_by_tags(my_dict, parent_dict=None, parent_key=None):
    """
    Recursive Update Dictionary By Tags.
    """
    if isinstance(my_dict, dict):
        for key, value in list(my_dict.items()):
            if isinstance(value, dict):
                recursive_update_dictionary_by_tags(value, my_dict, key)
            elif isinstance(value, list):
                for i in range(len(value)):
                    recursive_update_dictionary_by_tags(value[i], value, i)
            else:
                value = str(value)
                if is_remove(value) or is_ignores(value):
                    del my_dict[key]
                elif is_null(value):
                    my_dict[key] = None
                elif is_empty(value):
                    my_dict[key] = ''
                elif is_iso_datetime_tzcus(value):
                    my_dict[key] = get_iso_datetime_tzcus()
                elif is_utc_datetime(value):
                    my_dict[key] = get_utc_datetime()
                elif is_request_uid(value):
                    app_id = re.split(r'[\[|_|\]]', value)[1]
                    my_dict[key] = generate_request_uid(app_id)
                elif is_iso_datetime_ml(value):
                    my_dict[key] = get_iso_datetime_ml()
                else:
                    pass

@keyword(name="Remove Key In Dictionary", tags=(TAG,))
def remove_key_in_dictionary(my_dict, parent_dict=None, parent_key=None):
    """
    Remove Key from given Dictionary.
    """
    if is_empty_dict(my_dict):
        if parent_dict is not None:
            del parent_dict[parent_key]
            return True
    return False


@keyword(name="Update Dictionary By Tags", tags=(TAG,))
def update_dictionary_by_tags(my_dict):
    """
    Update dictionary by tags.

    Examples:

    | new_dict1 = | Update Dictionary By Tags | {'data': {'blueCardNumber': '[NULL]', 'cardSchema': 'VISA', 'ringId': '0317931605657959256'}} |
    | new_dict2 = | Update Dictionary By Tags | {'data': {'error': '[REMOVE]', 'message': '[REMOVE]', 'path': '[REMOVE]', 'requestId': '123e4567-e89b-42d3-a456-556642440000'}} |
    | new_dict3 = | Update Dictionary By Tags | {'data': {'KBankHeader_rqUID': '[772_DATE_UID]', 'KBankHeader_userId': 'Sudarat', 'KBankHeader_corrID': 'corrID'}} |

    =>

    | new_dict1 = {'data': {'blueCardNumber': '', 'cardSchema': 'VISA', 'ringId': '0317931605657959256'}}
    | new_dict2 = {'data': {'requestId': '123e4567-e89b-42d3-a456-556642440000'}}
    | new_dict3 = {'data': {'KBankHeader_rqUID': '772_20200701_000000000000102', 'KBankHeader_userId': 'Sudarat', 'KBankHeader_corrID': 'corrID'}}
    """
    new_dict = copy.deepcopy(my_dict)
    recursive_update_dictionary_by_tags(new_dict)
    return new_dict


def is_empty_dict(my_dict) -> bool:
    """
    Check if the dictionary is empty.
    """
    found = True
    if isinstance(my_dict, dict):
        for key in list(my_dict.keys()):
            if key:
                found = False
    if isinstance(my_dict, list):
        for i in range(len(my_dict)):
            if not is_empty_dict(my_dict[i]):
                found = False
                break
    return found
