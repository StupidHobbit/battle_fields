


class Game:
    def __init__(self):
        pass

    def shutdown(self):
        pass


if __name__ == '__main__':
    import math
    from multiprocessing.dummy import Pool as ThreadPool

    # Make the Pool of workers
    pool = ThreadPool(4)

    # Open the urls in their own threads
    # and return the results
    results = pool.map(math.sqrt, range(100))

    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

    print(results)