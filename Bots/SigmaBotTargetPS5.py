import AlphaBotScript

import os
import time
from random import randint,uniform
import random
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException


TARGET_URL = "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596#lnk=sametab"
TARGET_TEST_URL = "https://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-77464002#lnk=sametab"
TARGET_HOME_URL = "https://www.target.com/"
WAIT_TIME = 6





class SigmaBotTargetPS5():

    """ Constructor """
    def __init__(self, alphabot, configuration={}):
        self.name = "Sigma Target-PS5"
        self.alpha = alphabot
        self.iWait = alphabot.IMPPLICIT_WAIT_TIME
        self.notification_bot = alphabot.notification_bot





    """ 
    Summary
    -------------------
    Sets up the driver according to the tasks specific requirments. Need to add choice to what driver the user can use (might check requirements file)
    
    Inputs
    -------------------
    lightweight <bool> :: utilizes settings that free up browser resources to allow for faster compute
    stealth <bool> :: determines whether the bot will utilize proxy rotations to hide IP addresses

    Outputs
    -------------------
    Options object loaded with all desired settings
    """
    def configuration(self, lightweight=True, stealth=False):
        options = Options()
        
        """ Free up resources """
        if lightweight:
            options.add_argument('--no-sandbox')
            options.add_argument('--no-default-browser-check')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-default-apps')

        """ Include/Envoke tactics to avoid detection """
        if stealth:

            PROXY_STR = self.alpha.get_proxy() # returns -1 if proxy not available
            if type(PROXY_STR) == str:
                options.add_argument('--proxy-server=%s' % PROXY_STR)
            else:
                pass

        return options





    """ 
    Summary
    -------------------
    Starts the driver with the specific configurations loaded in.

    Inputs
    -------------------
    config_params <dictionary> :: {"specification": value}, indicates which specifications need to be set as well as gives the vale
                                  for that specification.

    Outputs
    -------------------
    None
    """
    def start_driver(self, options):
        exec_path = os.path.join( os.getcwd(), 'Requirements\geckodriver-v0.29.1-win64\geckodriver.exe' )
        self.driver = webdriver.Firefox(options=options, executable_path=exec_path)
        self.driver.implicitly_wait(self.iWait)

    




    # find product for x amount - (target sells it for retail value so don't worry about price)
    def findProduct(self):
        """
        Finds the product with the global link
        """
        isAvailable = False # setting the conditional - used to refresh page and try again
        while(isAvailable == False):

            # load the page
            driver = self.driver
            driver.get(TARGET_TEST_URL)
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
            
            # checking if the product is available
            isAvailable = self.isProductAvailable()
        
        # The console is available - click "Ship it" button
        driver.find_element_by_xpath('//button[normalize-space()="Ship it"]').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
        # Decline "Protect your purchase popup"
        driver.find_element_by_xpath('//button[normalize-space()="Decline coverage"]').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
        # "View Cart and Checkout popup"
        driver.find_element_by_xpath('//button[normalize-space()="View cart & checkout"]').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
        # "I'm ready to check out" button
        driver.find_element_by_xpath("""//button[normalize-space()="I'm ready to check out"]""").click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

        # sign in
        self.signIn()

        # input card number and cvv at checkout
        cc_info = self.alpha.personal_info['CCInfo']

        card_number_elem = driver.find_element_by_xpath("//input[@name='cardnumber']")
        card_number_elem.clear()
        card_number_elem.send_keys(cc_info['c_num'])

        driver.find_element_by_xpath("//input[@name='cvc']")
        card_number_elem.clear()
        card_number_elem.send_keys(cc_info['c_cvv'])

        # Finish and hit "Place you order"
        # driver.find_element_by_xpath('//button[normalize-space()="Place your order"]').click()
        driver.find_element_by_xpath('//button[normalize-space()="Place your order"]').text()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
        print("Ayyooooooo")





    def isProductAvailable(self):
        """
        Checks if product is available
        """
        driver = self.driver
        available = driver.find_element_by_xpath('//button[normalize-space()="Ship it"]').text
        print(available)
        if available == "Ship it":
            print("Availability: This bastard really found one")
            return True
        else:
            print("Availabillity: Unavailable")
            return False





    def signIn(self):
        """
        Sign into site with the product
        "I could improve this by throwing in a keystroke function instead of a copy/paste for username/password
        """
        driver = self.driver 
        login_info = self.alpha.personal_info['Target']

        # enter username
        username_elem = driver.find_element_by_xpath("//input[@name='username']")
        username_elem.clear()
        username_elem.send_keys(login_info['target_username']) # sending in the username
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

        # enter password
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(login_info['target_password']) # sending in the password
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

        # sign in button
        driver.find_element_by_xpath('//button[normalize-space()="Sign in"]').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))    







    def close_browser(self):
        """
        Closes Browswer
        """
        self.driver.close()






    def run(self):
        try:
            self.findProduct()
            self.close_browser()
            return True
        except InvalidSessionIdException:
            # write something to the log
            return False
