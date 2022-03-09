"""
This module provide keywords to support about socket.
"""

import socket
import base64
import hashlib
from robot.api.deco import keyword


UTF_8 = 'UTF-8'
TIS_620 = 'TIS-620'
SPACE = ' '
ZERO = '0'
TAG = 'socket'

__all__ = [
    'encrypt_sha256',
    'send_message_socket',
    'update_message_socket',
    'encode_base64',
    'decode_base64']


@keyword(name="Encrypt Sha256", tags=(TAG,))
def encrypt_sha256(text: str, salt: str = "", encode: str = UTF_8) -> str:
    """
    Encrypt text string by using sha256.

    Arguments:

    - ``text``: an input string.

    - ``salt``: an additional text to a one-way function that hashes data.

    - ``encode``: a cryptographic hash functions.

    Return: Text has been encoded by base64.

    Examples:

    |   Encrypt Sha256  |   hello there |        |           |
    |   Encrypt Sha256  |   hello there | " "    |           |
    |   Encrypt Sha256  |   hello there | " "    |   UTF-8   |

    It will return 'Gi/v5Wa3Y5JTJhh0DM2YOID9ExRkGDpJRTvWz3YPkzU='.
    """
    text = text.strip() + salt
    text = hashlib.sha256(text.encode(encode)).digest()
    return encode_base64(bytes(text))


@keyword(name="Send Message Socket", tags=(TAG,))
def send_message_socket(host: str, port: int, message: bytes) -> bytes:
    """
    First, This method connects to host. Next, It will be sent a message as a byte text.
    And then it will return data encoding by base64.

    Arguments:

    - ``host``: an address of website.

    - ``port``: an port.

    - ``message``: an text encoding by base64.

    Return: Text has been encoded by base64.

    Example:

    | Send Message Socket | 192.168.1.1 | 80 | AvKFM4YK02YwMUsxRTlL |

    It will return 'OSzQyODM4MDAwNzg2ODAyMzEg'.
    """
    text_byte = decode_base64(message)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
        soc.settimeout(30)
        soc.connect((host, port))
        soc.sendall(text_byte)
        data = soc.recv(1024)
    return encode_base64(data)


@keyword(name="Update Message Socket", tags=(TAG,))
def update_message_socket(text_base64: bytes, message: str, offset: int, length: int,
                          encode: str = TIS_620) -> bytes:
    """
    Update text in the text_base64 by substring byte text and replace message
    ... which is byte text in that place.

    Arguments:

    - ``text_base64``: the original text to update.

    - ``message``: a text to update.

    - ``offset``: an address index to update.

    - ``length``: a maximum size of an address to update.

    - ``encode``: encode message before updating.

    Return: Text has been encoded by base64.

    Examples:

    | Update Message Socket | AvKFM4YK02YwMUsxR | Hello | 2 | 10 |         |
    | Update Message Socket | AvKFM4YK02YwMUsxR | Hello | 2 | 10 | TIS-620 |

    It will return 'OSzQyODM4MDAwNzg2ODAyMzEg'.
    """
    if message is None:
        message = ''
    if encode == TIS_620:
        text_byte = convert_str_to_bytes(message, length, encode)
    else:
        text_byte = convert_int_to_hex(message, length)
    text_decode = decode_base64(text_base64)
    new_message = text_decode[:offset] + text_byte + text_decode[offset + length:]
    return encode_base64(new_message)


def convert_str_to_bytes(text: str, length: int, encode: str) -> bytes:
    """
    Convert string to Bytes.
    """
    space = make_pattern(text, length, SPACE)
    return bytes(text + space, encode)


def convert_int_to_hex(text: str, length: int) -> bytes:
    """
    Convert Integer to Hex.
    """
    number = hex(int(text))[2:]
    zero = make_pattern(number, 2 * length, ZERO)
    array = bytearray.fromhex(zero + number)
    return bytes(array)


def make_pattern(text: str, length: int, pattern: str):
    """
    Make pattern.
    """
    size = length - len(text)
    if size < 0:
        raise ValueError(f'Length of {text} should not greater than {length}')
    return pattern * size


def convert_hex_to_int(number: bytes) -> int:
    """
    Convert Hex to Integer.
    """
    return int(number.hex(), 16)


@keyword(name="Encode Base64", tags=(TAG,))
def encode_base64(text: bytes) -> bytes:
    """
    Encode text to base64.

    Argument:

    ``text``: message to encode.

    Return: Text has been encoded by base64.

    Example:

    | Update Message Socket | Hello world |

    It will return 'SGVsbG8gd29ybGQ='
    """
    return base64.b64encode(bytes(text))


@keyword(name="Decode Base64", tags=(TAG,))
def decode_base64(text: bytes) -> bytes:
    """
    Decode text base on base64.

    Argument:

    ``text``: text which is a base64.

    Return: Text message.

    Example:

    | Update Message Socket | SGVsbG8gd29ybGQ= |

    It will return 'Hello world'.
    """
    return base64.b64decode(text)
