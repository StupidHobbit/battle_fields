from multiprocessing.dummy import Pool


class Game:
    def __init__(self):
        self.pool = Pool(5)

    def update_units(self):
        pass

    def shutdown(self):
        pass


if __name__ == '__main__':
    pass