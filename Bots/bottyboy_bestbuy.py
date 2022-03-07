"""
CONCERNS/COMMENTS/NOTES

Note 11/17/2021: * I'm gonna save all of the element locations an "Element Pathing" section. It's more so for better readability and I think
                   its easier to work with having all the element paths saved befroe hand. Might even be a good idea to have a separate file, but I'm not sure if that would slow down performance

Note 11/20/2021: * Some items aren't able to be shipped an are available for in store pickup. I essentially need to code two different checkout fuctnions: 1. where i can ship the item, or 2 where 
                   i can pick the item up from the store. More work. I did some digging, I can do a check after I've already added the console to my cart. That way I don't slow down the bot 
                   unneccessarily. I basically look to see if a certain radio button is present. If it is, I'll take path B.


""" 
"""
UPDATES TO THE CODE

"""


from _typeshed import Self
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException

import random
from random import randint
import time

from secrets import first_name_shipping, last_name_shipping,street_addr_shipping,apt_num_shipping,zip_code_shipping,city_gme_shipping,state_shipping,email_shipping,phone_number_shipping, c_expiration_date, c_num, c_cvv, c_first_name, c_last_name

from bottyboy_gamestop import IMPPLICIT_WAIT_TIME

# Constants
BEST_BUY_HOME_URL = "https://www.bestbuy.com/"
BEST_BUY_PRODUCT_URL = "https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161"
BEST_BUY_TEST_URL = ""
IMPPLICIT_WAIT_TIME = 10 # upper bound for how long I'll wait for an element to appear on the page

"""
Element Pathing - String variables for the html paths on any element I need to interact with
"""
search_bar_xpath = '//*[@id="gh-search-input"]' # search bar
ps5_digitial_xpath = '//a[@href="/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161"]' # ps5 digital icon
add_to_cart_button_xpath = '//button[@data-button-state="ADD_TO_CART"]' # add to cart button

go_to_cart_button_xpath = '//a[@href="/cart"]' # go to cart button (pop up window)
checkout_button_xpath = '//button[@data-track="Checkout - Top"]' # checkout button
guest_checkout_xpath = '//button[@class="c-button c-button-secondary c-button-lg cia-guest-content__continue guest"]' # continue as guest checkout





class bottyboy_best_buy:

    """
    Constructor
    """
    def __init__(self):
        """" Initializes Bot with class-wide variables. """
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(IMPPLICIT_WAIT_TIME) # the driver will now immediately execute the next command or wait up to X seconds
        print("Let's get it")

    def reestablish_connection(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(IMPPLICIT_WAIT_TIME) # the driver will now immediately execute the next command or wait up to X seconds
        print("Let's get it...again")

    def set_driver_configuration(self):
        pass

    """ 
    Hard Way - Path starting from the homepage
    """
    def navigate_to_product(self):
        driver = self.driver
        driver.get(BEST_BUY_HOME_URL)
        time.sleep(2)
        
        # click, insert "ps5", and search
        search_bar = driver.find_element_by_xpath(search_bar_xpath)
        search_bar.click()
        search_bar.send_keys("PS5")
        search_bar.send_keys(Keys.Enter)

        # click the icon
        driver.find_element_by_xpath(ps5_digitial_xpath).click()



    """ 
    Easy way - Shortcut that goes straight to the prodcut
    """
    def shortcut_to_product(self):
        pass


    """
    Checks the availability oof the product on the product page. Refreshes and waits for the product to eventually become available
    """
    def is_product_in_stock(self):
        driver = self.driver
        time.sleep(2)

        num_attempts = 0
        available = False

        

        # keeps refreshing the page until the product becomes available
        while(available == False):
            time.sleep(1)
            print(f"Crawling... Attempt #{num_attempts}", end="\r", flush=True) # Track how many attempts it takes           
            check = driver.find_element_by_xpath(add_to_cart_button_xpath).is_enabled() # see if the button is available or not            
            if check == False and num_attempts > 250:
                self.close() # turn this into a reconnect function where the bot closes, uses a new configuration and consiues the search
            
            elif check == False and num_attempts <= 250:
                num_attempts += 1 # add to counter
                driver.refresh() # refresh page
            
            else: # button is available
                available = True
                notifcation_bot.run()
                print("I think we hooked one")


    """
    Navigates from the product page to complete the process
    Helpful Link - https://www.lambdatest.com/blog/locators-in-selenium-webdriver-with-examples/
    """
    def path_from_product_page(self):
        pass
        


    """
    Fills out the payment portion of the form
    Note - I'm not sure if I can get away with using a fake name on the CC so I'm just putting my real one. We'll see how it works
    """        
    def payment_form_fill(self):
     pass



    """
    Fills out the shipping portion of the form
    
    Note: Inputting the zip code alone will auto fill the city and state, so just skip those two and go straight to the email

    Update: We're still having issues with the street address field, but I've found another issue that occurs whenever I try to click another element after completing the address field. 
            The page slightly refreshes (?) and the email address element is selected... I'm gonna brute force this by essentially clicking on every element, waiting 5 seconds, and then clicking on 
            the same element again. This will fix that issue, and hopefully it fixes the input issues into the address field.
    """
    def shipping_form_fill(self):
       pass


    """
    Closes the Browser (We should have our PS5 on the way :) 
    """
    def close_browser(self):
        self.driver.close()


    """
    Helper Function - mimics human typing patterns for text box inputs
    Note: We're having an issue with the send_keys function, so we need to have a delay after sedning a single character. This is no longer humany_type, its boomer_type :(
    I was 2 seconds away from turning this into a static function
    Note: I added a wrapper to the function (I think thats what its called). To check if the correct text was inputted. 
    """
    def human_type(self,elem, text):
       pass

    """
    Helper Function - replica of the function above except there's no check to confirm that what was typed is correct. 
    Note: This fucntion is the result of poor organziation and me being lazy. I'll get rid of this once I clean the code up.
    """
    def human_type_2(self,elem, text):
        elem.clear()
        for char in text:
            elem.send_keys(char)
            time.sleep(random.uniform(1.0,1.1))


    """
    Helper function - Since I'm having inconsistent issues with the send_keys function, I need to check to make sure that it inputs exactly what I want before moving on. This 
                      function is called after the human type function enters the last character and exits the for loop. I wrap that logic in a while loop and call this check.
                      I extract the value that was just typed into the element, and check it against the text was supposed to be typed. A match will exit the loop, if not, we clear the input and try again.
    """
    def confirm_entry(self, elem, text):
        pass

    """
    Calls all the neccessary functions to run the bot. Wrapped in a loop to restart the connection if we lose connection for some reason
    """
    def run(self):

        not_connected = True
        while(not_connected == True):
            try:
                self.navigate_to_product()
                gm_shopBot.shortcut_to_product()
                self.is_product_in_stock()
                self.path_from_product_page()
                self.close_browser()
                not_connected = False
                print("Congratulations you cheeky boy")
            except InvalidSessionIdException:
                self.close_browser() # might not need this but i don't remember
                self.reestablish_connection()
        





if __name__ == '__main__':
    gm_shopBot = bottyboy_best_buy()
    gm_shopBot.run()
    

































