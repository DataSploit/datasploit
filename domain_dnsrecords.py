import sys
import dns.resolver
from termcolor import colored

from os_int_service import OsIntService

NO_RECORDS_FOUND = "No Records Found"


class DNS(OsIntService):
    def _perform_query(self):
        def fetch_dns_records(rec_type):
            try:
                return dns.resolver.query(self.domain, rec_type)
            except dns.resolver.NoAnswer:
                return NO_RECORDS_FOUND

        return {'SOA Records': fetch_dns_records("SOA"),
                'MX Records': fetch_dns_records("MX"),
                'TXT Records': fetch_dns_records("TXT"),
                'A Records': fetch_dns_records("A"),
                'Name Server Records': fetch_dns_records("NS"),
                'CNAME Records': fetch_dns_records("CNAME"),
                'AAAA Records': fetch_dns_records("AAAA")}

    def _formatted_data(self):
        def format_one_record(record):
            if NO_RECORDS_FOUND == record:
                return colored(NO_RECORDS_FOUND, 'red')
            else:
                return "".join([str(thing) for thing in record])

        formatted = ""
        for record_type in self.raw_data.keys():
            formatted += "%s\n\t%s\n" % (record_type, format_one_record(self.raw_data[record_type]))

        return formatted


def main():
    domain = sys.argv[1]
    w = DNS(domain)
    w.retrieve()


if __name__ == "__main__":
    main()
