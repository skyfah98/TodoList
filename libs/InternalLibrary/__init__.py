from .DataSolution import DataSolution


__version__ = '2.0.0'


class InternalLibrary(DataSolution):

    """
        InternalLibrary for create custom function or some solution to help automate
        FCISDebitBankAcc project. Used in separated project

        Required Library:
            ExcelImportLibrary
            ExtendedDatabaseLibrary

        Last update: 22-Sep-2020

        == Supported Tag ==
        | *Tag*                     | *Generated Value*                                                                     |
        | [AUTO_GEN_ID]             | ROBOT202001290123456789                                                               |
        | [AUTO_GEN_DOC_ID]         | DOC2020012                                                                            |
        | [AUTO_GEN_{CUSTOM_ID}_ID  | {CUSTOM_ID}202001290123456789                                                         |
        | [EXIST_{CUSTOM_ID}_ID]    | << Last value from [AUTO_GEN_{CUSTOM_NAME}_ID] >>                                     |
        | [AUTO_GEN_PHONE]          | 099999????                                                                            |
        | [EXIST_PHONE]             | << Last value from [AUTO_GEN_PHONE] >>                                                |
        | [AUTO_GEN_{BOOK_TYPE}]    | IOS-93316074-4-055, ADR-93316074-4-055                                                |
        | [EXIST_{BOOK_TYPE}]       | << Last value from [AUTO_GEN_{BOOK_TYPE}] >>                                          |
        | [NOW_ISO_DT]              | 2020-01-07T14:29:02.567Z                                                              |
        | [NOW_UTC_DT]              | 2020-01-07T14:29:02.567+07:00                                                         |
        | [NOW_UTC_DATE]            | 2020-01-17                                                                            |
        | [NOW_DATE_NO_SYMBOL]      |                                                                               |
        | [NOW_TIME_NO_SYMBOL]      |
        | [AUTO_GET_INVOICE_NO]     | 202001071429  |
        | [EXIST_ISO_DT]            | << Last value from [NOW_ISO_DT] >>                                                    |
        | [EXIST_UTC_DT]            | << Last generated value from [NOW_UTC_DT] >>                                          |
        | [EXIST_UTC_DATE]          | << Last value from [NOW_UTC_DATE] >>                                                  |
        | [SAVE]                    | << Save actual value >>                                                               |
        | [LOAD]                    | << Load saved actual value >>                                                         |
        | [SAVE_COOKIE]             | convert to valid cooke then save                                                      |
        | [LOAD_COOKIE]             | load lasted valid form last saved cookie                                              |
        | [QUERY:??????]            | query sql database with sql statement on tag rear (statement support *Tag* inside)    |
        | [NOW_ISO8601_DT]          | 2020-01-02 14:29:02                                                                   |
        | [EXIST_ISO8601_DT]        | load existed datetime in format ISO8601 (now it come from [NOW_ISO8602_DT] tag        |
    """

    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self):
        super(InternalLibrary, self).__init__()
