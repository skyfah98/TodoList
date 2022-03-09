"""
This module provides keywords to support dictionary-like processing.
"""
import copy
from datetime import datetime, time, date
from decimal import Decimal
from operator import itemgetter
from dictdiffer import diff
from robot.api.deco import keyword
from robot.api import logger
from .utilities import print_friendly_message, check_type

TAG = 'dict'
__all__ = [
    'verify_response_body',
    'update_data_into_original_dictionary',
    'convert_suds_object_to_dict',
    'update_the_value_for_the_key_list',
    'update_the_value_for_selected_key',
    'get_the_value_for_selected_key',
    'get_keys',
    'get_list_diffs',
    'delete_key_in_dictionary',
    'update_value_from_original_dictionary',
    'update_the_value_for_the_key_list_to_decimal',
    'update_the_value_for_selected_key_to_decimal',
    'validate_response_body']


@keyword(name="Verify Response Body", tags=(TAG,))
def verify_response_body(actual, expect, ignores=None, nonignores=None, check_key=True, check_datatype=True,
                         check_value=True):
    """Verify an actual result against an expected result.

    *Options*

    - ``ignores``: the field list which you want to ignore in case of verifying lots of keys.

    - ``nonignores``: the field list which you want to verify in case of verifying few keys.

    - ``check_key``: If false, skips a comparison about key between actual response and expected response.

    - ``check_datatype``: If false, skips a comparison about datatype between actual response and expected response.

    - ``check_value``: If false, skips any value validations for all keys.

    Arguments:

    - ``actual``: Should be the actual response.

    - ``expect``: Should be the expected response.

    Examples:

    | Verify Response Body | {data: {rsUUID: asdfg1234hjkl5678, rsDt: 2020-02-20 20:02:20, accName: KBANK, accNumber: 123456, accAmount: 360.00, transactionAmt: 60.50}} | {data: {rsUUID: asdfg4321hjkl8765, rsDt: 2020-02-20 02:20:02, accName: KBANK, accNumber: 123456, accAmount: 360.00, transactionAmt: 60.50}} | ignores = {data.rsUUID, data.rsDt} | |
    | Verify Response Body | {data: {rsUUID: asdfg1234hjkl5678, rsDt: 2020-02-20 20:02:20, accName: KBANK, accNumber: 123456, accAmount: 360.00, transactionAmt: 60.50}} | {data: {rsUUID: asdfg4321hjkl8765, rsDt: 2020-02-20 02:20:02, accName: KBANK, accNumber: 123456, accAmount: 630.00, transactionAmt: 50.60}} | nonignores = {data: {accName: null, accNumber: null}} | |
    | Verify Response Body | {data: {rsUUID: asdfg1234hjkl5678, rsDt: 2020-02-20 20:02:20, accName: KBANK, accNumber: 123456, accAmount: 360.00}} | {data: {rsUUID: asdfg4321hjkl8765, rsDt: 2020-02-20 02:20:02, accName: KBANK, accNumber: 123456, accAmount: 360.00, transactionAmt: 60.50}} | ignores = {data.rsUUID, data.rsDt} | |
    | Verify Response Body | {data: {rsUUID: asdfg1234hjkl5678, rsDt: 2020-02-20 20:02:20, accName: KBANK, accNumber: 123456, accAmount: 360.00, transactionAmt: 60.50}} | {data: {rsUUID: asdfg4321hjkl8765, rsDt: 2020-02-20 02:20:02, accName: KBANK, accNumber: 654321, accAmount: 630.00, transactionAmt: 50.60}} | nonignores = {data: {accName: null, accNumber: null}} | |
    | Verify Response Body | {data: {rsUUID: asdfg1234hjkl5678, rsDt: 2020-02-20 20:02:20, accName: KBANK, accNumber: 123456, accAmount: 360.00}} | {data: {rsUUID: asdfg4321hjkl8765, rsDt: 2020-02-20 02:20:02, accName: KBANK, accNumber: 123456, accAmount: 630.00, transactionAmt: 50.60}} | nonignores = {data: {accName: null, accNumber: null}} | check_key = False |

    =>

    The attribute "data.transactionAmt" is removed into actual result.\n
    The value of "data.accNumber" is changed from "123456" to "654321".
    """
    diffs = get_dict_diffs(actual, expect, ignores, nonignores, check_key, check_datatype, check_value)
    if diffs:
        raise AssertionError(print_friendly_message(diffs))


