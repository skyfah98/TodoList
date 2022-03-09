*** Variables ***
# Add Item
${ADD_ITEM.MENU}                xpath=/html/body/div/div/div[1]/a[1]/span
${ADD_ITEM.TEXTBOX}             xpath=//*[@class="mdl-textfield__input"]
${ADD_ITEM.BUTTON}              xpath=//*[@class="mdl-button mdl-js-button mdl-button--fab mdl-button--mini-fab mdl-button--colored"]

# To do Tasks
${TO_DO_TASKS.MENU}             xpath=/html/body/div/div/div[1]/a[2]/span
${TO_DO_TASKS.BUTTON}           xpath=//*[@class="mdl-checkbox mdl-js-checkbox mdl-js-ripple-effect mdl-js-ripple-effect--ignore-events is-upgraded"]
${TO_DO_TASKS.DELETE.BUTTON}    xpath=/html/body/div/div/div[3]/ul/li/button/span

# Completed
${COMPLETED.MENU}               xpath=/html/body/div/div/div[1]/a[3]/span
${COMPLETED.DELETE.BUTTON}      xpath=/html/body/div/div/div[4]/ul/li/button/span