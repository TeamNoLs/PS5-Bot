# I'm using this to test out some mutlithreading real quick. I'll eventually get the notification stuff running as well

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



# import smtplib, ssl

# password = "Infussy1@1"
# email = 'whatisthebestway27@gmail.com'
# port = 465  # For SSL
# smtp_server = "smtp.gmail.com"
# sender_email = 'whatisthebestway27@gmail.com'  # Enter your address
# receiver_email = "taj8zg@virginia.edu"  # Enter receiver address
# password = "Infussy1@1"
# message = """\
# PS5 yuhhhhhhhhhhh.

# Happy Christmas

# This message is sent from Python(dork)."""

# context = ssl.create_default_context()
# with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)