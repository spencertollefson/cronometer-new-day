"""Created on 11-Feb-18.
Author: Spencer Tollefson
Description: cronometerNewDay.py - Copy my Cronometer chart from the previous
             and reset most of the inputs to 0.
"""

import time
start = time.time()
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import logging
logging.basicConfig(level=logging.DEBUG,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)
logging.getLogger("selenium").setLevel(logging.WARNING)

# Chromedriver file location.
driver_location = "ABSOLUTE PATH TO CHROMEDRIVER.EXE HERE"

# Opt for headless and English language
options = webdriver.ChromeOptions()
logging.debug('running headless')
options.set_headless(headless=True)
options.add_argument('--lang=en-GB')  # en-US didn't work, so used GB

# Find webdriver.Chrome wherever saved locally.
browser = webdriver.Chrome(executable_path=driver_location,
                           chrome_options=options)

# Set wait for Expected Conditions - this will be used to allow loading
wait = WebDriverWait(browser, 10)

# Function to move to the next day in advance
def nextday():
    nextxpath = '//*[@id="cronometerApp"]/div/div[1]/div/table/tbody/tr/td[1]/div/div[1]/div/button[2]'
    element = wait.until(EC.visibility_of_element_located((By.XPATH, nextxpath)))
    return browser.find_element_by_xpath(nextxpath).click()


# Playground
try:
    browser.get("http://cronometer.com")

    # Login to account
    Login = browser.find_element_by_class_name('button--1')
    Login.click()
    Username = browser.find_element_by_name('username')
    Password = browser.find_element_by_name('password')
    element = wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
    Username.send_keys('INPUT_USERNAME_HERE')
    Password.send_keys('INPUT_PW_HERE')
    Password.send_keys(Keys.ENTER)

    # TODO Sometimes an upgrade thing pops up. If it does, Exit out of it then continue. simply need an if clause like below:
        # if XYZ field is present:
            # click the X to get out of it

    # TESTING ONLY. Change date forward 1 day. Tomorrow.
    # nextday()

    # Copy Yesterday's Diary to Today.
    logging.debug('made it before click the box')
    xpathforsettings = '//*[@id="cronometerApp"]/div/div[1]/div/table/tbody/tr/td[2]/div/div[1]/button[5]'
    element = wait.until(
        EC.visibility_of_element_located((By.XPATH, xpathforsettings)))
    browser.find_element_by_xpath(xpathforsettings).click() # Open settings button.
    logging.debug('clicked the box')
    # browser.find_element_by_class_name('GL-TVABCFNB brighten br-unhover').click()  # Open settings button.
    myxpath2 = '/html/body/div[3]/div/table/tbody/tr[3]/td/div'
    logging.debug('about to wait for EC visibility of xpath')
    element = wait.until(EC.visibility_of_element_located((By.XPATH, myxpath2)))
    browser.find_element_by_xpath(myxpath2).click() # Wait then click Copy Prev Day
    logging.debug('clicked the Copy Prev Day button')

    # Set values for all food to 0.
    try:
        '''
        As XPATH has 1 number change for each row, iterate up 1
        incrementally and each time use it to find the serving size field
        enter 0 into it to reset yesterday's serving, and then hit Enter
        '''
        logging.debug('Entering the loop')
        for i in range(2, 100):
            old = time.time()
            logging.debug('got first time')

            keyxpath = f'// *[ @ id = "cronometerApp"] / div / div[1] / div / table / tbody / tr / td[2] / div / div[2] / table / tbody / tr[{i}] / td[3] / div'
            logging.debug('Set key path')

            element = WebDriverWait(browser, 1).until(EC.visibility_of_element_located((By.XPATH, keyxpath))) # I changed wait out for WebDriverWait here
            logging.debug('Did element wait')

            serving = browser.find_element_by_xpath(keyxpath).click()
            logging.debug('Set serving to keyxpath and clicked')

            number = browser.find_element_by_xpath(f'//*[@id="cronometerApp"]/div/div[1]/div/table/tbody/tr/td[2]/div/div[2]/table/tbody/tr[{i}]/td[3]/input')
            logging.debug('selected the input box field. Next step is entering into it')

            number.send_keys('0', Keys.ENTER)
            logging.debug('set number to keyxpath and entered 0 then ENTER')

            interval = time.time() - old
            logging.info(f'i completed # {i}. {interval} seconds')

            time.sleep(0.3) # TODO: improve this by some sort of WebDriverWait function here. 0.15 seconds was too fast, 0.5 though ran well.
    except:
        logging.info('Broke the for loop and triggered Except line')
finally:
    browser.quit()
    print('Completed in: ' + str(time.time() - start) + ' seconds')