def get_dict_diffs(actual, expect, ignores=None, nonignores=None, check_key=True, check_datatype=True,
                   check_value=True):
    """
    Compare the value between two dictionaries and return the change between two dictionaries.

    Arguments:

    - ``actual``: the actual dictionary.

    - ``expected``: the expected dictionary.

    - ``ignores``: the field list which you want to ignore in case of verifying lots of keys.

    - ``nonignores``: the field list which you want to verify in case of verifying few keys.

    - ``check_key``: set to False if you don't want to compare keys between two dicts.

    - ``check_datatype``: set to False if you don't want to compare datatype between two dicts.

    - ``check_value``: set to False if you don't want to verify value for all keys.
    """
    logger.debug("This is expected result:\n")
    logger.debug(expect)
    logger.debug("This is actual result:\n")
    logger.debug(actual)
    if check_datatype:
        check_type(actual, expect)
    diffs = list()
    if check_value:
        if ignores and isinstance(ignores, list):
            logger.debug("This is ignore list:\n")
            logger.debug(ignores)
            key_diffs = []
            if check_key:
                key_diffs = list(diff(expect, actual))
                key_diffs = list(d for d in key_diffs if (d[0] == 'add' or d[0] == 'remove'))
            try:
                value_diffs = list(diff(expect, actual, ignore=set(ignores)))
            except TypeError:
                value_diffs = list(diff(expect, actual, ignore=ignores))
            value_diffs = list(d for d in value_diffs if d[0] == 'change')
            diffs = key_diffs + value_diffs
        elif ignores and isinstance(ignores, dict):
            raise AssertionError("Currently inputting ignores as dict is not supported")
        elif nonignores:
            logger.debug("This is the nonignore list:\n")
            logger.debug(nonignores)
            key_diffs = []
            if check_key:
                key_diffs = list(diff(expect, actual))
                key_diffs = list(d for d in key_diffs if (d[0] == 'add' or d[0] == 'remove'))
            del_expected = update_value_from_original_dictionary(expect, nonignores)
            del_actual = update_value_from_original_dictionary(actual, nonignores)
            value_diffs = list(diff(del_expected, del_actual))
            value_diffs = list(d for d in value_diffs if d[0] == 'change')
            diffs = key_diffs + value_diffs
        else:
            diffs = list(diff(expect, actual))
    logger.debug("This is the diff list:\n")
    logger.debug(diffs)
    return diffs


@keyword(name="Update Data Into Original Dictionary", tags=(TAG,))
def update_data_into_original_dictionary(original_source, overrides):
    """
    Update data into original dictionary.

    Arguments:

    - ``original_source``: the original dictionary (get from the sample response).

    - ``overrides``: the dictionary with the key which you want to update new value.

    Examples:

    | new_dict1 = | Update Data Into Original Dictionary | {data: {funcName: API123, appId: 222, accountNumber: null}} | {data: {accountNumber: 123456} |
    | new_dict2 = | Update Data Into Original Dictionary | {data: {funcName: API123, appId: 222, accountName: null, accountNumber: null}} | {data: {accountName: KBANK, accountNumber: 123456} |

    =>

    | new_dict1 = {data: {funcName: API123, appId: 222, accountNumber: 123456}}
    | new_dict2 = {data: {funcName: API123, appId: 222, accountName: KBANK, accountNumber: 123456}}
    """
    source = copy.deepcopy(original_source)
    if (overrides is not None) and (overrides != ''):
        result = recursive_update_data_into_original_dictionary(source, overrides)
    else:
        result = source
    return result


