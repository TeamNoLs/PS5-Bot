"""
PURPOSE
-------------------
A task for my alphabot. Create a sellenium webdriver object, goes to Gamestop website, and snags me a ps5. 


"""






from AlphaBot import AlphaBot

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException
from selenium.webdriver.common.keys import Keys


# Constants
GME_HOME_URL = 'https://www.gamestop.com/'
GME_PRODUCT_URL = 'https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/playstation-5-digital-edition/229026.html'
GME_PRODUCT_TEST_URL = 'https://www.gamestop.com/consoles-hardware/playstation-4/consoles/products/playstation-4-pro-and-cyberpunk-2077-system-bundle-gamestop-premium-refurbished/B134406E.html'


class SigmaBotGamestopPS5(AlphaBot):

    iWait = AlphaBot.IMPPLICIT_WAIT_TIME

    """ Constructor """
    def __init__(self, configuration={}):
        self.name = "Sigma Gamestop-PS5"
        self.driver = webdriver.Firefox() # initates webdriver (firefox)
        self.driver.implicitly_wait(iWait)

    



    """ 
    Summary
    -------------------
    Sets up the driver according to the tasks specific requirments

    Inputs
    -------------------
    config_params <dictionary> :: {"specification": value}, indicates which specifications need to be set as well as gives the vale
                                  for that specification.

    Outputs
    -------------------
    Congratulotory statement
    """
    def configuration(self, config_params={}):
        options = Options()
        
        """ Free up resources """
        options.add_argument('--no-sandbox')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-default-apps')

        # Requirements
        # options.binary_location = '/opt/chrome-linux.63.0.3239.b.508580/chrome'
    
    
    def start_driver(self):
        pass


    def navigate_to_product(self):
        driver = self.driver
        driver.get(GME_HOME_URL).implicitly_wait(iWait)

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
        print("All right lets begin...")

    def is_product_in_stock(self):
        pass

    def path_from_product_page(self):
        pass

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

        




