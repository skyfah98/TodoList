import unittest
from Utilities.dict_management import update_data_into_original_dictionary


class Test(unittest.TestCase):
    def test_update_dict1(self):
        source = {'hello': 'to_override'}
        overrides = {'hello': 'over'}
        result = update_data_into_original_dictionary(source, overrides)
        assert result == {'hello': 'over'}
    
    def test_update_dict2(self):
        source = {'hello': {'value': 'to_override', 'no_change': 1}}
        overrides = {'hello': {'value': 'over'}}
        result = update_data_into_original_dictionary(source, overrides)
        assert result == {'hello': {'value': 'over', 'no_change': 1}}
        
    def test_update_dict3(self):
        source = {'hello': {'value': 'to_override', 'no_change': 1}}
        overrides = {'hello': {'value': ''}}
        result = update_data_into_original_dictionary(source, overrides)
        assert result == {'hello': {'value': '', 'no_change': 1}}
        
    def test_update_dict4(self):
        source = {'hello': {'value': {}, 'no_change': 1}}
        overrides = {'hello': {'value': 2}}
        result = update_data_into_original_dictionary(source, overrides)
        assert result == {'hello': {'value': 2, 'no_change': 1}}
        
    def test_update_dict5(self):
        source = {'Person': {'Name': 'Testing', 'Age': 25, 'Car':{'Name' :'Mercedes', 'Color': 'Red'}}}
        overrides = {'Person': {'Name': 'Edit_Testing'}}
        result = update_data_into_original_dictionary(source, overrides)
        assert result == {'Person': {'Name': 'Edit_Testing', 'Age': 25, 'Car':{'Name' :'Mercedes', 'Color': 'Red'}}}
        
    def test_update_dict6(self):
        source = {'Person': {'Name': 'Testing', 'Age': 25, 'Car':{'Name' :'Mercedes', 'Color': 'Red'}}, 'Others': {'Table': '1', 'Mouse': 3}}
        overrides = {'Person': {'Car':{'Name' :'Toyota', 'Color': 'Yellow'}}, 'Others': {'Mouse': 5}}
        result = update_data_into_original_dictionary(source, overrides)
        assert result == {'Person': {'Name': 'Testing', 'Age': 25, 'Car':{'Name' :'Toyota', 'Color': 'Yellow'}}, 'Others': {'Table': '1', 'Mouse': 5}}
        
    def test_update_dict7(self):
        source = {'kbankHeader': {'funcNm': 'VS3D2077O01', 'rqUID': '766_20191022_AUTOMATIONTESTING', 'rsAppId': '257', 'rsUID': '3a6e2f637f000001518fe3b59a0dfbd7', 'rsDt': '2019-11-05T14:18:49.958+07:00', 'statusCode': '10', 'errors': [{'errorAppId': '257', 'errorAppAbbrv': 'EAI', 'errorCode': '30195', 'errorDesc': 'TO ACCOUNT INACTIVE', 'errorSeverity': '00'}], 'corrID': None, 'reqAuthUserId': None, 'reqAuthLevel': None}}
        overrides = {'kbankHeader': {'errors': [{'errorDesc': 'funcNm [VS3D2077O02_@] does not match service implementation'}]}}
        actual = update_data_into_original_dictionary(source, overrides)
        expect = {'kbankHeader': {'funcNm': 'VS3D2077O01', 'rqUID': '766_20191022_AUTOMATIONTESTING', 'rsAppId': '257', 'rsUID': '3a6e2f637f000001518fe3b59a0dfbd7', 'rsDt': '2019-11-05T14:18:49.958+07:00', 'statusCode': '10', 'errors': [{'errorAppId': '257', 'errorAppAbbrv': 'EAI', 'errorCode': '30195', 'errorDesc': 'funcNm [VS3D2077O02_@] does not match service implementation', 'errorSeverity': '00'}], 'corrID': None, 'reqAuthUserId': None, 'reqAuthLevel': None}}
        assert actual == expect

    def test_update_dict8(self):
        '''Verify source is not changed'''
        source = {'kbankHeader': {'funcNm': 'VS3D2077O01', 'rqUID': '766_20191022_AUTOMATIONTESTING', 'rsAppId': '257', 'rsUID': '3a6e2f637f000001518fe3b59a0dfbd7', 'rsDt': '2019-11-05T14:18:49.958+07:00', 'statusCode': '10', 'errors': [{'errorAppId': '257', 'errorAppAbbrv': 'EAI', 'errorCode': '30195', 'errorDesc': 'TO ACCOUNT INACTIVE', 'errorSeverity': '00'}], 'corrID': None, 'reqAuthUserId': None, 'reqAuthLevel': None}}
        overrides = {'kbankHeader': {'errors': [{'errorDesc': 'funcNm [VS3D2077O02_@] does not match service implementation'}]}}
        update_data_into_original_dictionary(source, overrides)
        assert source == {'kbankHeader': {'funcNm': 'VS3D2077O01', 'rqUID': '766_20191022_AUTOMATIONTESTING', 'rsAppId': '257', 'rsUID': '3a6e2f637f000001518fe3b59a0dfbd7', 'rsDt': '2019-11-05T14:18:49.958+07:00', 'statusCode': '10', 'errors': [{'errorAppId': '257', 'errorAppAbbrv': 'EAI', 'errorCode': '30195', 'errorDesc': 'TO ACCOUNT INACTIVE', 'errorSeverity': '00'}], 'corrID': None, 'reqAuthUserId': None, 'reqAuthLevel': None}}

    def test_update_dict9(self):
        source = {'kbankHeader': {'funcNm': 'VS3D2077O01', 'rqUID': '766_20191022_AUTOMATIONTESTING', 'rqDt': '2019-10-31T10:23:13.877+07:00', 'rqAppId': '766', 'userId': 'K0173005', 'terminalId': None, 'userLangPref': 'EN', 'corrID': None, 'authUserId': 'K0173005', 'authLevel': 1}, 'cardInfo': {'ticketId': 'f859f32ad7f447b1bf79639b4733590a', 'consent': 'Y', 'otp': '123'}}
        overrides = {'kbankHeader': {'funcNm': ''}}
        result = update_data_into_original_dictionary(source, overrides)
        assert source == {'kbankHeader': {'funcNm': 'VS3D2077O01', 'rqUID': '766_20191022_AUTOMATIONTESTING', 'rqDt': '2019-10-31T10:23:13.877+07:00', 'rqAppId': '766', 'userId': 'K0173005', 'terminalId': None, 'userLangPref': 'EN', 'corrID': None, 'authUserId': 'K0173005', 'authLevel': 1}, 'cardInfo': {'ticketId': 'f859f32ad7f447b1bf79639b4733590a', 'consent': 'Y', 'otp': '123'}}
        assert result == {'kbankHeader': {'funcNm': '', 'rqUID': '766_20191022_AUTOMATIONTESTING', 'rqDt': '2019-10-31T10:23:13.877+07:00', 'rqAppId': '766', 'userId': 'K0173005', 'terminalId': None, 'userLangPref': 'EN', 'corrID': None, 'authUserId': 'K0173005', 'authLevel': 1}, 'cardInfo': {'ticketId': 'f859f32ad7f447b1bf79639b4733590a', 'consent': 'Y', 'otp': '123'}}