def recursive_update_data_into_original_dictionary(source, overrides):
    """
    Returns new dictionary after updating the values of ``overrides`` into ``source`` with the corresponding key.\n
    This keyword can update with multiple levels in dictionary.
    """
    for key, value in overrides.items():
        if isinstance(value, dict):
            recursive_update_data_into_original_dictionary(source.get(key, {}), value)
        elif isinstance(value, list):
            for i in range(len(value)):
                recursive_update_data_into_original_dictionary(source.get(key)[i], value[i])
        else:
            if key not in source:
                raise AssertionError(key + " does not exist.")
            else:
                source[key] = overrides[key]
    return source


@keyword(name="Convert Subs Object to Dictionary", tags=(TAG,))
def convert_suds_object_to_dict(my_suds):
    """Converts a suds object to dictionary."""
    logger.debug("Before converting:\n")
    logger.debug(my_suds)
    result = recursive_convert_suds_object_to_dict(my_suds)
    logger.debug("After converting:\n")
    logger.debug(result)
    return result


def recursive_convert_suds_object_to_dict(obj):
    """Converts a suds object to a dict."""
    if not hasattr(obj, '__keylist__'):
        if isinstance(obj, (datetime, time, date)):
            return obj.isoformat()
        else:
            return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if isinstance(val, list):
            data[field] = []
            for item in val:
                data[field].append(recursive_convert_suds_object_to_dict(item))
        else:
            data[field] = recursive_convert_suds_object_to_dict(val)
    return data


@keyword(name="Update The Value For The Key List", tags=(TAG,))
def update_the_value_for_the_key_list(mydic, keys, values):
    """
    Update new value for the key list from the dictionary and return the dictionary with new value.

    Arguments:

    - ``mydic``: the dictionary which you want to change.

    - ``keys``: the key list which you want to update a new value.

    - ``values``: the value list which you need to update.

    Example:

    | new_dict = | Update The Value For The Key List | {data: {funcName: API123, appId: 222, accName: KBANK, accNumber: 123456, accAmount: null, transactionAmt: null}} | {accName, accNumber, accAmount, transactionAmt} | {KSOFT, 78901, 360.50, 60.50} |

    =>

    | new_dict = {data: {funcName: API123, appId: 222, accName: KSOFT, accNumber: 78901, accAmount: 360.50, transactionAmt: 60.50}}
    """
    try:
        i = 0
        for key in keys:
            mydic = update_the_value_for_selected_key(mydic, key, values[i])
            i += 1
        return mydic
    except Exception as e:
        logger.error('Update The Value For The Key List method: ' + str(e))


@keyword(name="Update The Value For Selected Key", tags=(TAG,))
def update_the_value_for_selected_key(mydic, keyid, valueid):
    """Update the value for selected key.

    Example:

    | new_dict = | Update The Value For Selected Key | {data: {funcName: API123, appId: 222, accName: KBANK, accNumber: 123456}} | accNumber | 78901 |

    =>

    | new_dict = {data: {funcName: API123, appId: 222, accName: KBANK, accNumber: 78901}}
    """
    source = copy.deepcopy(mydic)
    result = recursive_update_the_value_for_selected_key(source, keyid, valueid)
    return result

def recursive_update_the_value_for_selected_key(mydic, keyid, valueid):
    """
    Update new value for selected key from the dictionary and return the dictionary with new value.

    Argument:

    - ``mydic`` the dictionary which you want to change.

    - ``keyid`` the key which you want to update a new value.

    - ``valueid`` the value which you need to update.
    """
    try:
        for key, value in mydic.items():
            if isinstance(value, dict):
                recursive_update_the_value_for_selected_key(value, keyid, valueid)
            elif isinstance(value, list):
                for i in range(len(value)):
                    recursive_update_the_value_for_selected_key(value[i], keyid, valueid)
            elif key == keyid:
                mydic[key] = valueid
        return mydic
    except Exception as e:
        logger.error('Update The Value For Selected Key method: ' + str(e))


