"""
This module provides keywords to support xml processing.
"""


from xml.etree import ElementTree as et
from robot.api import logger
from robot.api.deco import keyword


TAG = 'xml'
__all__ = [
    'update_value_to_xml',
    'adjust_xml_to_zeep_format']


@keyword(name="Update Value To XML File", tags=(TAG,))
def update_value_to_xml(data_file, path, value, encode="UTF-8"):
    """
    Update value in xml file follow by path (json path).

    Example:
    | Update Value To XML | request.xml | header.appId | 681 | UTF-8 |

    Return type: bool
    """
    tree = et.parse(data_file)
    path = str(path).replace('.', '/')
    logger.info(f"{path}")
    try:
        tree.find(f'.//{path}').text = value
    except Exception as info:
        logger.info(f"update_value_to_xml {info}")
        pass
    tree.write(data_file, encoding=encode)

@keyword(name="Convert XML File To Zeep XML File", tags=(TAG,))
def adjust_xml_to_zeep_format(data_file, encode="UTF-8"):
    """
    Adjust xml to zeep format.
    """
    tree = et.parse(data_file)
    tree.write(data_file, encoding=encode)
