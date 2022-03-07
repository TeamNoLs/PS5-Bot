# We will get that ps5 and become tik tok famous
# I need to set up the home address, payment method, and everything else I would need to make a purchase in advance
# Looks like Target can track when selenium is being used and doesn't allow the user to sign in (L)

"""
CONCERNS/COMMENTS/NOTES

Concern 6/1/2021: * Target is identifying me as a bot. I'm researching ways now to avoid detection. Am I a hacker? 

Concern 6/9/2021: * I feel like refreshing the page 1000 times during the same session is just asking to get flagged as a bot. I should
                   research how useful it would be to close out of the browser and start the process again. 

Note 6/9/2021: * I can add in some random mouse movements and clicks in between "progressive actions" (actions that move me forward in the process)
                 instead of just waiting. 
               * Making requests through proxies and using multpile outgoing IP addresses
               * I should be using a large list of fake user agents and rotating through them (By default, most web scraping software don't have user agents).
                 I can also send in more request headers (depending on what the site looks for).
                 Source - https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/
               * d

Note 6/11/2021: * I found a good stack overflow that led me to a site that has a giant list of user agents. I'm not exactly sure what criteria i need to have
                  match up for it to work (does the firefox version matter?).
                  Source - https://developers.whatismybrowser.com/useragents/explore/software_name/firefox/
                           https://stackoverflow.com/questions/53161173/how-to-rotate-various-user-agents-using-selenium-python-on-each-request
                
"""
"""
UPDATES TO THE CODE

Update 6/9/2021: This script is now specifically for getting a Nintendo Switch. I'm changing the route to start at the Target homepage
                 and navigate its way to the console listing. A new function for navigating to the console listing will be implemented,
                 and from there, the script will proceed in the same way as before.  
"""
from bottyboy import WAIT_TIME
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  #We might use
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException
import random
from random import randint, randrange
import time
from secrets import target_username, target_password, c_num,c_cvv

TARGET_URL = "https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596#lnk=sametab"
TARGET_TEST_URL = "https://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-77464002#lnk=sametab"
TARGET_HOME_URL = "https://www.target.com/"
WAIT_TIME = 6


class bottyboy_target:
    def __init__(self, username, password,card_number, card_cvv):
        """" Initializes Bot with class-wide variables. """
        self.driver = webdriver.Firefox()
        self.username = username
        self.password = password
        self.card_number = card_number
        self.card_cvv = card_cvv

        

    def set_driver_configuration(self):
        """
        Additional settings for the driver to help get through bot detection
        """


        profile = webdriver.FirefoxProfile()
        option = webdriver.FirefoxOptions()
        # option.add_argument('window_size=1280,800') # Its already max screen by itself

        # changing the user agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0" # default user agent
        profile.set_preference("general.useragent.override", user_agent)


        driver = webdriver.Firefox(firefox_profile=profile,options=option) 
        # Remove navigator.webdriver Flag using JavaScript
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")


        # Change Browser Options


    def signIn(self):
        """
        Sign into site with the product
        "I could improve this by throwing in a keystroke function instead of a copy/paste for username/password
        """
        driver = self.driver 

        # enter username
        username_elem = driver.find_element_by_xpath("//input[@name='username']")
        username_elem.clear()
        username_elem.send_keys(self.username) # sending in the username
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

        # enter password
        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password) # sending in the password
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

        # sign in button
        driver.find_element_by_xpath('//button[normalize-space()="Sign in"]').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))



    def navigate_to_product(self):
        driver = self.driver
        driver.get(TARGET_HOME_URL)
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
        driver



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
        card_number_elem = driver.find_element_by_xpath("//input[@name='cardnumber']")
        card_number_elem.clear()
        card_number_elem.send_keys(self.card_number)

        driver.find_element_by_xpath("//input[@name='cvc']")
        card_number_elem.clear()
        card_number_elem.send_keys(self.card_cvv)

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
    
    def closeBrowser(self):
        """
        Closes Browswer
        """
        self.driver.close()



if __name__ == '__main__':
    print('Ready 1')
    shopBot = bottyboy_target(username=target_username, password=target_password, card_number=c_num, card_cvv=c_cvv)
    shopBot.set_driver_configuration() # if I want to use enhanced features to get by security 
    shopBot.findProduct()
    shopBot.closeBrowser()

    user_agent_list = ["Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0", "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0","Mozilla/5.0 (Windows NT 5.1; rv:36.0) Gecko/20100101 Firefox/36.0","Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0"]





