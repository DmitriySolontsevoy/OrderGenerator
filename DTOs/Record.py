class Record:
    def __init__(self, order, status, datetime, fill_px, fill_volume):
        self.order = order
        self.__status = status
        self.__datetime = datetime
        self.__fill_px = fill_px
        self.__fill_volume = fill_volume

    def get_status(self):
        return self.__status

    def get_datetime(self):
        return self.__datetime

    def get_fill_px(self):
        return self.__fill_px

    def get_fill_volume(self):
        return self.__fill_volume

    def __str__(self):
        return self.order.__str__() + "{}|{}|{}|{}|".format(self.__status, self.__datetime,
                                                            self.__fill_px, self.__fill_volume)
