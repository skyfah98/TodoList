import unittest
from Utilities.tag_generator import update_dictionary_by_tags


class Tag_Generator_Test(unittest.TestCase):

    def test1(self):
        source = {'args': 'insert', 'dynamicAgentSession': 'true', 'param': {'channel': 'IB', 'custId': '[NULL]', 'ipAddress': '127.0.0.1', 'loginId': 'ibuser200', 'ssoSessionId': 'ssoSessionId'}, 'params': {'segmentId': 'IBUser'}, 'password': 'password1', 'realmId': '40151', 'userId': 'ibuser200'}
        actual = update_dictionary_by_tags(source)
        assert source['param']['custId'] == '[NULL]'
        assert actual['param']['custId'] == None

    def test2(self):
        source = {'args': 'insert', 'dynamicAgentSession': 'true', 'param': {'channel': 'IB', 'custId': '[NULL]', 'ipAddress': '127.0.0.1', 'loginId': 'ibuser200', 'ssoSessionId': 'ssoSessionId'}, 'params': {'segmentId': '[REMOVE]'}, 'password': '[REMOVE]', 'realmId': '[REMOVE]', 'userId': '[REMOVE]'}
        actual = update_dictionary_by_tags(source)
        assert actual == {'args': 'insert', 'dynamicAgentSession': 'true', 'param': {'channel': 'IB', 'custId': None, 'ipAddress': '127.0.0.1', 'loginId': 'ibuser200', 'ssoSessionId': 'ssoSessionId'}, 'params': {}}

    def test3(self):
        source = {'rqUID': '[756_DATE_UID]'}
        result = update_dictionary_by_tags(source)
        regex = r'^756_\d{8}_\d{15}$'
        self.assertRegex(result['rqUID'], regex)
