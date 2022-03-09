import unittest
from Utilities.utilities import print_friendly_message


class TestPrintMessage(unittest.TestCase):
    
    def test1(self):
        input_data = [('change', ['kbankHeader', 'errors', 0, 'errorDesc'], ('funcNm [VS3D2077O02_@] does not match service implementation', 'funcNm [VS3D2077O02_@] does not match service implementatio'))]
        actual = print_friendly_message(input_data)
        expect = 'The value of "errorDesc" at index "0" of "kbankHeader.errors" is changed from "funcNm [VS3D2077O02_@] does not match service implementation" to "funcNm [VS3D2077O02_@] does not match service implementatio"'
        assert actual == expect
    
    def test2(self):
        input_data = [('change', ['kbankHeader', 'errors', 0, 'errorAppAbbrv'], ('EAI', 'EAIaa')), ('change', ['kbankHeader', 'errors', 0, 'errorDesc'], ('funcNm [VS3D2077O02_@] does not match service implementation', 'funcNm [VS3D2077O02_@] does not match service implementatio'))]
        actual = print_friendly_message(input_data)
        expect = '''The value of "errorAppAbbrv" at index "0" of "kbankHeader.errors" is changed from "EAI" to "EAIaa"
The value of "errorDesc" at index "0" of "kbankHeader.errors" is changed from "funcNm [VS3D2077O02_@] does not match service implementation" to "funcNm [VS3D2077O02_@] does not match service implementatio"'''
        assert actual == expect
        
    def test3(self):
        input_data = [('change', 'kbankHeader.funcNm', ('VS3D2077O01', 'VS3D2077O02')), ('change', ['kbankHeader', 'errors', 0, 'errorAppAbbrv'], ('EAI', 'EAIaa')), ('change', ['kbankHeader', 'errors', 0, 'errorDesc'], ('funcNm [VS3D2077O02_@] does not match service implementation', 'funcNm [VS3D2077O02_@] does not match service implementatio'))]
        actual = print_friendly_message(input_data)
        expect = '''The value of "kbankHeader.funcNm" is changed from "VS3D2077O01" to "VS3D2077O02"
The value of "errorAppAbbrv" at index "0" of "kbankHeader.errors" is changed from "EAI" to "EAIaa"
The value of "errorDesc" at index "0" of "kbankHeader.errors" is changed from "funcNm [VS3D2077O02_@] does not match service implementation" to "funcNm [VS3D2077O02_@] does not match service implementatio"'''
        assert actual == expect

    def test4(self):
        input_data = [('change', 'kbankHeader.funcNm', ('VS3D2077O01', 'VS3D2077O02'))]
        actual = print_friendly_message(input_data)
        expect = 'The value of "kbankHeader.funcNm" is changed from "VS3D2077O01" to "VS3D2077O02"'
        assert actual == expect
        
    def test5(self):
        input_data = [('change', 'MDWCommonTransferK2K.fromOutStandBal', (300509591.81, 300532295.81)), ('change', 'MDWCommonTransferK2K.fromAvailBal', (300509591.81, 300532295.81)), ('change', 'MDWCommonTransferK2K.toAcctOutStandBal', (90111171015.69, 90111148344.69)), ('change', 'MDWCommonTransferK2K.toAvailBal', (90111171015.69, 90111148344.69))]
        actual = print_friendly_message(input_data)
        expect = '''The value of "MDWCommonTransferK2K.fromOutStandBal" is changed from "300509591.81" to "300532295.81"
The value of "MDWCommonTransferK2K.fromAvailBal" is changed from "300509591.81" to "300532295.81"
The value of "MDWCommonTransferK2K.toAcctOutStandBal" is changed from "90111171015.69" to "90111148344.69"
The value of "MDWCommonTransferK2K.toAvailBal" is changed from "90111171015.69" to "90111148344.69"'''
        assert actual == expect
    
    def test6(self):
        input_data = [('remove', 'KBankHeader', [('rqUID', '50920191113_sfbrl9pp1lrzp7nukerf3ki645809213')])]
        actual = print_friendly_message(input_data)
        expect = 'The attribute "KBankHeader.rqUID" is removed from actual result'
        assert actual == expect
        
    def test7(self):
        input_data = [('add', 'KBankHeader', [('rqUID', '50920191113_sfbrl9pp1lrzp7nukerf3ki645809213')])]
        actual = print_friendly_message(input_data)
        expect = 'The attribute "KBankHeader.rqUID" is added into actual result'
        assert actual == expect      
        
    def test8(self):
        input_data = [('add', ['kbankHeader', 'errors', 0], [('errorAppId', '681'), ('errorAppAbbrv', 'CVRS'), ('errorCode', '2001'), ('errorSeverity', '00')])]
        actual = print_friendly_message(input_data)
        expect = 'The attribute "errorAppId" at index "0" of "kbankHeader.errors" is added into actual result'
        assert actual == expect
    
    def test9(self):
        input_data = [('add', '', [('cvrsInfo', "aaaa")])]
        actual = print_friendly_message(input_data)
        expect = 'The attribute "cvrsInfo" is added into actual result'
        assert actual == expect 

    def test10(self):
        input_data = [('change', 'kbankHeader.funcNm', ('VS3D2077O01', 'VS3D2077O02')),('change', ['kbankHeader', 'errors', 0, 'errorAppAbbrv', 'abc'], ('EAI', 'EAIaa')),('change', ['result', 'authzResponses', 'wsa.sessionIID'], ('QE1wPkZGDfltG8nn3pDClg', 'v0M0lsmwSdorvs78mGMPpA'))]
        actual = print_friendly_message(input_data)
        expect = '''The value of "kbankHeader.funcNm" is changed from "VS3D2077O01" to "VS3D2077O02"
The value of "errorAppAbbrv.abc" at index "0" of "kbankHeader.errors" is changed from "EAI" to "EAIaa"
The value of "result.authzResponses.wsa.sessionIID" is changed from "QE1wPkZGDfltG8nn3pDClg" to "v0M0lsmwSdorvs78mGMPpA"'''
        assert actual == expect
