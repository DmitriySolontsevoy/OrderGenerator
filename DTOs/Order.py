class Order:
    def __init__(self, id, cur_pair, direction, init_px, init_volume, desc, tags):
        self.id = id
        self.cur_pair = cur_pair
        self.direction = direction
        self.init_px = init_px
        self.init_volume = init_volume
        self.desc = desc
        self.tags = tags
