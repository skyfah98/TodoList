*** Settings ***
Library  SeleniumLibrary  run_on_failure=Capture Page Screenshot

*** Variables ***
${CHROME_DRIVER_PATH}    ${EXECDIR}${/}drivers${/}win32${/}chromedriver_98
#${CHROME_DRIVER_PATH}    ${EXECDIR}${/}drivers${/}mac64${/}chromedriver_89

*** Keywords ***
Create Chrome Webdriver
    [Documentation]  create new chrome driver with options
    [Arguments]  ${url}  ${driver_path}=${CHROME_DRIVER_PATH}  ${speed}=0.1
    log to console  ------
    ${chrome_options} =  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method  ${chrome_options}  add_experimental_option    useAutomationExtension    ${False}
    # Call Method  ${chrome_options}  add_argument  --headless
    Call Method  ${chrome_options}  add_argument  --test-type
    Call Method  ${chrome_options}  add_argument  --ignore-certificate-errors
    Call Method  ${chrome_options}  add_argument  --disable-gpu
    Call Method  ${chrome_options}  add_argument  --no-sandbox
    ${kwargs} =  BuiltIn.Create Dictionary  executable_path=${driver_path}
    Create Webdriver  Chrome  chrome_options=${chrome_options}  kwargs=${kwargs}
    Go To  ${url}
    log to console  url: ${url}
    Set Selenium Speed  ${speed}
    log to console  speed: ${speed}s
    log to console  ------
    Maximize Browser Window

