from pathlib import Path


def run(h):
    base = "day05_ip_subnetting/"
    out = h.run_script(base + "01_subnet_calculator.py", "192.168.1.77/26")
    h.check("day05 subnet calculator /26", out, "192.168.1.64", "192.168.1.127", "Usable Hosts    : 62")
    out = h.run_script(base + "01_subnet_calculator.py", "10.0.0.0/24", "--split", "26")
    h.check("day05 subnet split", out, "split into 4 x /26", "10.0.0.192")

    out = h.run_script(base + "02_vlsm_planner.py")
    h.check("day05 vlsm planner", out, "192.168.10.0/26", "192.168.10.64/26", "192.168.10.128/27",
            "192.168.10.160/28", "192.168.10.176/30", "192.168.10.180/30", "184/256")

    csv_file = str(h.ROOT / base / "sample_interfaces.csv")
    out = h.run_script(base + "03_ip_overlap_checker.py", "--from-csv", csv_file)
    h.check("day05 overlap checker (offline CSV)", out, "DUPLICATE-IP", "SUBNET-OVERLAP", "10.10.10.3/24")

    out = h.run_script(base + "03_ip_overlap_checker.py", "-d", "R1-EDGE")
    h.check("day05 overlap checker (live/mock)", out, "DUPLICATE-IP", "SUBNET-OVERLAP", "10.1.1.129/25")
