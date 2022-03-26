"""
Note: Stop using implicitly_wait, its a timewaster. It's best since this is such a dynamic use case, but in terms of speed, its not helping the odds of checking out fast enough (I think)

"""






import AlphaBotScript

import os
import time
from random import randint,uniform

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException
from selenium.webdriver.common.keys import Keys


# Constants
GME_HOME_URL = 'https://www.gamestop.com/'
GME_PRODUCT_URL = 'https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/playstation-5-digital-edition/229026.html'
GME_PRODUCT_TEST_URL = 'https://www.gamestop.com/consoles-hardware/playstation-4/consoles/products/playstation-4-pro-and-cyberpunk-2077-system-bundle-gamestop-premium-refurbished/B134406E.html'
WAIT_TIME = 7


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
    Easy way - Shortcut that goes straight to the prodcut. Not as secure and may get caught
    """
    def shortcut_to_product(self):
        driver = self.driver
        driver.get(GME_PRODUCT_URL)
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))





    """
    Fills out the payment portion of the form
    Note - I'm not sure if I can get away with using a fake name on the CC so I'm just putting my real one. We'll see how it works
    """        
    def payment_form_fill(self):
        driver = self.driver
        cc_info = self.alpha.personal_info['CCInfo']
        
        # identifying each element
        card_num_elem = driver.find_element_by_id('cardNumber')
        expir_date_elem = driver.find_element_by_id('expirationMonthYear')
        cvv_elem = driver.find_element_by_id('securityCode')
        # first_name_elem = driver.find_element_by_id('billingFirstName')
        # last_name_elem = driver.find_element_by_id('billingLastName')

        payment_form_text_box = [card_num_elem, expir_date_elem, cvv_elem]
        payment_form_text_box_values = [cc_info['c_num'], cc_info['c_expiration_date'], cc_info['c_cvv']]
        payment_form_pairs = zip(payment_form_text_box, payment_form_text_box_values)

        # access each element and pass it the appropriate values
        for elem, value in payment_form_pairs:
            elem.clear() # making sure the text boxes are empty
            self.human_type_2(elem,value) # function that mimics human typing
            # elem.send_keys(value)

        driver.find_element_by_name('submit-payment').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 





    """
    Fills out the shipping portion of the form
    
    Note: Inputting the zip code alone will auto fill the city and state, so just skip those two and go straight to the email

    Update: We're still having issues with the street address field, but I've found another issue that occurs whenever I try to click another element after completing the address field. 
            The page slightly refreshes (?) and the email address element is selected... I'm gonna brute force this by essentially clicking on every element, waiting 5 seconds, and then clicking on 
            the same element again. This will fix that issue, and hopefully it fixes the input issues into the address field.
    """
    def shipping_form_fill(self):
        driver = self.driver
        shipping_info = self.alpha.personal_info['ShippingInfo']

        # identifying all the elements - OPTIMIZE BY USING find_element_by_id('blah') instead of xpath etc
        first_name_elem = driver.find_element_by_id("shippingFirstName")
        last_name_elem = driver.find_element_by_id("shippingLastName")
        street_address_elem = driver.find_element_by_id("shippingAddressOne")
        add_apt_num_elem = driver.find_element_by_id('address-two-link') # figure this one out later (look at the link I pasted in the notes for 9/3/21)
        zip_code_elem = driver.find_element_by_id("shippingZipCode")
        # city_elem = driver.find_element_by_id("shippingAddressCity")
        # state_elem = Select(driver.find_element_by_id('shippingState')) # (to "click" value https://stackoverflow.com/questions/63167600/how-to-select-a-value-from-drop-down-menu-in-python-selenium) use state_elem.options to get a list of values. Look for a value that contains 'virginia' and select that index (or just look ahead of time and select that)
        email_addr_elem = driver.find_element_by_id('shipping-email')
        phone_num_elem = driver.find_element_by_id('shippingPhoneNumber')

        shipping_form_text_box_elems = [first_name_elem,last_name_elem,zip_code_elem,email_addr_elem,] # i need to deal with the drop down separately
        shipping_form_text_box_values = [shipping_info['first_name_shipping'], shipping_info['last_name_shipping'], shipping_info['zip_code_shipping'], shipping_info['email_shipping']]
        ship_form_pairs = zip(shipping_form_text_box_elems,shipping_form_text_box_values) # matching the element to the value in tuples
        
        # accesses each element and passes in the appropriate value
        for elem,value in ship_form_pairs:
            elem.clear() # making sure the text boxes are empty
            elem.click() # clicking on the element because of the issue listed above
            time.sleep(5) # waiting 5 seconds because of the issue listed above 
            self.human_type(elem, value) # function that mimics human typing
            # elem.send_keys(value)
            time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 


        # TROUBLESOME FIELDS(state, apt number, address...phone number) - I need to do these ones manually at the end
        
        # STATE
        # state_elem.select_by_value('Virginia') # super annoying that its a drop down

        # PHONE NUMBER - is odd because it adds space-like chars to the input when your done, so my helper function thinks the input is incorrect compared to the OG. 
        phone_num_elem.click()
        time.sleep(5) # waiting 5 seconds because of the issue listed above 
        phone_num_elem.send_keys(shipping_info["phone_number_shipping"])

        # ADDRESS - keeps on acting up
        street_address_elem.click()
        street_address_elem.send_keys(shipping_info["street_addr_shipping"])

        # APT NUMBER - manually inputting apt number since its a two step process
        add_apt_num_elem.click()
        time.sleep(5) # waiting 5 seconds because of the issue listed above 
        driver.find_element_by_id('shippingAddressTwo').send_keys(shipping_info["apt_num_shipping"])
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 

        # UPDATE - apparently i don't even need to click the continue button, it'll just do that automatically :)
        # click the "Save and Continue button"
        driver.find_element_by_name('submit-shipping').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 
        # driver.find_element_by_class_name('btn btn-primary xav-address-btn  mb-2').click() # this should click the first button on the page (It shouldn't matter which one is clicked though)
        # time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 





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
    Helper Function - mimics human typing patterns for text box inputs
    Note: We're having an issue with the send_keys function, so we need to have a delay after sedning a single character. This is no longer humany_type, its boomer_type :(
    I was 2 seconds away from turning this into a static function
    Note: I added a wrapper to the function. To check if the correct text was inputted. 
    """
    def human_type(self,elem, text):
        check = False
        while(check == False):
            elem.clear()
            for char in text:
                elem.send_keys(char)
                time.sleep(uniform(1.0,1.1))
            check = self.confirm_entry(elem, text)






    """
    Helper Function - replica of the function above except there's no check to confirm that what was typed is correct. 
    Note: This fucntion is the result of poor organziation and me being lazy. I'll get rid of this once I clean the code up.
    """
    def human_type_2(self,elem, text):
        elem.clear()
        for char in text:
            elem.send_keys(char)
            time.sleep(uniform(1.0,1.1))






    """
    Helper function - Since I'm having inconsistent issues with the send_keys function, I need to check to make sure that it inputs exactly what I want before moving on. This 
                      function is called after the human type function enters the last character and exits the for loop. I wrap that logic in a while loop and call this check.
                      I extract the value that was just typed into the element, and check it against the text was supposed to be typed. A match will exit the loop, if not, we clear the input and try again.
    """
    def confirm_entry(self, elem, text):
        text_box_val = elem.get_attribute('value')
        return text_box_val == text







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
            self.is_product_in_stock()
            self.path_from_product_page()
            self.close_browser()
            return True
        except InvalidSessionIdException:
            # write something to the log
            return False

        




