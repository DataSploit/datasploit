import time
from abc import abstractmethod

from termcolor import colored


class OsIntService(object):
    BOLD = '\033[1m'
    END = '\033[0m'

    def __init__(self, domain):
        self.raw_data = None
        self.domain = domain

    def retrieve(self):
        print self.header('Finding %s Information.' % type(self).__name__)
        self.raw_data = self._perform_query()
        print self.generate_formatted_report()

        return self.raw_data

    def generate_formatted_report(self):
        report = self._formatted_data() or ""
        report += self._query_footer()

        return report

    def print_formatted_report(self):
        print self.generate_formatted_report()
        time.sleep(.3)

    def header(self, message):
        return colored(OsIntService.BOLD + '---> ' + message + OsIntService.END, 'blue')

    def _query_footer(self):
        return colored(OsIntService.BOLD + "\n-----------------------------\n" + OsIntService.END, 'blue')

    @abstractmethod
    def _perform_query(self):
        pass

    @abstractmethod
    def _formatted_data(self):
        pass
