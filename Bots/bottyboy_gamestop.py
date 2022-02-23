# We will get that ps5 and become tik tok famous

"""
CONCERNS/COMMENTS/NOTES
Note 9/2/2021: * I want to craete this in a way that allows me to be lazy at first (just to see if I can get away with it), but gives me the freedom to easily add in 
                 additional more complicated layers like security workarounds. Increasing the length of the path taken is a perfect example. Another would be enhanced
                 bot detection measures. These things may or may not be neccesssary, and they are a bit annoyng to have to do up front.

Note 9/3/2021: * I ran into a roadblock that I'm just a little too lazy to fix right now, so I'm just gonna leave the gap in my path for another day. I want to try and 
                 finish as much of the pathing as I can first.
                 This link might help with getting the more obscure elements - https://stackoverflow.com/questions/22529952/using-selenium-to-select-an-anchor-with-specific-content     

Note 9/4/2021: * When I have time it won't hurt to go through and optimize some elements (not structrually). Like using find_element_by_id instead of xpath when applicable. Stuff specific 
                 to Sellenium. No rush, I'd rather get it running first.
               * This link gives great example for how to access a bunch of different kinds of objects using sellenium: https://www.lambdatest.com/blog/locators-in-selenium-webdriver-with-examples/    
               * Don't forget to add in appropriate wait times  so that things can load in before you call them

Note 9/10/2021: * We've made a ton of progress in terms of fixing those super annoying input field errors, but because I'm lazy and just want to get this thing working, my code is getting just
                just a little bit messy. I'll need to go back and clean this jaunt up when I get 100 functionality out of this thing.

Note 11/12/2021: * After getting the batch file running, it broke at attempt 19 (after running for literally 3K cycles last night). It may be beneifical to create a "loop" where if we're under 1K
                   attempts, then I capture the error (write the contents of the error to some text file (is there already a log I can take?)), "reset" the crawler, and the process continues 
                   starting all over again.
                 * Another, more frustrating, scenario that could have occured is that a ps5 became available but was then snatched up too fast. This would cause my bot to proceed and close
                   the browser. This is a possibility since I've never gotten this error before. Actually no... idk.
                 * Using this website (https://piprogramming.org/articles/How-to-make-Selenium-undetectable-and-stealth--7-Ways-to-hide-your-Bot-Automation-from-Detection-0000000017.html) to try 
                   and bypass bot detection from these websites. Might be a good idea to think about switching to using chrome (ultrafunkamsterdam's chrome driver)

Note 11/16/2021: * I'm trying to research whether hardcoding element locations vs "wildcard" shorthand (// or *) vs. find_by_id is faster. From what I've seen it looks like css path is faster 
                   than xpath so I'll eventually need to recode everything in css path (not as bad as it sounds)

Note 11/17/2021: * I'm trying to write css/xpath strings but I'm not finding the elements for some reason... it feels like there's something I'm not fundamentally getting because this stuff is 
                   pretty easy. For now, I can use a stop gap where I simply grab the css/xpath from the dev tools in firefox(literal copy and paste). The downside is that its the literal path 
                   instead of a shorthand. The literal path is much more prone to breakage, but if it gets it working...for now

Note 11/19/2021: * So Gamestop updated their website today (updated their banner for black friday, very minor), and the script broke because a single element was shifted. This is the risk of using the 
                   hardcoded paths.

Note 11/19/2021: * Gamestop bot V1 is complete! I still need to deal with the really large number of requests that I'm making after a certain amount of time. I can get around this by restarting the 
                   browser every 100 attempts or something like that. This could be an important addition since we may get blocked otherwise. Another top of mind update that I'd like to do is replace
                   all the xpath code with css paths. It's not essetnial, but it'll speed things up. Other than some coding structure stuff that I talk about above, this is ready to go.

Note 11/26/2021: * I got blocked. Gonna creeate a new function that shuts down the bot after 250 attempts and reconnects using a new web driver configuration (basically using a vpn and crap)
"""
"""
UPDATES TO THE CODE

Update 11/11/2021: * Added functionality to screenshot the browser when something breaks.
                   * Created a batch file that allows me to use windows task scheduler to run the program automatically for me at some set time

Update 11/16/2021: * Added the implicit wait feature in the constructor. This allows the driver to proceed immediately after it accesses an element or to wait for the specified amount of time 
                     for the element to appear. I can get rid of the tedious time.sleep lines, but I'll leave a couple sprinkled in there to avoid any harsh bot detection.

Update 11/18/2021: * Completed the "long path" where I start from the home path. It might be a good idea to start from google, but I'll save that for another day...

"""


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  # We might use
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException

import random
from random import randint, randrange
import time


from secrets import gamestop_username, gamestop_password,first_name_shipping, last_name_shipping,street_addr_shipping,apt_num_shipping,zip_code_shipping,city_gme_shipping,state_shipping,email_shipping,phone_number_shipping, c_expiration_date, c_num, c_cvv, c_first_name, c_last_name
from  email_notification_system import email_bot



# CONSTANTS
GME_HOME_URL = 'https://www.gamestop.com/'
GME_PRODUCT_URL = 'https://www.gamestop.com/consoles-hardware/playstation-5/consoles/products/playstation-5-digital-edition/229026.html'
GME_PRODUCT_TEST_URL = 'https://www.gamestop.com/consoles-hardware/playstation-4/consoles/products/playstation-4-pro-and-cyberpunk-2077-system-bundle-gamestop-premium-refurbished/B134406E.html'
WAIT_TIME = 5
IMPPLICIT_WAIT_TIME = 10


