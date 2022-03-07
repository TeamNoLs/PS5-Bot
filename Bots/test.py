"""
Prep - Need to install webdriver and save it in local directory (I think, maybe just save where compiler/excecutable is)
     - Install sellenium 

I'm going to write out the steps for creating this scraper, just so Rachel can read it very easily, and in case for future use
"""

# Set up all of your imports (used to bring in neccessary packages)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, InvalidSessionIdException

from random import randint, randrange
import time

""" Just setting important variables in one place so its easy to manuever"""
# Set key variables
IMPLCIT_WAIT_TIME = 10 # want to take into account lag time for the program to "find" objects
url = 'https://fred.stlouisfed.org/' # website we're going to be scraping

search_bar_xpath = '//input[@class="form-control search-input-homepage"]' # allows us to click on search bar
search_item = "delinquency" # what we type into the search bar
variable_item_xpath = '//a[@href="/series/DRCCLACBS"]' # the link/item we click on to get to the page (variable, could change as website is updated)
download_xpath = '//span[@class="fg-download-btn-gtm"]'
csv_xpath_href = '/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=968&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DRCCLACBS&scale=left&cosd=1991-01-01&coed=2021-07-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly%2C%20End%20of%20Period&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-12-07&revision_date=2021-12-07&nd=1991-01-01'
test_path = 'https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1168&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=DRCCLACBS&scale=left&cosd=1991-01-01&coed=2021-07-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Quarterly%2C%20End%20of%20Period&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2021-12-07&revision_date=2021-12-07&nd=1991-01-01'
csv_xpath = '//a[@id="download-data-csv"]'
# csv_xpath = '//a[@href="{}"]'.format(csv_xpath_href)




""" This creates an object ot connect to the internet """
# Intiate Webdriver
driver = webdriver.Firefox()
driver.implicitly_wait(IMPLCIT_WAIT_TIME)
print('Driver is up and running')


driver.get(url)
search_bar = driver.find_element_by_xpath(search_bar_xpath)
search_bar.click()
search_bar.send_keys(search_item)
time.sleep(2)
search_bar.send_keys(Keys.ENTER)
time.sleep(2)
driver.find_element_by_xpath(variable_item_xpath).click()
time.sleep(2)
driver.find_element_by_xpath(download_xpath).click()
time.sleep(2)
driver.find_element_by_xpath(csv_xpath).click()
time.sleep(2)

# click on the search bar
# Type in "delinquency"
# Click on the "link"
# click download
# click csv

































