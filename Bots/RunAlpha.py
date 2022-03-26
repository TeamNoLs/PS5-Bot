"""
PURPOSE
-------------------
This file will be used to run the alpha bot. Keeping it very simple at first, but can build this further out later.
"""

import AlphaBotScript
import multiprocessing as mp


if __name__ == '__main__':
    alpha = AlphaBotScript.AlphaBot() # boot up alphabot
    # alpha.apply_stealth_mode()  # use stealth mode
    lightweight = True # limit reources the driver will utilize
    lock = mp.Lock() # used to keep shared resources in order

    # """ Run a single crawler"""
    # alpha.gamestop_ps5(lock=lock, lightweight=lightweight) # start gamestop ps5 crawler



    """ Run multiple crawlers """
    gme_ps5_bots = 2 # number of gamestop ps5 bots i want to run
    target_ps5_bots = 2 # number of target ps5 bots i want to run

    crawlers = {
        "Gamestop-PS5" : alpha.gamestop_ps5,
        "Target-PS5" : alpha.target_ps5
    }

    n_crawlers = gme_ps5_bots + target_ps5_bots # total number of bots running in parallel

    # check to make sure we have the resources to run all the bots
    if n_crawlers >= mp.cpu_count():
        print("Bruh...way too many bots")
    else:

        """ Create a process for each crawler """
        processes = []
        # add in desired number of gme ps5 bots
        for i in range(gme_ps5_bots):
            p = mp.Process(target=crawlers["Gamestop-PS5"], args=[lock,lightweight])
            processes.append(p)
            p.start()
            
        # add in desired number of target ps5 bots
        for i in range(target_ps5_bots):
            p = mp.Process(target=crawlers["Target-PS5"], args=[lock,lightweight])
            processes.append(p)
            p.start()

        for p in processes:
            p.join()