@keyword(name="Get The Value For Selected Key", tags=(TAG,))
def get_the_value_for_selected_key(mydict, keyid):
    """
    Get the value for selected key.

    Arguments:

    - ``mydict``: the dictionary which you want to change.

    - ``keyid``: the key which you want to get the value.

    Example:

    | myvalue = | Get The Value For Selected Key | {data: {funcName: API123, appId: 222, accName: KBANK, accNumber: 123456}} | accNumber |

    =>

    | myvalue = 123456
    """
    try:
        myvalue = None
        if isinstance(mydict, dict):
            for a_k, a_v in mydict.items():
                if isinstance(a_v, dict):
                    myvalue = get_the_value_for_selected_key(a_v, keyid)
                elif isinstance(a_v, list):
                    for i in range(len(a_v)):
                        myvalue = get_the_value_for_selected_key(a_v[i], keyid)
                else:
                    if a_k == keyid:
                        myvalue = mydict[keyid]
                        break
        # Using list comprehension
        # Get values of particular key in list of dictionaries
        elif isinstance(mydict, list):
            myvalue = map(itemgetter(keyid), mydict)
        else:
            myvalue = ""
        return myvalue
    except Exception as e:
        logger.error('Get The Value For Selected Key From The Response method: ' + str(e))


@keyword(name="Get Keys", tags=(TAG,))
def get_keys(mydict):
    """
    Get all keys in the dictionary including main dictionary and nested dictionary.

    Argument:

    ``mydict``: the dictionary which you want to get the key.

    Example:

    | mylist = | Get Keys | {api: {funcName: API123, appId: 222, account: {accName: KBANK, accNumber: 123456}, transfer: { data: {dateTransfer: 20200220, amtTranfer: 50}}}} |

    =>

    | mylist = funcName, appId, account, accName, accNumber, transfer, dateTransfer, amtTranfer
    """
    try:
        if isinstance(mydict, dict):
            for k, v in mydict.items():
                if isinstance(v, dict):
                    yield k
                    yield from get_keys(v)
                elif isinstance(v, list):
                    for i in v:
                        yield from get_keys(i)
                else:
                    yield k
        elif isinstance(mydict, list):
            for i in mydict:
                yield from get_keys(i)
    except Exception as e:
        logger.error('Get Keys method: ' + str(e))


@keyword(name="Get List Diffs", tags=(TAG,))
def get_list_diffs(list1, list2):
    """
    Custom python code to check if list one is equal to list two by taking difference.

    Arguments:

    - ``list1``: the comparing list.

    - ``list2``: the standard list.

    Example:

    | list_dif = | Get List Diffs | {10, 15, 20, 25, 30, 35, 40} | {25, 40, 35} |

    =>

    | list_dif = False
    """
    try:
        list_dif = [i for i in list1 if i not in list2]
        return list_dif
    except Exception as e:
        logger.error('Get Difference Between Two Lists method: ' + str(e))


@keyword(name="Delete Key In Dictionary", tags=(TAG,))
def delete_key_in_dictionary(original_source, key):
    """Delete the key in dictionary which you want.

    Example:

    | result = | Delete Key In Dictionary | {api: {funcName: API123, appId: 222, account: {accName: KBANK, accNumber: 123456}}} | accNumber |

    =>

    | result = {api: {funcName: API123, appId: 222, account: {accName: KBANK}}}
    """
    source = copy.deepcopy(original_source)
    result = recursive_delete_key_in_dictionary(source, key)
    return result


def recursive_delete_key_in_dictionary(source, key_delete):
    """
    Returns new dictionary after removing key-value in the original dictionary.

    Argument:

    - ``source`` Original dictionary.

    - ``key_delete`` Key name need to delete.
    """
    for key, value in source.items():
        if isinstance(value, dict):
            recursive_delete_key_in_dictionary(value, key_delete)
        elif key_delete in source:
            source.pop(key_delete)
            break
    return source


