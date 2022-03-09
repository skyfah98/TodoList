***Keywords***
To Do List: Open Browser
    Create Chrome Webdriver          https://abhigyank.github.io/To-Do-List/

To Do List: Add Item
    [Arguments]     ${task}
    Click Element   ${ADD_ITEM.MENU}
    Input Text      ${ADD_ITEM.TEXTBOX}    ${task}
    Click Element   ${ADD_ITEM.BUTTON}

To Do List: Completed Task
    Click Element   ${TO_DO_TASKS.MENU}
    sleep   2s
    Click Element   ${TO_DO_TASKS.BUTTON}

To Do List: Delete Uncompleted Task
    Click Element   ${TO_DO_TASKS.MENU}
    Click Element   ${TO_DO_TASKS.DELETE.BUTTON}

To Do List: Delete Completed Task
    Click Element   ${COMPLETED.MENU} 
    sleep   2s
    Click Element   ${COMPLETED.DELETE.BUTTON}

To Do List: Close Browser