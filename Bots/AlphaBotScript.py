""" 
PURPOSE
-------------------
This will be the alpha bot. I want this file to be where we initialize our bot, set any configurations, and most importantly, allow multiple bots to run simultaneosuly. Ideally 
this could hold any major functionalities that's consistent across the different bots I'll run, but that's not the most important feature. I want to be able to use this for any
web task I want to automate and use the specifc task as a plugin for this. 

We've done a lot of the work already so really its just a copy and past procedure right now, but going forward, I can focus on different components without things getting too
messy. Alright lets get it.

Plan of attack
-------------------
1. Initialize AlphaBot
2. Run Specific Task - Each task will be a child of the AlphaBot (SigmaBots) that inherits the functionlity. This will include things like setting the driver's configuration, 
                       reestablishing a lost connection, or any other useful fucntions.
    a. Each task will create their own webdriver instance and run their own configurations/pathing. 
3. Execute additional functionalities (notification system)

Notes
-------------------
* Each task is named appropropriately. For example, getting my ps5 off gamestop could be called "gamestop_ps5". Within the task, I create the task instance, pass in the 
  configuration, and then call the task's run function that executes the crawling operations. 

"""

import SigmaBotGamestopPS5
import email_notification_system

import os
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By


class AlphaBot():

    IMPPLICIT_WAIT_TIME = 10 # driver will execute the next command or wait X amount of seconds

    """ Constructor """
    def __init__(self):

        print("--- AlphaBot Running ---")
        self.task_count = 0

        print("--- NotificationBot Running ---")
        self.notification_bot = email_notification_system.email_bot()

        self.stealth_mode = False
        self.proxy_list = []





    """ 
    Summary
    -------------------
    Runs a bot to get a ps5 from gamestop.

    Inputs
    -------------------
    config_params <dictionary> :: {"specification": value}, indicates which specifications need to be set as well as gives the vale
                                  for that specification.

    Outputs
    -------------------
    Congratulotory statement
    """
    def gamestop_ps5(self, lightweight):
        self.task_count = self.task_count + 1 # keep track of the number of tasks alphabot is running
        local_task_count = self.task_count # need to use locks around this to ensure accuracy        

        task = SigmaBotGamestopPS5.SigmaBotGamestopPS5(alphabot=self) # initialize bot
        print(f"Task {local_task_count} -- {task.name} -- Running")

        config = task.configuration(lightweight=lightweight, stealth=self.stealth_mode) # set the driver configurations

        task.start_driver(config) # start up the driver

        complete = task.run() # run the crawling prcoedure, returns true if everything completes without a problem


        if complete:
            print(f"Task {local_task_count} -- {task.name} -- Complete")
        else:
            print(f" Something went wrong with {task.name}")





    """ Helper Method -- retrieves a random proxy from proxy list and concatentates the IP Address + Port """
    def get_proxy(self):

        # ensure that there are US proxies to use; if not, have to wait for a refresh, so better to just carry on without stealth
        if self.proxy_list:
            index = randint(0,len(self.proxy_list)-1)
            proxy_str = self.proxy_list[index]['IP Address'] + ':' + self.proxy_list[index]['Port']
            return proxy_str
        else:
            return -1





    """ 
    Summary
    -------------------
    Scrapes a website that offers free proxies I can use to rotate IPs. Saves them to alphabot so all the sigmas can use them

    Inputs
    -------------------
    None

    Outputs
    -------------------
    List of dictionaries that have the IP addresses, Ports, etc. for eacch proxy
    """
    def apply_stealth_mode(self):
        print("--- Stealth Mode Running ---")

        # set up driver
        exec_path = os.path.join( os.getcwd(), 'Requirements\geckodriver-v0.29.1-win64\geckodriver.exe' )
        driver = webdriver.Firefox(executable_path=exec_path) 
        driver.get('https://sslproxies.org') # go to site with proxies

        # setting pathing
        table = driver.find_element(By.TAG_NAME, 'table')
        thead = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
        tbody = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        """ Extracting proxies from table on site, converting them to dictionaries """
        headers = []
        for th in thead:
            headers.append(th.text.strip())

        proxies = []
        for tr in tbody:
            proxy_data = {}
            tds = tr.find_elements(By.TAG_NAME, 'td')
            for i in range(len(headers)):
                proxy_data[headers[i]] = tds[i].text.strip()
            proxies.append(proxy_data)

        driver.close() # close the browser

        # only want to use US based proxies
        US_PROXIES = [dictionary for dictionary in proxies if dictionary['Country'] == 'United States']
        self.proxy_list = US_PROXIES
        self.stealth_mode = True