@keyword(name="Update Value From Original Dictionary", tags=(TAG,))
def update_value_from_original_dictionary(source, source_target):
    """Update the value from original dictionary.

    Examples:

    | new_dict = | Update Data Into Original Dictionary | {api: {funcName: API123, appId: 222, account: {accName: KBANK, accNumber: 123456}, transfer: { data: {dateTransfer: 20200220, amtTranfer: 50}}}} | {data: {account: {accName: null, accNumber: null}, transfer: { data: {amtTranfer: null}}}} |

    =>

    | new_dict = {data: {account: {accName: KBANK, accNumber: 123456}, transfer: { data: {amtTranfer: 50}}}}
    """
    try:
        target = copy.deepcopy(source_target)
        logger.debug("Source:\n")
        logger.debug(source)
        logger.debug("Target:\n")
        logger.debug(target)
        check_type(source, target)
        result = recursive_update_value_from_original_dictionary(source, target)
        logger.debug("Result:\n")
        logger.debug(result)
        return result
    except Exception as e:
        raise AssertionError("Update Value From Original Dictionary: " + str(e))


def recursive_update_value_from_original_dictionary(source, target):
    """
    Update the value from the original dictionary to the standard dictionary which has required keys.

    This method can update with multiple levels in the dictionary.
    """
    try:
        for key, value in target.items():
            if isinstance(value, dict):
                recursive_update_value_from_original_dictionary(source.get(key, {}), value)
            elif isinstance(value, list):
                for i in range(len(value)):
                    if not isinstance(value[i], str):
                        recursive_update_value_from_original_dictionary(source.get(key)[i], value[i])
                    else:
                        target[key] = source[key]
            else:
                target[key] = source[key]
        return target
    except Exception as e:
        logger.error('Recursive Update Value From Original Dictionary method: ' + str(e))


@keyword(name="Update The Value For The Key List To Decimal", tags=(TAG,))
def update_the_value_for_the_key_list_to_decimal(mydict, keys):
    """
    Update type of value from string to decimal for the key list from the dictionary and return the dictionary.

    Arguments:

    - ``mydic``: the dictionary which you want to change.

    - ``keys``: the key list which you want to convert type of value from string to decimal.

    Example:

    | new_dict = | Update The Value For Selected Key | {data: {funcName: API123, appId: 222, accName: KBANK, accAmount: '1,234', amtTranfer: '3.14'}} | {accAmount, amtTranfer} |

    =>

    | new_dict = {data: {funcName: API123, appId: 222, accName: KBANK, accAmount: Decimal('1234'), amtTranfer: Decimal('3.14')}}
    """
    try:
        for key in keys:
            mydict = update_the_value_for_selected_key_to_decimal(mydict, key)
        return mydict
    except Exception as e:
        logger.error('update The Value For The Key List To Decimal method: ' + str(e))


@keyword(name="Update The Value For Selected Key List To Decimal", tags=(TAG,))
def update_the_value_for_selected_key_to_decimal(mydic, keyid):
    """
    Update the value to decimal format for selected key. This keyword do not effect to data in mydic.
    And it return a new dictionary.

    Arguments:

    - ``mydic``: the dictionary which you want to change.

    - ``keyid``: the key which you want to convert the value from string to decimal.

    Example:

    | new_dict = | Update The Value For Selected Key | {data: {funcName: API123, appId: 222, accName: KBANK, accAmount: '1,234'}} | accAmount |

    =>

    | new_dict = {data: {funcName: API123, appId: 222, accName: KBANK, accAmount: Decimal('1234')}}
    """
    source = copy.deepcopy(mydic)
    result = recursive_update_the_value_for_selected_key_to_decimal(source, keyid)
    return result


def recursive_update_the_value_for_selected_key_to_decimal(mydict, keyid):
    """
    Update the value to decimal format for selected key. Return the dictionary with
    type of value for the selected key from string to decimal.

    Arguments:

    - ``mydict`` the dictionary which you want to change.

    - ``keyid`` the key which you want to convert the value from string to decimal.
    """
    try:
        myvalue = None
        if isinstance(mydict, dict):
            for a_k, a_v in mydict.items():
                if isinstance(a_v, dict):
                    myvalue = recursive_update_the_value_for_selected_key_to_decimal(a_v, keyid)
                elif isinstance(a_v, list):
                    for i in range(len(a_v)):
                        myvalue = recursive_update_the_value_for_selected_key_to_decimal(a_v[i], keyid)
                else:
                    if a_k == keyid:
                        myvalue = mydict[keyid]
                        mydict[keyid] = Decimal(myvalue.replace(',', ''))
        return mydict
    except Exception as e:
        logger.error('Update The Value For Selected Key To Decimal method: ' + str(e))


