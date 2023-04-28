import socket
from urllib.request import urlopen
from json import load
import argparse

from scapy.layers.inet import traceroute


def get_ip_info(ip: str):
    url = f"https://api.incolumitas.com/?q={ip}"
    res = urlopen(url)
    data = load(res)

    result = {
        'ASN': data['asn'].get('asn', 'Unknown'),
        'Country': data['location'].get('country_code', 'Unknown'),
        'Provider': data['asn'].get('descr', 'Unknown')
    }
    return result


def is_ip_address(ip: str):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False


def trace(target):
    if not is_ip_address(target):
        target = socket.gethostbyname(target)

    res, _ = traceroute(target, maxttl=30, verbose=False)
    trace = res.get_trace()[target]
    result_table = []
    for idx, (ip, _) in sorted(list(trace.items()), key=lambda x: x[0]):
        if ip.startswith("10.") or ip.startswith("192.168"):
            continue

        row = {"IP": ip}
        ip_data = get_ip_info(ip)
        row.update(ip_data)
        result_table.append(row)

    return result_table


def print_trace(result_table):
    col_widths = {
        "order": max(
            len("Order"),
            max(len(str(i)) for i in range(len(result_table)))
        ),
        "IP": max(
            len("IP"),
            max(len(row["IP"]) for row in result_table)
        ),
        "ASN": max(
            len("ASN"),
            max(len(str(row["ASN"])) for row in result_table)
        ),
        "Country": max(
            len("Country"),
            max(len(row["Country"]) for row in result_table)
        ),
        "Hostname": max(
            len("Provider"),
            max(len(row["Provider"]) for row in result_table)
        ),
    }

    header = f"| {'Order':<{col_widths['order']}} | {'IP':<{col_widths['IP']}} | {'ASN':<{col_widths['ASN']}} | {'Country':<{col_widths['Country']}} | {'Provider':<{col_widths['Hostname']}}"
    print(header)
    print("-" * len(header))

    for i, row in enumerate(result_table, start=1):
        print(f"| {i:<{col_widths['order']}} | {row['IP']:<{col_widths['IP']}} | {row['ASN']:<{col_widths['ASN']}} | {row['Country']:<{col_widths['Country']}} | {row['Provider']:<{col_widths['Hostname']}}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="", type=str)
    args = parser.parse_args()

    trace_data = trace(args.ip)
    print_trace(trace_data)
