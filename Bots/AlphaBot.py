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

import multiprocessing
import SigmaBotGamestopPS5

import multiprocessing as mp

class AlphaBot():

    IMPPLICIT_WAIT_TIME = 10 # driver will execute the next command or wait X amount of seconds

    """ Constructor """
    def __init__(self):
        print("--- AlphaBot Running ---")
        self.task_count = 0





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
    def gamestop_ps5(self, config_params={}):
        self.task_count = self.task_count + 1
        print(f"Task #{self.task_count} running")
        task = SigmaBotGamestopPS5()
        task.configuration()
        complete = task.run()
        if complete:
            print(f"Task -- {task.name} -- complete")
        else:
            print(f" Something went wrong with {task.name}")

    def test(self, money):
        print(f'Test working {money}')


if __name__ =='__main__':
    n = 2   # number of processes to run
    alpha = AlphaBot()
    print(mp.cpu_count())
    p = mp.Pool(n)
    p.map(alpha.test, [2,3])
    





