@keyword(name="Validate Response Body", tags=(TAG,))
def validate_response_body(actual, expect, ignores=None, nonignores=None, check_key=True, check_datatype=True,
                           check_value=True):
    """Created By Thai Team

    Verify an actual result against an expected result.

    *Options*

        ``actual``: the actual dictionary.

        ``expected``: the expected dictionary.

        ``ignores``: in case of verifying lots of keys the field list which you want to ignore.

        ``nonignores``: in case of verifying few keys that the field list which you want to verify.

        ``check_key``: set to False if you don't want to compare keys between two dicts.

        ``check_datatype``: set to False if you don't want to compare datatype between two dicts.

        ``check_value``: set to False if you don't want to compare value between two dicts.

        *Examples*

        | `Validate_Response_Body` | actual | expect |
        | `Validate_Response_Body` | actual | expect | ignores=data.activities |
        | `Validate_Response_Body` | actual | expect | nonignores=${VALIDATE.getAccountBalances} |
        | `Validate_Response_Body` | actual | expect | check_key=False |
        | `Validate_Response_Body` | actual | expect | check_datatype=False |
        | `Validate_Response_Body` | actual | expect | check_value=False |
    """

    diffs = get_diffs(actual, expect, ignores, nonignores, check_key, check_datatype, check_value)
    if diffs:
        raise AssertionError(print_friendly_message(diffs))


def get_diffs(actual, expect, ignores=None, nonignores=None, check_key=True, check_datatype=True, check_value=True):
    """
    Compare the value between two dictionaries and return the change between two dictionaries.

    actual: the actual dictionary
    expected: the expected dictionary
    ignores: in case of verifying lots of keys the field list which you want to ignore
    nonignores: in case of verifying few keys that the field list which you want to verify
    check_key: set to False if you don't want to compare keys between two dicts
    check_datatype: set to False if you don't want to compare datatype between two dicts
    """
    logger.debug("This is expected result:\n")
    logger.debug(expect)
    logger.debug("This is actual result:\n")
    logger.debug(actual)
    if check_datatype:
        check_type(actual, expect)
    diffs = list()
    if check_value:
        if ignores and isinstance(ignores, list):
            logger.debug("This is ignore list:\n")
            logger.debug(ignores)
            key_diffs = []
            if check_key:
                key_diffs = list(diff(expect, actual, ignore=set(ignores)))
                key_diffs = list(d for d in key_diffs if (d[0] == 'add' or d[0] == 'remove'))
            value_diffs = list(diff(expect, actual, ignore=set(ignores)))
            value_diffs = list(d for d in value_diffs if d[0] == 'change')
            diffs = key_diffs + value_diffs
        elif ignores and isinstance(ignores, dict):
            raise AssertionError("Currently inputting ignores as dict is not supported")
        elif nonignores:
            logger.debug("This is the nonignore list:\n")
            logger.debug(nonignores)
            key_diffs = []
            del_expected = update_value_from_original_dictionary(expect, nonignores)
            del_actual = update_value_from_original_dictionary(actual, nonignores)
            if check_key:
                key_diffs = list(diff(del_expected, del_actual))
                key_diffs = list(d for d in key_diffs if (d[0] == 'add' or d[0] == 'remove'))
            value_diffs = list(diff(del_expected, del_actual))
            value_diffs = list(d for d in value_diffs if d[0] == 'change')
            diffs = key_diffs + value_diffs
        else:
            diffs = list(diff(expect, actual))
    logger.debug("This is the diff list:\n")
    logger.debug(diffs)
    return diffs
