import unittest
from Utilities import generate_request_uid
from tag_generator import is_request_uid

class Generate(unittest.TestCase):
    def test1(self):
        '''
        This function verifies generate_request_uid creates a valid request unique id with the correct format.

        *Example*
        | App_id has 3 characters
        '''
        result = generate_request_uid(772)
        regex = r'^772_\d{8}_\d{15}$'
        self.assertRegex(result, regex)

    def test2(self):
        '''
        This function verifies generate_request_uid creates a valid request unique id with the correct format.

        *Example*
        | App_id has 1 character
        '''
        result = generate_request_uid(1)
        regex = r'^1_\d{8}_\d{15}$'
        self.assertRegex(result, regex)

    def test3(self):
        '''
        This function verifies generate_request_uid creates a valid request unique id with the correct format.

        *Example*
        | App_id has a float number format
        '''
        result = generate_request_uid(68.01)
        regex = r'^68.01_\d{8}_\d{15}$'
        self.assertRegex(result, regex)

    def test4(self):
        '''
        The input of the is_request_uid function is the request_uid tag.
        '''
        result = is_request_uid('[772_DATE_UID]')
        assert result == True

    def test5(self):
        '''
        The input of the is_request_uid function is not the request_uid tag.
        '''
        result = is_request_uid('77_[DATE_UID]')
        assert result == None

    def test6(self):
        '''
        The input of the is_request_uid function is not the request_uid tag.
        '''
        result = is_request_uid('68.01_DATE_UID')
        assert result == None
