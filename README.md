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

I use a run file that initilaizes the AlphaBot and calls all subsequent commands to work the bot.... I'll pick this back up tomorrow

## Documentation
Overviews on all the major folders/files

### Bots - Folder
This folder contatins all of the scripts used to run the bot. Any additional bots should be added to this folder

### Requirements - Folder
This folder holds all of the required files to run the bots. Really just the webdriver files that and executables needed to access specific web browser. Any additional web browsers that want to be used should be added to this folder. I will add in a file the lists out all the dependencies/versions I'm using.

### AlphaBotScript - Bots/script
Note: Move notification system call from sigmabots to AlphaBot. This will avoid overlapping calls from multiple bots (very unlikely but ya know). 