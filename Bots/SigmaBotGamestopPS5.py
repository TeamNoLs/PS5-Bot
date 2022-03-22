"""
Note: Stop using implicitly_wait, its a timewaster. It's best since this is such a dynamic use case, but in terms of speed, its not helping the odds of checking out fast enough (I think)

"""






import AlphaBotScript

import os
import time
from random import randint

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException
from selenium.webdriver.common.keys import Keys


# Constants
GME_HOME_URL = 'https://www.gamestop.com/'
GME_PRODUCT_URL = 'https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/playstation-5-digital-edition/229026.html'
GME_PRODUCT_TEST_URL = 'https://www.gamestop.com/consoles-hardware/playstation-4/consoles/products/playstation-4-pro-and-cyberpunk-2077-system-bundle-gamestop-premium-refurbished/B134406E.html'


class SigmaBotGamestopPS5():

    

    """ Constructor """
    def __init__(self, alphabot, configuration={}):
        self.name = "Sigma Gamestop-PS5"
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
    def navigate_to_product(self):
        driver = self.driver
        driver.get(GME_HOME_URL)

        """ Set object Xpath/CSS adresses """
        search_bar_xpath = '/html/body/div/div[3]/header/nav/div[1]/div/div[1]/div[3]/div[1]/form/div[1]/div[2]/input' # dropped the index for the 1st div element since it keeps changing
        ps5_image_xpath = '//a[@href="/consoles-hardware/playstation-5/consoles"]'
        # ps5_digital_item_xpath = '/html/body/div[7]/div[5]/div[3]/div/div[1]/div/div[2]/div[8]/div[1]/div[4]/div/div/div[1]/a'
        ps5_digital_item_xpath = '//a[@href="/consoles-hardware/playstation-5/consoles/products/playstation-5-digital-edition/229026.html"]'

        """ Execute crawl path """

        # Search for "PS5" in the search bar
        search_bar = driver.find_element_by_xpath(search_bar_xpath)
        search_bar.click()
        search_bar.send_keys('PS5')
        search_bar.send_keys(Keys.ENTER)

        # click on ps5 "image" links to the consoles. I'm going this way casue it's faster than going through the menu, and it it consistently takes me to the consoles without anything else being in the way
        ps5_image = driver.find_element_by_xpath(ps5_image_xpath)
        ps5_image.click()

        # click on the digital ps5
        ps5_digital_item = driver.find_element_by_xpath(ps5_digital_item_xpath)
        ps5_digital_item.click()

        # We made it - in_stock function will take over from here





    """ 
    Summary
    -------------------
    Where the bulk of our time is spent. Refreshes the product page until the product is in stock. I need to add in a locking 
    mechanism around the notification bot or else that could get messy if I'm running multiple bots.

    Inputs
    -------------------
    None

    Outputs
    -------------------
    None
    """
    def is_product_in_stock(self):
        driver = self.driver

        # force wait
        time.sleep(5)

        num_attempts = 0
        available = False

        # keeps refreshing the page until the product becomes available
        while(available == False):
            time.sleep(1)
            print(f"Crawling... Attempt #{num_attempts}", end="\r", flush=True) # Track how many attempts it takes           
            check = driver.find_element_by_id('add-to-cart').is_enabled() # see if the button is available or not            
            if check == False:
                num_attempts += 1 # add to counter
                driver.refresh() # refresh page
            
            else: # button is available
                available = True
                self.notification_bot.run(store=self.name)





    """ 
    Summary
    -------------------
    Starts the driver with the specific configurations loaded in.

    Inputs
    -------------------
    None

    Outputs
    -------------------
    None
    """
    def path_from_product_page(self):
        driver = self.driver
  
        """
        Path - ADD TO CART(button) -> VIEW CART(button) -> ? PROCEED TO CHECKOUT(???span???) ? -> GUEST CHECKOUT ->  FILL OUT FORM (SHIPPING, PAYMENT) -> SUBMIT(button)
        """

        # diagnostic stuff
        error_msg = ''

        try: 
            error_msg = 'Broke#1'
            driver.find_element_by_id('add-to-cart').click() 
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

            error_msg = 'Broke#2'
            driver.find_element_by_class_name('view-cart-button').click() 
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

            # these next two are lowkey a shot in the dark .... I'm not sure exactly how to access them so lets go with it
            error_msg = 'Broke#3'
            driver.find_element_by_class_name("checkout-btn-text-mobile").click()
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

            error_msg = 'Broke#4'
            driver.find_element_by_class_name("btn checkout-as-guest").click()

            error_msg = 'Broke#5'
            driver.find_element_by_xpath("//a[@class='btn checkout-as-guest']").click()
                
            error_msg = 'Broke#6'
            driver.find_element_by_xpath("//a[@href='https://www.gamestop.com/spcheckout/']").click()

            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

            # Shipping Form
            error_msg = 'Broke#7'
            self.shipping_form_fill()
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

            # Payment Form 
            error_msg = 'Broke#8'
            self.payment_form_fill()
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

            # Place Order 
            driver.find_element_by_name('submit').click()
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))       

            # that should be it
        except:
            driver.get_screenshot_as_file('Test_this_jaunt_out.png')
            print(f"Something broke. Error code: {error_msg}")
            # self.close_browser() # comment this out so I can manually continue process if need be. 
        





    """ 
    Summary
    -------------------
    Starts the driver with the specific configurations loaded in.

    Inputs
    -------------------
    None

    Outputs
    -------------------
    None
    """
    def close_browser(self):
        print(f"Closing {self.name}")






    """ 
    Summary
    -------------------
    Runs every operation to complete the task

    Inputs
    -------------------
    None

    Outputs
    -------------------
    Boolean confirming whether all the operations ran successfully
    """
    def run(self):
        try:
            self.navigate_to_product()
            # self.is_product_in_stock()
            # self.path_from_product_page()
            # self.close_browser()
            return True
        except InvalidSessionIdException:
            # write something to the log
            return False

        




