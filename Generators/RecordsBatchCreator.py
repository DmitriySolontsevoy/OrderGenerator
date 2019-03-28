from Services.Logger.Implementation.Logging import Logging
from Generators.ValueProcessor import ValueProcessor
from Configs.Constants.ConstantCollections import ConstantCollections
from DTOs.Order import Order
from DTOs.Record import Record


class RecordsBatchCreator:
    def __init__(self, prev_id, prev_curpair, prev_desc, prev_tags, config):
        self.prev_id = prev_id
        self.prev_curpair = prev_curpair
        self.prev_desc = prev_desc
        self.prev_tags = prev_tags
        self.config = config
        self.value_creator = ValueProcessor(config)

    def batch_creation(self, start_offset):
        Logging.text_file_logger.info("Starting batch generation of orders")
        iterations = self.config.BATCH_SIZE
        try:
            all_batch_records = []

            for i in range(start_offset, start_offset + iterations):
                record = self.__create_records_for_order(i)

                self.prev_id = record.new_prev_id
                self.prev_curpair = record.new_prev_curpair
                self.prev_desc = record.new_prev_desc
                self.prev_tags = record.new_prev_tags

                all_batch_records.extend(record)
        except MemoryError:
            Logging.text_file_logger.error("Ran out of memory! Stopping!")
            exit(self.config.MEMORY_ERROR)

        return all_batch_records

    def __generate_order(self, seed):
        Logging.text_file_logger.info("Generate common fields amongst the records in order")
        temp_volume = self.value_creator.generate_temporary_volumes(seed)

        id, new_prev_id = self.value_creator.generate_id(self.prev_id)
        cur_pair, cur_price, new_prev_curpair = self.value_creator.select_currency_pair(self.prev_curpair)
        direction = self.value_creator.generate_direction(seed)
        init_px = self.value_creator.generate_initial_price(seed, cur_price)
        init_volume = self.value_creator.calculate_volume(init_px, temp_volume)
        desc, new_prev_desc = self.value_creator.generate_desc(self.prev_desc)
        tags, new_prev_tags = self.value_creator.generate_tags(self.prev_tags)

        return Order(id, cur_pair, direction, init_px, init_volume, desc, tags)

    def __create_record(self, seed, order, status, datetime_margin):
        Logging.text_file_logger.info("Form a single record insertion query string")
        date = self.value_creator.generate_timestamp(seed) + datetime_margin
        fill_px, fill_volume = self.value_creator.final_fill_price_and_volume(seed, order.cur_price, order.temp_volume)

        return Record(order, status, date, fill_px, fill_volume)

    def __create_records_for_order(self, seed):
        Logging.text_file_logger.info("Creating 2-3 records for a given order")
        zone = self.value_creator.localize_zone(seed)

        order = self.__generate_order(seed)

        try:
            several_records = []

            several_records.append(self.__create_record(seed, order, "ToProvide", 0))
            if zone == 1:
                type_num = self.value_creator.close_status_selection(seed)
                type = ConstantCollections.CLOSED_DEAL_STATUSES_LIST[type_num]
                several_records.append(
                    self.__create_record(seed, order, type, self.config.WAIT_AFTER))
            elif zone == 3:
                several_records.append(
                    self.__create_record(seed, order, "New", self.config.WAIT_BEFORE))
            else:
                type_num = self.value_creator.close_status_selection(seed)
                type = ConstantCollections.CLOSED_DEAL_STATUSES_LIST[type_num]
                several_records.append(
                    self.__create_record(seed, order, type, 10))
                several_records.append(
                    self.__create_record(seed, order, "New", -10))
        except MemoryError:
            Logging.text_file_logger.error("Ran out of memory! Stopping!")
            exit(self.config.MEMORY_ERROR)

        return several_records
