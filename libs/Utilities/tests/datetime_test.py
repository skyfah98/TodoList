import unittest
from Utilities import get_iso_datetime_tzcus
from Utilities import get_current_date_with_local_timezone
from Utilities import get_utc_datetime
from Utilities import get_iso_datetime_ml


class DateTimeTest(unittest.TestCase):
    def test1(self):
        result = get_iso_datetime_tzcus()
        regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}$'
        self.assertRegex(result, regex)

    def test2(self):
        actual = get_current_date_with_local_timezone()
        regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}$'
        self.assertRegex(actual, regex)

    def test3(self):
        actual = get_utc_datetime()
        regex = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{6}\+\d{2}:\d{2}$'
        self.assertRegex(actual, regex)

    def test4(self):
        actual = get_iso_datetime_ml()
        regex = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}\+\d{2}:\d{2}$'
        self.assertRegex(actual, regex)
