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
    def convert_rec_to_sql_query(record):
        return "INSERT INTO mytable VALUES({},'{}','{}','{}',{},{},{},{},{},'{}','{}');"\
            .format(record.order.get_id(), record.order.get_cur_pair(), record.order.get_direction(),
                    record.get_status(), record.get_datetime(), record.order.get_init_px(),
                    record.order.get_init_volume(), record.get_fill_px(), record.get_fill_volume(),
                    record.order.get_desc(), record.order.get_tags())
