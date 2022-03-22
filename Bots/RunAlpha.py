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

    """ Run a single crawler"""
    alpha.gamestop_ps5(lock=lock, lightweight=lightweight) # start gamestop ps5 crawler



    # """ Run multiple crawlers """
    # n_bots = 2
    # # n_bots = mp.cpu_count() - 1 # use all but 1 processor
    # processes = []
    # lock = mp.Lock()
    # for i in range(n_bots):
    #     p = mp.Process(target=alpha.gamestop_ps5, args=[lock,lightweight])
    #     processes.append(p)
    #     p.start()

    # for p in processes:
    #     p.join()