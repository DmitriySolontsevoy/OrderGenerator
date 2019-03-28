from DTOs import Order


class Record(Order):
    def __init__(self, order, status, datetime, fill_px, fill_volume):
        self.order = order
        self.status = status
        self.datetime = datetime
        self.fill_px = fill_px
        self.fill_volume = fill_volume
