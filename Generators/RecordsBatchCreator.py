from Services.Logger.Implementation.Logging import Logging
from Generators.ValueProcessor import ValueProcessor
from Configs.Constants.ConstantCollections import ConstantCollections
from DTOs.Order import Order
from DTOs.Record import Record
from ReportData.ReportData import ReportData
import datetime


class RecordsBatchCreator:
    def __init__(self, config):
        self.config = config
        self.value_creator = ValueProcessor(config)
        self.prev_id = [self.config["FIRST_ID_PART"], self.config["SECOND_ID_PART"],
                        self.config["THIRD_ID_PART"], self.config["FOURTH_ID_PART"]]
        self.prev_curpair = self.config["FIRST_PAIR"]
        self.prev_desc = self.config["FIRST_DESC"]
        self.prev_tags = [self.config["FIRST_TAG"], self.config["SECOND_TAG"],
                          self.config["THIRD_TAG"], self.config["FOURTH_TAG"],
                          self.config["FIFTH_TAG"]]

    def batch_creation(self, start_offset):
        Logging.info("Starting batch generation of orders")
        iterations = self.config["BATCH_SIZE"]
        try:
            all_batch_records = []

            for i in range(start_offset, start_offset + iterations):
                record = self.__create_records_for_order(i)

                all_batch_records.extend(record)

        except MemoryError:
            Logging.error("Ran out of memory! Stopping!")
            exit(self.config["MEMORY_ERROR"])

        return all_batch_records

    def __generate_order(self, seed, zone):
        Logging.info("Generate common fields amongst the records in order")

        self.prev_id = self.value_creator.generate_id(self.prev_id)
        id = self.value_creator.format_id(self.prev_id)

        cur_pair, cur_price, self.prev_curpair = self.value_creator.select_currency_pair(self.prev_curpair)
        direction = self.value_creator.generate_direction(seed)
        init_px = self.value_creator.generate_initial_price(seed, cur_price)
        init_volume = self.value_creator.generate_init_volume(init_px)
        desc, self.prev_desc = self.value_creator.generate_desc(self.prev_desc)
        self.prev_tags = self.value_creator.generate_tags(self.prev_tags)

        tags = self.value_creator.concatenate_tags(self.prev_tags)

        return Order(id, cur_pair, direction, init_px, init_volume, desc, tags, zone, cur_price)

    def __create_record(self, seed, order, status, datetime_margin):
        Logging.info("Form a single record insertion query string")
        date = self.value_creator.generate_timestamp(seed) + datetime_margin
        fill_px, fill_volume = self.value_creator.final_fill_price_and_volume(seed, status, order.get_cur_price(),
                                                                              order.get_volume_in_other_currency())
        return Record(order, status, date, fill_px, fill_volume)

    def __create_records_for_order(self, seed):
        Logging.info("Creating 2-3 records for a given order")
        start_time = datetime.datetime.now()

        zone = self.value_creator.localize_zone(seed)
        order = self.__generate_order(seed, zone)

        try:
            several_records = []
            type_num = self.value_creator.close_status_selection(seed)
            type = ConstantCollections.CLOSED_DEAL_STATUSES_LIST[type_num]
            several_records.append(self.__create_record(seed, order, "ToProvide", 0))

            if zone == 1:
                several_records.append(self.__create_record(seed, order, type, self.config["WAIT_AFTER"]))
                finish_time = datetime.datetime.now()
                ReportData.generated_red.append((finish_time - start_time).total_seconds() * 1000)
            elif zone == 3:
                several_records.append(self.__create_record(seed, order, "New", self.config["WAIT_BEFORE"]))
                finish_time = datetime.datetime.now()
                ReportData.generated_blue.append((finish_time - start_time).total_seconds() * 1000)
            else:
                several_records.append(self.__create_record(seed, order, type, 10))
                several_records.append(self.__create_record(seed, order, "New", -10))
                finish_time = datetime.datetime.now()
                ReportData.generated_green.append((finish_time - start_time).total_seconds() * 1000)
        except MemoryError:
            Logging.error("Ran out of memory! Stopping!")
            exit(self.config["MEMORY_ERROR"])

        return several_records
