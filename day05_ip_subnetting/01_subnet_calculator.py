
import argparse
import ipaddress
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.netutils import print_table, save_output  


def classful(first_octet: int) -> str:
    if first_octet == 127:
        return "Loopback"
    for limit, name in ((127, "A"), (191, "B"), (223, "C"), (239, "D (multicast)")):
        if first_octet <= limit:
            return name
    return "E (experimental)"


def describe(net: ipaddress.IPv4Network) -> dict:
    prefix = net.prefixlen
    if prefix <= 30:
        usable = net.num_addresses - 2
        first, last = net.network_address + 1, net.broadcast_address - 1
    elif prefix == 31:                       
        usable, first, last = 2, net.network_address, net.broadcast_address
    else:                                    
        usable, first, last = 1, net.network_address, net.network_address
    return {
        "network": str(net.network_address),
        "prefix": f"/{prefix}",
        "netmask": str(net.netmask),
        "wildcard": str(net.hostmask),
        "broadcast": str(net.broadcast_address),
        "first_host": str(first),
        "last_host": str(last),
        "usable_hosts": usable,
        "total_addresses": net.num_addresses,
        "class": classful(int(net.network_address) >> 24),
        "private": net.is_private,
        "binary_mask": ".".join(f"{octet:08b}" for octet in net.netmask.packed),
    }


def main():
    parser = argparse.ArgumentParser(description="IPv4 subnet calculator")
    parser.add_argument("cidr", help="e.g. 192.168.1.77/26 or 10.0.0.0/24")
    parser.add_argument("--split", type=int, metavar="PREFIX",
                        help="split the network into /PREFIX subnets")
    parser.add_argument("--save", action="store_true", help="also save to output/")
    parser.add_argument("-f", "--format", choices=["csv", "json", "yaml"], default="csv")
    args = parser.parse_args()

    try:
        iface = ipaddress.ip_interface(args.cidr)
    except ValueError as exc:
        sys.exit(f"Invalid address: {exc}")
    if iface.version != 4:
        sys.exit("IPv4 only today - IPv6 subnetting comes later in the series.")
    net = iface.network

    info = describe(net) # type: ignore
    print(f"\nInput address : {iface.ip}")
    for key, value in info.items():
        print(f"{key.replace('_', ' ').title():<16}: {value}")

    rows = [info]
    if args.split:
        if not net.prefixlen < args.split <= 32:
            sys.exit(f"--split must be bigger than /{net.prefixlen} and at most /32")
        rows = [describe(sub) for sub in net.subnets(new_prefix=args.split)] # type: ignore
        print(f"\n{net} split into {len(rows)} x /{args.split} subnets:\n")
        print_table(rows, ["network", "prefix", "first_host", "last_host", "broadcast", "usable_hosts"])

    if args.save:
        save_output(rows, args.format, "subnet_calc")


if __name__ == "__main__":
    main()
