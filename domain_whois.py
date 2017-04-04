import sys

import whois

from os_int_service import OsIntService


class Whois(OsIntService):
    def _perform_query(self):
        return whois.whois(self.domain)

    def _formatted_data(self):
        return str(self.raw_data)


def main():
    domain = sys.argv[1]
    w = Whois(domain)
    w.retrieve()


if __name__ == "__main__":
    main()
