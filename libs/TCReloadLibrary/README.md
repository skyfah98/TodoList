# TCReloadLibrary

Python library for support create `*.robot` file with step on `*.txt` file

## Requirements

- [python](https://www.python.org/downloads/)       version 3.8
- [pip](https://pip.pypa.io/en/stable/installing/)  version 19.3.1

## Installation

```shell
$ pip install -m requirement.txt
```

## Usage
   
#### Create Robot File

```python
    @keyword("Create Robot File")
    def create_robot_file(self, robot_filepath: str):
        """
        Create blank robot file (*.robot)
        
        EX:
        PYTHON ->   TCReloader.create_robot_file("Demo/demo.robot")
        ROBOT ->    Create Robot File  robot_filepath=Demo/demo.robot
        """
```
        
#### Add Test Case Header

```python
    @keyword("Add Test Case Header")
    def add_header(self, robot_filepath: str, header_filepath: str) -> bool:
        """
        Used for add test case header about Settings, Variables or Keywords
        Above Test Cases section

        EX:
        PYTHON -->  TCReloader.add_header("~/project/template_testcases.robot", "~/project/_generate_parts/header.txt")
        ROBOT -->   Add Test Case  robot_filepath=~/project/template_testcases.robot  header_filepath=/project/_generate_parts/header.txt
        
        """
```
             
#### Clear All Test Case

```python
    @keyword("Clear All Test Case")
    def clear_testcases(self, robot_filepath: str) -> bool:
        """
        Used for clear all test case from robot file but still keep Settings,
        Variables and Keywords.
        
        EX:
        PYTHON -->  TCReloader.clear_testcases("Demo/robot.robot")
        ROBOT -->   Clear All Test Case  robot_filepath=Demo/robot.robot
        """
```

#### Write Test Case

```python
    @keyword("Write Test Case")
    def add_testcase(self, robot_filepath: str, test_name: str, documentation: str, tags: list, step_filepath: str) -> bool:
        
        """
        Used for add test case under *** Test Cases *** tags
        and can add documentation and tag under test case's name
        * this test case will use default 4 space

        EX:
        PYTHON -->  TCReloader.add_testcase(
                        "~/project/template_testcases.robot",
                        "Example Test Case #001",
                        "This is example test case for check add",
                        ["tag#1", "tag#2"],
                        "~/project/_generate_parts/teststeps.txt"
                    )
                    
        ROBOT -->   Write Test Case  
                    ...  robot_filepath=~/project/template_testcases.robot  
                    ...  test_name=Example Test Case #001  
                    ...  documentation=This is example test case for check add  
                    ...  tags=["tag#1", "tag#2"]  
                    ...  step_filepath=~/project/_generate_parts/teststeps.txt
        """
```

##### Last Updated: 27 Dec 2019
