class Order:
    def __init__(self, id, cur_pair, direction, init_px, init_volume, desc, tags):
        self.__id = id
        self.__cur_pair = cur_pair
        self.__direction = direction
        self.__init_px = init_px
        self.__init_volume = init_volume
        self.__desc = desc
        self.__tags = tags
