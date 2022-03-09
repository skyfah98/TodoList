*** Settings ***
Library     SeleniumLibrary     # https://robotframework.org/SeleniumLibrary/SeleniumLibrary.html
Resource    ${EXECDIR}/common/selenium_keywords.resource
Resource    ${EXECDIR}/keywords/todo_list_keywords.resource
Resource    ${EXECDIR}/locators/todo_list_locators.resource

*** Test Cases ***
TO DO LIST
    [Tags]           todo_list     POSITIVE     UI     CHROME
    To Do List: Open Browser
    To Do List: Add Item    Test
    # To Do List: Delete Uncompleted Task
    To Do List: Completed Task
    To Do List: Delete Completed Task
    

### command run robot ###
# robot -P libs -d results -i todo_list workspace


