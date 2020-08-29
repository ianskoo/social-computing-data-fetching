from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

'''
Vorlesungsverzeichnis bot
-------------------------
Finds the IDs of all the modules of the economics faculty
for the current semester and saves them to 'id_list.txt'.
Modify the following parameter for slower internet connections 
(or possibly CPUs)
'''
# Speed limiter factor:
# 1: normal speed; higher factor = slower bot; 0.1 increase steps suggested
lim = 1

# Chromedriver path
driver = webdriver.Chrome('/usr/bin/chromedriver')

# Go to VVZ
driver.get('https://studentservices.uzh.ch/uzh/anonym/vvz/index.html#/search')

# Sleep to let the page load
time.sleep(4 * lim)

# Find dropdown menu for the faculty and choose WWF
driver.find_element_by_id('__box10-__clone91-arrow').click()
driver.find_element_by_id('__item10').click()
time.sleep(0.5 * lim)

# Save elements needed for the action chains
topbar = driver.find_element_by_id('__toolbar0')
actions = ActionChains(driver)

# Get total number of modules from the list's title
numAttr = driver.find_element_by_id('__xmlview1--smSearchResultTitle').get_attribute('aria-label')
totMods = int(numAttr.split(' ')[0])
print('Total number of modules found: ' + str(totMods))

moduleClass = "sapMLIB sapMLIB-CTX sapMLIBShowSeparator sapMLIBTypeNavigation sapMLIBActionable sapMLIBHoverable" \
                  " sapMLIBFocusable sapMListTblRow sapMListTblRowMiddle navTableItemLayout"

# Loop through the list of modules and get their ID
idList = []
for i in range(totMods):
    # If the range of visible modules is reached, scroll down the list
    topbar.click()
    num = (i + 1) // 20 + 1  # Add one scroll to avoid index errors when not starting from the beginning of the list
    for r in range(num):
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(0.3 * lim)  # Increase this time for slower internet connections
    time.sleep(0.5 * lim)

    modules = driver.find_elements_by_xpath(
        '//tbody[@class="sapMListItems sapMTableTBody"]/tr[@class="%s"]' % moduleClass)

    print('Number of modules in the DOM: ' + str(len(modules)) + '; ', end='')

    # Visit the next module
    modules[i].click()
    time.sleep(0.5 * lim)

    # Get id from URL and append it to list
    currId = driver.current_url.split("/")[-1]
    print('module ID %d: %s' % (i + 1, currId))
    idList.append(currId + '\n')

    # Return to the list of modules and increase count
    driver.back()
    time.sleep(0.5 * lim)


# Save the list to a file
with open("id_list.txt", "w") as file:
    file.writelines(idList)
