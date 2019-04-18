from Services.Logger.Implementation.Logging import Logging
from scipy.stats import norm
from Generators.Generators import Generators
from Configs.Constants.ConstantCollections import ConstantCollections
import math


class ValueProcessor:
    def __init__(self, config):
        self.config = config

    # Generate the ID in 4 pieces using the
    # linear congruent method
    def generate_id(self, prev, number):
        Logging.info("Generating ID")
        multiplier = self.config["ID_MULT"]
        offset = self.config["ID_OFFSET"] + number
        divisor = self.config["ID_DIV"]

        part_one = Generators.linear_congruent_generate(prev[0], multiplier, offset, divisor) + 1000
        part_two = Generators.linear_congruent_generate(prev[1], multiplier, offset, divisor) + 1000
        part_three = Generators.linear_congruent_generate(prev[2], multiplier, offset, divisor) + 1000
        part_four = Generators.linear_congruent_generate(prev[3], multiplier, offset, divisor) + 1000

        try:
            new_prev = [part_one, part_two, part_three, part_four]
        except MemoryError:
            Logging.error("Ran out of memory! Stopping!")
            exit(self.config["MEMORY_ERROR"])

        return new_prev

    def format_id(self, prev):
        return str(prev[0]) + str(prev[1]) + str(prev[2]) + str(prev[3])

    # Generate temporary volumes that are used in both
    # initial volume and fill volume creation
    def generate_init_volume(self, number):
        Logging.info("Generating temporary volume value")
        value = Generators.absolute_cosine_generate(number) * 100
        return round(value, self.config["PLACES_FOR_VOLUME"])

    # Generate a direction for an order
    def generate_direction(self, number):
        Logging.info("Selecting direction")
        return round(Generators.absolute_sine_generate(number))

    # Generate tags list for an order
    def generate_tags(self, prev):
        Logging.info("Generating tag list")
        multiplier = self.config["TAGS_MULT"]
        offset = self.config["TAGS_OFFSET"]
        divisor = self.config["TAGS_DIV"]

        tag_num_one = Generators.linear_congruent_generate(prev[0], multiplier, offset, divisor)
        tag_num_two = Generators.linear_congruent_generate(prev[1], multiplier, offset, divisor)
        tag_num_three = Generators.linear_congruent_generate(prev[2], multiplier, offset, divisor)
        tag_num_four = Generators.linear_congruent_generate(prev[3], multiplier, offset, divisor)
        tag_num_five = Generators.linear_congruent_generate(prev[4], multiplier, offset, divisor)

        try:
            new_prev = [tag_num_one, tag_num_two, tag_num_three, tag_num_four, tag_num_five]
        except MemoryError:
            Logging.error("Ran out of memory! Stopping!")
            exit(self.config["MEMORY_ERROR"])

        return new_prev

    # Collect tags into a single string
    def concatenate_tags(self, prev):
        Logging.info("Creating a unified tag string")
        tags_list = ""

        length = len(ConstantCollections.TAGS_LIST)

        if prev[0] is not None and prev[0] < length:
            tags_list += ConstantCollections.TAGS_LIST[prev[0]]
        if prev[1] is not None and prev[1] < length:
            tags_list += " " + ConstantCollections.TAGS_LIST[prev[1]]
        if prev[2] is not None and prev[2] < length:
            tags_list += " " + ConstantCollections.TAGS_LIST[prev[2]]
        if prev[3] is not None and prev[3] < length:
            tags_list += " " + ConstantCollections.TAGS_LIST[prev[3]]
        if prev[4] is not None and prev[4] < length:
            tags_list += " " + ConstantCollections.TAGS_LIST[prev[4]]

        return tags_list.strip()

    # Pseudorandomly select a currency pair
    def select_currency_pair(self, prev):
        Logging.info("Selecting currency pair")
        pair = Generators.linear_congruent_generate(prev, self.config["CURPAIR_MULT"], self.config["CURPAIR_OFFSET"],
                                                    self.config["CURPAIR_DIV"])
        price = ConstantCollections.CURRENCY_PAIR_PRICES_LIST[pair]
        return price, pair

    # Fluctuating initial price by a given margin
    def generate_initial_price(self, number, price):
        Logging.info("Generating initial pair price")
        margin = self.config["INIT_MARGIN"]
        dir = self.config["INIT_LESS"]

        if number % 2 == 1:
            dir = self.config["INIT_MORE"]

        value = norm.ppf(dir, price, price * margin)
        return round(value, self.config["PLACES_FOR_PRICE"])

    # Assign an order to a specific zone
    def localize_zone(self, number):
        Logging.info("Figuring out the zone of order")
        total_to_generate = self.config["BATCH_SIZE"] * self.config["BATCHES_AMOUNT"]
        partition = number/total_to_generate
        num = 3

        if partition < self.config["RED"]:
            num = 1
        elif self.config["RED"] < partition < self.config["RED"] + self.config["GREEN"]:
            num = 2

        return num

    # Fluctuating fill price by a 5% margin
    # It is temporary, since it can be nullified
    def generate_temporary_fill_price(self, number, price):
        Logging.info("Generating temporary fill pair price")
        margin = self.config["FILL_MARGIN"]
        dir = self.config["FILL_LESS"]

        if number % 2 == 0:
            dir = self.config["FILL_MORE"]

        value = norm.ppf(dir, price, price * margin)
        return round(value, self.config["PLACES_FOR_PRICE"])

    # Form a 3-character description
    def generate_desc(self, prev):
        Logging.info("Generating description")
        return Generators.linear_congruent_generate(prev, self.config["DESC_MULT"], self.config["DESC_OFFSET"],
                                                    self.config["DESC_DIV"])

    # Select deal closing status
    def close_status_selection(self, number):
        Logging.info("Selecting type of deal closing")
        return math.floor(Generators.exponent_sine_generate(number)) + 3

    # Generate final fill price
    def final_fill_price_and_volume(self, number, status, price, volume):
        Logging.info("Generate both fill price and volume")
        if status < 4:
            pair_price_volume = (0, 0)
        else:
            fill_price = self.generate_temporary_fill_price(number, price)
            coeff = 1
            if status == 4:
                coeff = 0.5
            fill_volume = round(volume * fill_price * coeff, self.config["PLACES_FOR_VOLUME"])
            pair_price_volume = (fill_price, fill_volume)

        return pair_price_volume

    # Generate datetime in UNIX timestamp fashion
    # adding milliseconds
    def generate_timestamp(self, number):
        Logging.info("Generating timestamp")
        value = Generators.absolute_sine_generate(number) * 100000
        return round(value) + self.config["BEGINNING_OF_TIME"]
