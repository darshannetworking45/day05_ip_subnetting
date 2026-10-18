
import argparse
import ipaddress
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common.netutils import print_table, save_output  


def host_bits_for(hosts: int) -> int:
    return max(2, (hosts + 1).bit_length())


def plan(base: ipaddress.IPv4Network, requirements: list) -> tuple[list, int]:
    start, end = int(base.network_address), int(base.broadcast_address) + 1
    cursor = start
    rows = []
    for req in sorted(requirements, key=lambda r: r["hosts"], reverse=True):
        bits = host_bits_for(req["hosts"])
        size = 1 << bits
        cursor = start + -(-(cursor - start) // size) * size      
        if cursor + size > end:
            sys.exit(f"'{req['name']}' needs a /{32 - bits} but {base} is out of space.")
        net = ipaddress.IPv4Network((cursor, 32 - bits))
        usable = size - 2
        rows.append({
            "name": req["name"],
            "hosts_needed": req["hosts"],
            "subnet": str(net),
            "netmask": str(net.netmask),
            "gateway_suggestion": str(net.network_address + 1),
            "first_host": str(net.network_address + 1),
            "last_host": str(net.broadcast_address - 1),
            "broadcast": str(net.broadcast_address),
            "usable_hosts": usable,
            "spare": usable - req["hosts"],
        })
        cursor += size
    return rows, end - cursor


def main():
    parser = argparse.ArgumentParser(description="VLSM planner")
    parser.add_argument("-r", "--requirements",
                        default=str(Path(__file__).with_name("vlsm_requirements.yaml")))
    parser.add_argument("-f", "--format", choices=["csv", "json", "yaml"], default="csv")
    args = parser.parse_args()

    data = yaml.safe_load(Path(args.requirements).read_text())
    base = ipaddress.ip_network(data["base_network"], strict=True)
    requirements = data["requirements"]
    names = [r["name"] for r in requirements]
    if len(names) != len(set(names)):
        sys.exit("Duplicate subnet names in the YAML file.")
    if any(int(r["hosts"]) < 1 for r in requirements):
        sys.exit("'hosts' must be 1 or more.")

    rows, free = plan(base, requirements) # type: ignore
    print(f"\nVLSM plan for {base}:\n")
    print_table(rows, ["name", "hosts_needed", "subnet", "netmask", "usable_hosts", "spare"])
    used = base.num_addresses - free
    print(f"\nAddresses used: {used}/{base.num_addresses} ({used / base.num_addresses:.0%}); "
          f"free: {free}")
    save_output(rows, args.format, "vlsm_plan")


if __name__ == "__main__":
    main()
