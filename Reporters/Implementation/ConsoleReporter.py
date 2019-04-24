from Reporters.API.Reporter import Reporter
from Services.Logger.Implementation.Logging import Logging
from ReportData.ReportData import ReportData


class ConsoleReporter(Reporter):
    def __init__(self, db_service):
        self.db_service = db_service

    def report(self):
        Logging.info("Started console reporting")
        self.__report_list(ReportData.generated_red, "Red zone generation")
        self.__report_list(ReportData.generated_green, "Green zone generation")
        self.__report_list(ReportData.generated_blue, "Blue zone generation")

        self.__report_list(ReportData.messaged_red, "Red zone RMQ messaging")
        self.__report_list(ReportData.messaged_green, "Green zone RMQ messaging")
        self.__report_list(ReportData.messaged_blue, "Blue zone RMQ messaging")

        self.__report_single_metric(ReportData.received_from_rabbit, "Amount of messages received from RMQ")

        result = self.db_service.select("""SELECT count(*) FROM mytable UNION
            SELECT count(DISTINCT id) FROM mytable UNION
            SELECT count(*) FROM (SELECT * FROM mytable GROUP BY id HAVING count(*) = 2 AND status = 2) AS T UNION
            SELECT count(*) FROM (SELECT count(*) FROM mytable GROUP BY id HAVING count(*) = 3) AS T UNION
            SELECT count(*) FROM (SELECT * FROM mytable GROUP BY id HAVING count(*) = 2 AND status = 1) AS T;""")
        if result:
            self.__report_single_metric(int(result[0][0]), "Amount of records in the database")
            self.__report_single_metric(result[1][0], "Amount of orders in the database")
            self.__report_single_metric(result[2][0], "Orders in red zone")
            self.__report_single_metric(result[3][0], "Orders in green zone")
            self.__report_single_metric(result[4][0], "Orders in blue zone")

    def __report_list(self, list, flavor_text):
        if len(list) > 0:
            amount = len(list)
            minimum = min(list)
            maximum = max(list)
            average = sum(list)/amount
            print("{} (amount = {}):\nMin: {} ms\nMax: {} ms\nAvg: {} ms\n".format(flavor_text, amount, minimum,
                                                                                   maximum, average))

    def __report_single_metric(self, metric, flavor_text):
        print("{}: {}\n".format(flavor_text, metric))
