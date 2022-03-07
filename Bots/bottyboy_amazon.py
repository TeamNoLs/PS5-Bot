# We will get that ps5 and become tik tok famous
# I need to set up the home address, payment method, and everything else I would need to make a purchase in advance
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  #We might use
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
import random
from random import randint, randrange
import time
from secrets import amazon_username, amazon_password


AMAZON_NEW_URL = 'https://www.amazon.com/PlayStation-5-Digital/dp/B09DFHJTF5/ref=sr_1_10?brr=1&pd_rd_r=4a4efe23-8b85-41b8-8d51-a331c3a3b807&pd_rd_w=LojOc&pd_rd_wg=IuEJE&qid=1637543577&rd=1&refinements=p_89%3APlayStation&rnid=2528832011&s=videogames&sr=1-10'
AMAZON_REFURB_URL = 'https://www.amazon.com/PlayStation-5-Digital-Renewed/dp/B08Z8JV4RB/ref=sr_1_5?brr=1&pd_rd_r=4a4efe23-8b85-41b8-8d51-a331c3a3b807&pd_rd_w=LojOc&pd_rd_wg=IuEJE&qid=1637543577&rd=1&refinements=p_89%3APlayStation&rnid=2528832011&s=videogames&sr=1-5'
AMAZON_TEST_URL = 'https://www.amazon.com/Sony-Playstation-1TB-Console-Controller/dp/B08X2VZX7X/ref=sr_1_5?crid=G30YOHY3QCZE&dchild=1&keywords=playstation+4&qid=1620492941&sprefix=playst%2Caps%2C171&sr=8-5'
WAIT_TIME = 5
IMPPLICIT_WAIT_TIME = 10
PRICE_LIMIT = 700.0 # UPPER LIMIT FOR WHAT I'LL PAY

"""
ELEMENT PATHING - SET ALL THE VARIABLES THAT HOLD THE PATH TO EVERY ELEMENT I NEED TO INTERACT WITH
"""




class bottyboy:
    def __init__(self, username, password):
        """" Initializes Bot with class-wide variables. """
        self.username = username
        self.password = password
        self.count = 0 # running counter
        self.driver = webdriver.Firefox()

    # Sign in to the site with the product
    def signIn(self):
        """
        Sign into site with the product
        """
        driver = self.driver 

        ## Enter Username
        username_elem = driver.find_element_by_xpath("//input[@name='email']")
        username_elem.clear()

        username_elem.send_keys(self.username)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        username_elem.send_keys(Keys.RETURN)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        ## Enter Password
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()

        password_elem.send_keys(self.password)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

        password_elem.send_keys(Keys.RETURN)
        time.sleep(randint(int(WAIT_TIME/2), WAIT_TIME))

    ## Find the product under x amount
    def findProduct(self):
        """
        Finds the product with the global link
        """
        isAvailable = False # setting the conditional - used to refresh page and try again
        while(isAvailable == False):
            # load the page
            driver = self.driver
            driver.get(AMAZON_URL)
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
            
            # checking if the product is available
            isAvailable = self.isProductAvailable()

        ## if the product is not availabe, wait until it is available
        isAvailable = self.isProductAvailable()
        if isAvailable == 'Currently unavailable.':
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
            self.findProduct()

        elif isAvailable <= PRICE_LIMIT:
            ## Buy Now
            buy_now = driver.find_element_by_name('submit.buy-now')
            buy_now.click()
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
            self.signIn()

            ## Place the order
            place_order = driver.find_element_by_name('placeYourOrder1')
            place_order.click()
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

        else:
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
            self.findProduct()

    def isProductAvailable(self):
        """
        Checks if product is available
        """
        self.count = self.count + 1 # using a running counter to see how many times this thing runs

        driver = self.driver
        available = driver.find_element_by_class_name('a-color-price').text
        if available == 'Currently unavailable.':
            print(f'**** ATTEMPT #{self.count} --- {available}')
            return available
        else:
            print(f'***** Price: {available}')
            return float(available[1:]) ## $123.22 -> 123.22

    def closeBrowser(self):
        """
        Closes Browswer
        """
        self.driver.close()

if __name__ == '__main__':
    # print(amazon_password)
    shopBot = bottyboy(username=amazon_username, password=amazon_password)
    shopBot.findProduct()
    shopBot.closeBrowser()
