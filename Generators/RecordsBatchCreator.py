from Services.Logger.Implementation.Logging import Logging


class RecordsBatchCreator:
    def __init__(self, prev_id, prev_curpair, prev_desc, prev_tags):
        self.prev_id = prev_id
        self.prev_curpair = prev_curpair
        self.prev_desc = prev_desc
        self.prev_tags = prev_tags

    def batch_creation(self, start_offset):
        pass

    def __generate_order(self, seed):
        pass

    def __create_record(self, seed, order, status, datetime_margin):
        pass

    def __create_records_for_order(self, seed):
        pass
