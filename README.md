# PS5 Bot

## Introduction 
I'm just a kid who decided one day that I wanted a ps5. So I built something to help me get it. And it worked. Now I'm cleaning up my scripts and changing the organizational structure of my code to make this a much more usable application. Not just for others, but also for myself as a template for running other web-automation projects. Also this was frickin cool and I want people to think I'm smart.

## Overview
This project involved me building a number of bots, using selenium web driver, to automate the purchase of a ps5 from a number of different retail websites. The goal was to create programs that could monitor different websites (ideally mutliple websites at once) and follow through with the checkout process once a ps5 became available. 

The process was simple. The webdriver would boot up and go to the retailers website (depending on the security of the website, sometimes you can jump straight to the product page without issue). The driver would then navigate to the product page and check the availability of the product. Most likely it wouldn't be available, in that case it would constantly refresh the page (at some contained random interval of time) until the product becomes available (up to to a certain amount of time before closing the browser and restarting the process). Once the product was found to be available, the driver would continue forward with the checkout process and order the ps5. Different sites have different paths to the "final checkout" so pathing is very dynamic. 

The core process is pretty simple, but there are a number of bells and whistles that needed to be attached to the program to create an effective bot. Parallel processing to allow for numerous bots to be deployed at the same time (locally, I'm not paying for a server), "Stealth Procedures" to help avoid bot detection on the websites, and even a complimentary notification system that signals the user when a ps5 came in stock.

Looking back, there are a number of things that I would do differently/improve upon from my v1 methods, but I don't plan on spending too much time adding any new functionalities. The final version uploaded to this repo will be a polished version of my bread and butter code. It will be effective, but won't be in state that can simply be pulled and ran (if I'm not lazy I'll set up a venv). This isn't simply becasue I'm a lazy kid, but automated web tools tend to become deprecated over time. The pathing I wrote for half the bots are already broken due to some overzealous web developers over at Best Buy, Walmart, and Amazon. So everything I have on here should be pretty easy to build off but no promises that it will run smoothly whenever you come across this.

### Project Structure
I restructured my initial implementation to utilize a more of a template format to allow me to house multiple bots with unique functionalities that take advantage of the same resources (while also saving me time coding). 

I start off creating an AlphBot. This can be thought of in a hierarchy where this is the "bot" in charge (not actually a web driver but who cares it sounds cool). The lesser bots are SigmaBots. These are the bots that actually act was webcrawlers to execute specific tasks. 

The AlphaBot has a two main responsibilities: it can call and run any and all SigmaBots (in paralllel if specified) and it executes the primary stealth procedure used to avoid detection. Additionally it serves as a very nice template for housing all of the SigmaBot run procedures. Using this format makes parallel processing much simpler as well as keeping track of notification system and stealth ops.

The SigmaBot is the main character here. These are the actual web crawlers that boot up the wbsites and execute the crawl path. They utilize a number of different techniques but it really boils down to starting up the driver (with the specified configurations), finding/assigning each of the xpath/css objects specified (depends on the website, I know it shouldn't but css wasn't working at times), and completing the path. 

There is only one AlphaBot, but there can be an infinite number of SigmaBots. The run process starts by initializing the AlphaBot. This also starts up the notification bot (sends an email to the user when a ps5 is located). From there, a number of different configurations can be set that impact the SigmaBots' profile. Once these settings are in place, the SigmaBot (representing what specific task needs to be accomplished) is called as a method of the AlphaBot. This is where the user is able to enable the "parallel crawler" functionality which allows X number of bots to run in parallel on the local CPU's avaialable.


## Documentation
Overviews on all the major folders/files

### Bots - Folder
This folder contatins all of the scripts used to run the bot. Any additional bots should be added to this folder

### Requirements - Folder
This folder holds all of the required files to run the bots. Really just the webdriver files that and executables needed to access specific web browser. Any additional web browsers that want to be used should be added to this folder. I will add in a file the lists out all the dependencies/versions I'm using.

### AlphaBotScript - Bots/script
Note: Move notification system call from sigmabots to AlphaBot. This will avoid overlapping calls from multiple bots (very unlikely but ya know).

This file holds the AlphaBot class, the core class for running this project. There 3 core components to the AlphaBot class: the constructor intiates all attributes and notification system, each of the SigmaBots are run from a method in the AlphaBot class, and the the stealth operations are intialized and set up.

1. I'm not going to run through every attribute of the constructor since its commented/named pretty well, but the major callouts here are the instantiation of the email_notification_system() (notification bot) and reading in the Secrets file that holds all of the personal information (credit card info, shipping info, login credentials, etc.). The motification bot accesses a custom built class that allows the AlphaBot to use a remote email server to send a message to the user's email notifying them that a ps5 has become available. One thing to note about the secrets file is that only the template to the secrets file has been uploaded to the repo, so to be run the bot, the parts you want to use need to be filled out (and the secrets_template.json file needs to be renamed to secrets.json).


2. The next component are the SigmaBot methods. There's no real naming convention (maybe there should be?), but each of these methods contains the run procedure for each of the SigmaBots I've created. The logic is very similar for each SigmaBot: the class for the SigmaBot is intialized, the configurations are set, the driver is booted up, and then the crawl begins. Once the task is completed, it shuts down the driver.

3. The final component is the set up for "stealth procedures". I've said stealth like 20 times already without explaining what's actually happening so here it is. I'm essentialy scraping a website (yep another web crawler) that has a bunch of free proxies that people can utilize to rotate theiir IP address so their identity is hidden (kinda) from outsiders. My function here scrapes the website for a list of proxies, filters them down to only the US based ones, and then passes them to each SigmaBot that is running. 

Note: There are other "stealth procedures" I utilize through the behaviour of the bots (mimicing human type, wait times, etc.), but this is a major component. Other protocols like using a headless browser, a VPN, etc. have been used but I'm keeping this implementation simple for now. Later versions may include this depending on how beefy the systems I'm dealing with.

### RunAlpha - Bots/script
This is the run file for the project. Any specifc configurations for the bots can be set here. Run this file and make sure everything's in the right place and your good to go.

### SigmaBotGamestopPS5 - Bots/script
The first SigmaBot. The sigmaBot files are where the bulk of the code/functionality for these bots will live. There are essentially 3 components to each of these files: driver configuration, pathing, and additional helper methods.

1. The driver configuration portion is where the setttings for the web driver are put in place before starting it. This controls important features that relate to what resources the web driver will have access to while running, the browser we choose to use, and applying the stealth attributes. Once these configurations are set, the driver is ready to be booted up.

2. The pathing is the largest and most dynamic piece to this whole project. This is where the literal path taken to get from point A to point B is executed. Depending on the website, the path taken will differ in length and complexity (dealing with pop ups, filling out forms, avoding honeypot traps, avoiding detection, etc.)

3. The helper methods are really here to assist in the pathing procedure. Some of the tasks in the pathing portion need to be handled in a more complicated way than expected. For example, filling out a form. I created a function that mimics human typing rather than just pasting in the letters. These helper methods allow consistent execution across multiple objects as well as saving me a ton of time.

### SigmaBotTargetPS5 - Bots/script
Similar set up to SigmaBotGamestopPS5. Code is a bit older. Might revamp.

### email_notification_system - Bots/script
This file holds the code for sending the user an email to notify them (of whatever they want). It connects to a remote server that (hosted online for free) that allows an email to be sent from a dummy email (I created one) to the user's email. 

Note: The email most definitley will be sent to your spam folder the first time, so try to unmark it as spam when you first get it.


## Troubleshooting
I'm writing this section mostly for myself so I can log my progress and track any issues. 

* After getting the parallel crawlers up and running, I'm having trouble with the shared resources when I display what task is running. I included locks, but were still having an issue. Minor issue that can be diagnosed later

* Need to test out Target bot stealth features. They had the toughest security measures in the past.
