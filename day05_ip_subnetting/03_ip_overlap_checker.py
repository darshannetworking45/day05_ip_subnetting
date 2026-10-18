
import argparse
import csv
import ipaddress
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.netutils import (add_common_args, get_credentials, load_inventory,  
                             print_table, run_task, save_output, send_parsed)


def collect(conn, dev):
    rows = []
    for intf in send_parsed(conn, "show interfaces"):
        if intf["ip_address"] and intf["prefix_length"]:
            rows.append({"hostname": dev["hostname"], "interface": intf["interface"],
                         "ip_cidr": f"{intf['ip_address']}/{intf['prefix_length']}"})
    return rows


def find_conflicts(entries):
    parsed = [(e, ipaddress.ip_interface(e["ip_cidr"])) for e in entries]
    conflicts = []
    for (a, ia), (b, ib) in itertools.combinations(parsed, 2):
        if ia.ip == ib.ip:
            kind = "DUPLICATE-IP"
        elif ia.network != ib.network and ia.network.overlaps(ib.network):
            kind = "SUBNET-OVERLAP"
        elif ia.network == ib.network and a["hostname"] == b["hostname"]:
            kind = "SAME-SUBNET-ON-ONE-DEVICE"
        else:
            continue
        conflicts.append({
            "finding": kind,
            "a_device": a["hostname"], "a_interface": a["interface"], "a_ip": str(ia),
            "b_device": b["hostname"], "b_interface": b["interface"], "b_ip": str(ib),
        })
    return conflicts


def main():
    parser = argparse.ArgumentParser(description="IP overlap / duplicate checker")
    add_common_args(parser)
    parser.add_argument("--from-csv", metavar="FILE", help="offline mode (no SSH)")
    args = parser.parse_args()

    if args.from_csv:
        with open(args.from_csv, newline="") as fh:
            entries = list(csv.DictReader(fh))
    else:
        devices = load_inventory(args.inventory, args.device)
        entries, _errors = run_task(devices, get_credentials(), collect)

    print(f"\nChecking {len(entries)} interface addresses...\n")
    conflicts = find_conflicts(entries)
    if conflicts:
        print_table(conflicts, ["finding", "a_device", "a_interface", "a_ip",
                                "b_device", "b_interface", "b_ip"])
        save_output(conflicts, args.format, "ip_conflicts")
    else:
        print("No duplicate IPs or overlapping subnets found.")


if __name__ == "__main__":
    main()
