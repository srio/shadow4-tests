import logging
logging.basicConfig(level=logging.INFO)



class A():
    # pass
    # logging.basicConfig(level=logging.INFO)
    # logging.debug('This message should appear on the console')
    def __init__(self):
        logging.info("A: PRE info\n newline")
        # logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)
        logging.info("A: info\n newline")
        # logging.warning('A: warning')
        # logging.error('A: error')

class B():
    def __init__(self):
        print(">> in B")
        # logging.basicConfig(level=logging.INFO)
        logging.info('B: info')


if __name__ == "__main__":
    pass
    A()
    B()
    # A()
