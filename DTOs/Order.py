class Order:
    def __init__(self, id, cur_pair, direction, init_px, init_volume, desc, tags, zone, cur_price):
        self.__id = id
        self.__cur_pair = cur_pair
        self.__direction = direction
        self.__init_px = init_px
        self.__init_volume = init_volume
        self.__desc = desc
        self.__tags = tags
        self.__zone = zone
        self.__cur_price = cur_price

    def get_id(self):
        return self.__id

    def get_cur_pair(self):
        return self.__cur_pair

    def get_direction(self):
        return self.__direction

    def get_init_px(self):
        return self.__init_px

    def get_init_volume(self):
        return self.__init_volume

    def get_desc(self):
        return self.__desc

    def get_tags(self):
        return self.__tags

    def get_zone(self):
        return self.__zone

    def get_cur_price(self):
        return self.__cur_price

    def get_volume_in_other_currency(self):
        return self.__init_volume / self.__init_px

    def __str__(self):
        return "{}|{}|{}|{}|{}|{}|{}|{}|{}|".format(self.__id, self.__cur_pair, self.__direction, self.__init_px,
                                                    self.__init_volume, self.__desc, self.__tags, self.__zone,
                                                    self.__cur_price)