class bottyboy_gamestop:

    """
    Constructor
    """
    def __init__(self):
        """" Initializes Bot with class-wide variables. """
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(IMPPLICIT_WAIT_TIME) # the driver will now immediately execute the next command or wait up to X seconds
        print("Let's get it")

    """
    Restarts the driver and starts up another browser - There's a chance I lose connection, for whatever reason, this essentially restarts the process automatically
    """
    def reestablish_connection(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(IMPPLICIT_WAIT_TIME) # the driver will now immediately execute the next command or wait up to X seconds
        print("Let's get it...again")

    """
     Secure way - Using a bunch of techniques to avoid bot detection. This only deals with the configuration techniques.
    """
    def set_driver_configuration(self):

        option = self.driver.FirefoxOptions()

        
        # Option 1: removing navigator.webdriver flag - the standard way websites are able to tell if an automation tool is being used (this goes after the browser is open)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Option 2: changing IP addresses by using Proxy's (need to get a private proxy, paid works the best)
        option.add_argument('proxy-server=106.122.8.54:3128')

        print('a')


    """ 
    Hard Way - Path starting from the homepage
    """
    def navigate_to_product(self):
        driver = self.driver
        driver.get(GME_HOME_URL)
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))

        # This is the shorter path that isn't working because I can't click on the console icon
        search_bar_xpath = '/html/body/div/div[3]/header/nav/div[1]/div/div[1]/div[3]/div[1]/form/div[1]/div[2]/input' # dropped the index for the 1st div element since it keeps changing
        ps5_image_xpath = '//a[@href="/consoles-hardware/playstation-5/consoles"]'
        # ps5_digital_item_xpath = '/html/body/div[7]/div[5]/div[3]/div/div[1]/div/div[2]/div[8]/div[1]/div[4]/div/div/div[1]/a'
        ps5_digital_item_xpath = '//a[@href="/consoles-hardware/playstation-5/consoles/products/playstation-5-digital-edition/229026.html"]'

        # Crawl Path

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


    """ 
    Easy way - Shortcut that goes straight to the prodcut
    """
    def shortcut_to_product(self):
        driver = self.driver
        driver.get(GME_PRODUCT_URL)
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME))
   

    """
    Checks the availability oof the product on the product page. Refreshes and waits for the product to eventually become available
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
                notifcation_bot.run()
                print("I think we hooked one")

  
                

    """
    Navigates from the product page to complete the process
    Helpful Link - https://www.lambdatest.com/blog/locators-in-selenium-webdriver-with-examples/
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
    Fills out the payment portion of the form
    Note - I'm not sure if I can get away with using a fake name on the CC so I'm just putting my real one. We'll see how it works
    """        
    def payment_form_fill(self):
        driver = self.driver
        
        # identifying each element
        card_num_elem = driver.find_element_by_id('cardNumber')
        expir_date_elem = driver.find_element_by_id('expirationMonthYear')
        cvv_elem = driver.find_element_by_id('securityCode')
        # first_name_elem = driver.find_element_by_id('billingFirstName')
        # last_name_elem = driver.find_element_by_id('billingLastName')

        payment_form_text_box = [card_num_elem, expir_date_elem, cvv_elem]
        payment_form_text_box_values = [c_num, c_expiration_date, c_cvv]
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
        shipping_form_text_box_values = [first_name_shipping, last_name_shipping,zip_code_shipping,email_shipping]
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
        phone_num_elem.send_keys(phone_number_shipping)

        # ADDRESS - keeps on acting up
        street_address_elem.click()
        street_address_elem.send_keys(street_addr_shipping)

        # APT NUMBER - manually inputting apt number since its a two step process
        add_apt_num_elem.click()
        time.sleep(5) # waiting 5 seconds because of the issue listed above 
        driver.find_element_by_id('shippingAddressTwo').send_keys(apt_num_shipping)
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 

        # UPDATE - apparently i don't even need to click the continue button, it'll just do that automatically :)
        # click the "Save and Continue button"
        driver.find_element_by_name('submit-shipping').click()
        time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 
        # driver.find_element_by_class_name('btn btn-primary xav-address-btn  mb-2').click() # this should click the first button on the page (It shouldn't matter which one is clicked though)
        # time.sleep(randint(int(WAIT_TIME / 2), WAIT_TIME)) # may need to be longer 

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
        check = False
        while(check == False):
            elem.clear()
            for char in text:
                elem.send_keys(char)
                time.sleep(random.uniform(1.0,1.1))
            check = self.confirm_entry(elem, text)

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
        text_box_val = elem.get_attribute('value')
        return text_box_val == text

    """
    Calls all the neccessary functions to run the bot. Wrapped in a loop to restart the connection if we lose connection for some reason
    """
    def run(self):

        not_connected = True
        while(not_connected == True):
            try:
                self.navigate_to_product()
                self.is_product_in_stock()
                self.path_from_product_page()
                self.close_browser()
                not_connected = False
                print("Congratulations you cheeky boy")
                not_connected = False
            except InvalidSessionIdException:
                # self.close_browser() # might not need this but i don't remember
                self.reestablish_connection()
        
        print("Good work son...go rest now")
        pass
        


if __name__ == '__main__':
    gm_shopBot = bottyboy_gamestop()
    notifcation_bot = email_bot("Gamestop")
    gm_shopBot.run()
    








