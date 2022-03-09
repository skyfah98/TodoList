# encoding=utf8
from robot.api import logger
from robot.api.deco import keyword


class TCReloader:
    """
    This test library provides keywords to read, write robot file for dynamic automation test follow by test-data

    * Before running tests in Robot Framework *
    Prior to running tests,
    TCRLoadLibrary must first be imported into your Robot test suite.
    and use 'robot -P {library_path}' before run robot file

    Example:
    |  Library  |  TCReloadLibrary  |
    """

    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'

    def __init__(self):
        self.status = None

    @staticmethod
    def __log_error(message: str):
        logger.error(
            f"[TCReloadLibrary] {message}",
            True
        )

    @staticmethod
    def __log_info(message: str):
        logger.info(
            f"[TCReloadLibrary] {message}",
            True
        )

    @keyword("Create Robot File")
    def create_robot_file(self, robot_filepath: str):
        """
        Create blank robot file (*.robot)
        """

        try:
            newRobotFile = open(robot_filepath, "w+")
            newRobotFile.close()
            self.__log_info(
                f"Created file '{robot_filepath}'"
            )
        except Exception as exception:
            self.__log_info(
                f"Can not create robot file at '{robot_filepath}' : {exception}"
            )

    @keyword("Add Test Case Header")
    def add_header(self, robot_filepath: str, header_filepath: str) -> bool:
        """
        Used for add test case header about Settings, Variables or Keywords
        Above Test Cases section

        TCReloader.add_header(
            "~/project/template_testcases.robot",
            "~/project/_generate_parts/header.txt"
        )
        """

        try:
            with open(str(robot_filepath), "a") as script:
                with open(str(header_filepath), "r") as headers:
                    header_lines = headers.readlines()
                    for line in header_lines:
                        script.write(line)
                    script.write('\n')
                    self.status = True
            self.__log_info(
                f"Added test suite header '{robot_filepath}'"
            )
            return self.status
        except Exception as exception:
            self.__log_info(
                f"There are error occur while write test case header on file '{robot_filepath}' with '{header_filepath}' : {exception}"
            )
            return False

    @keyword("Clear All Test Case")
    def clear_testcases(self, robot_filepath: str) -> bool:
        """
        Used for clear all test case from robot file but still keep Settings,
        Variables and Keywords.
        """

        try:
            with open(str(robot_filepath), "r+") as script:
                script_lines = script.readlines()
                script.truncate(0)
                found = False
                script.seek(0)
                for line in script_lines:
                    if not found:
                        script.write(line)
                    line = str(line).lower()
                    if "*** test cases ***" in line:
                        found = True
                        script.write("")
                        break
                if not found:
                    self.status = False
                script.close()
                self.__log_info(
                    f"Clear test cases from file '{robot_filepath}'"
                )
                return self.status
        except Exception as exception:
            self.__log_error(
                f"There are error occur while clear testcases on file '{robot_filepath}' : {exception}"
            )
            raise

    @keyword("Write Test Case")
    def add_testcase(self, robot_filepath: str, test_name: str, documentation: str, tags: list, step_filepath: str) -> bool:
        """
        Used for add test case under *** Test Cases *** tags
        and can add documentation and tag under test case's name

        TCReloader.add_testcase(
            "~/project/template_testcases.robot",
            "Example Test Case #001",
            "This is example test case for check add",
            ["tag#1", "tag#2"],
            "~/project/_generate_parts/teststeps.txt"
        )
        """

        try:
            with open(str(robot_filepath), "a") as script:
                script.write(f'{test_name}\n')
                if documentation != '':
                    documentation = str(documentation).replace('\n', '\n  ...  \\n')
                    script.write(f"  [Documentation]  {documentation}\n")
                script.write(f"  [Tags]  ")
                if len(tags) > 0:
                    for tag in tags:
                        script.write(f"{tag}  ")
                script.write("\n")
                with open(str(step_filepath), "r") as steps:
                    step_lines = steps.readlines()
                    for line in step_lines:
                        script.write(line)
                    script.write('\n')
                    self.status = True
                script.write("\n")
                script.close()
                self.status = True
            self.__log_info(
                f"[{test_name}] has been created"
            )
            return self.status
        except Exception as exception:
            self.__log_info(
                f"There are error occur while add test case '{test_name}' on file '{robot_filepath}' : {exception}"
            )
            raise
