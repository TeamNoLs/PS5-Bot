"""
PURPOSE
-------------------
This file will be used to run the alpha bot. Keeping it very simple at first, but can build this further out later.
"""

import AlphaBotScript
import multiprocessing as mp


if __name__ == '__main__':
    alpha = AlphaBotScript.AlphaBot()
    alpha.apply_stealth_mode()
    lightweight = True
    # alpha.gamestop_ps5(config_params=config)



    """ Run multiple crawlers """
    # n = 2   # number of processes to run
    # # print(mp.cpu_count())
    # p = mp.Pool(n)
    # p.map(alpha.gamestop_ps5, (lightweight,))

    # n_bots = 2
    # processes = []
    # for i in range(n_bots):
    #     p = mp.Process(target=alpha.gamestop_ps5, args=config)
    #     processes.append(p)
    #     p.start()

    # for p in processes:
    #     p.join()