
# this will be the main driver file I use to run any of the bots

from selenium import webdriver
import threading
import time

# this funtion encapsulates initiating the bot object and the calling the run method.
def test_logic():
    driver = webdriver.Firefox()
    url = 'https://www.google.com'
    driver.get(url)
    # bot functionality goes here

    driver.quit()

# main 
N = 5 # number of bots
thread_list = []

# run threads
for i in range(N):
    t = threading.Thread(name='Bot #{}'.format(i))
    t.start()
    time.sleep(1)
    print('Bot # {}'.format(i))
    thread_list.append(t)

    # not sure why we have to join each thread. Vaguely familiar, but idk
    for thread in thread_list:
        thread.join()

    print('done')


