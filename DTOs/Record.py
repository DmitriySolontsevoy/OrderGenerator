from DTOs import Order


class Record(Order):
    def __init__(self, id, cur_pair, direction, init_px, init_volume, desc, tags, status, datetime, fill_px, fill_volume):
        super().__init__(id, cur_pair, direction, init_px, init_volume, desc, tags)
        self.status = status
        self.datetime = datetime
        self.fill_px = fill_px
        self.fill_volume = fill_volume
