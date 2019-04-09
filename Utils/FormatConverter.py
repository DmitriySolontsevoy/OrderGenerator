from Proto.OrderRecord_pb2 import OrderRecord
from DTOs.Record import Record
from DTOs.Order import Order


class FormatConverter:
    @staticmethod
    def convert_rec_to_txt(record):
        return record.__str__()

    @staticmethod
    def convert_txt_to_rec(str):
        pieces = str.split("|")
        order = Order(pieces[0], pieces[1], pieces[2], pieces[3], pieces[4], pieces[5], pieces[6], pieces[7], pieces[8])
        record = Record(order, pieces[9], pieces[10], pieces[11], pieces[12])
        return record

    @staticmethod
    def convert_proto_to_rec(proto):
        order = Order(proto.id, proto.currency_pair, proto.direction, proto.init_px, proto.init_volume, proto.desc,
                      proto.tags, proto.zone, proto.currency_price)
        record = Record(order, proto.status, proto.datetime, proto.fill_px, proto.fill_volume)
        return record

    @staticmethod
    def convert_rec_to_proto(record):
        proto = OrderRecord()
        proto.id = record.order.get_id()
        proto.currency_pair = record.order.get_cur_pair()
        proto.direction = record.order.get_direction()
        proto.status = record.get_status()
        proto.datetime = record.get_datetime()
        proto.init_px = record.order.get_init_px()
        proto.init_volume = record.order.get_init_volume()
        proto.fill_px = record.get_fill_px()
        proto.fill_volume = record.get_fill_volume()
        proto.desc = record.order.get_desc()
        proto.tags = record.order.get_tags()
        proto.zone = record.order.get_zone()
        proto.currency_price = record.order.get_cur_price()
        return proto

    @staticmethod
    def convert_rec_to_sql_query(record):
        return "INSERT INTO mytable VALUES('{}',{},{},{},{},{},{},{},{},'{}','{}',{});"\
            .format(record.order.get_id(), record.order.get_cur_pair(), record.order.get_direction(),
                    record.get_status(), record.get_datetime(), record.order.get_init_px(),
                    record.order.get_init_volume(), record.get_fill_px(), record.get_fill_volume(),
                    record.order.get_desc(), record.order.get_tags(), record.order.get_zone())
