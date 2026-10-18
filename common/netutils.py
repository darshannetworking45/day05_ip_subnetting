from __future__ import annotations

import csv
import json
import os
from datetime import datetime
from getpass import getpass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"
DEFAULT_INVENTORY = ROOT / "inventory" / "devices.csv"





def load_inventory(path=DEFAULT_INVENTORY, only=None):
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        with path.open(newline="") as fh:
            devices = list(csv.DictReader(fh))
    elif suffix == ".json":
        data = json.loads(path.read_text())
        devices = data["devices"] if isinstance(data, dict) else data
    elif suffix in (".yaml", ".yml"):
        data = yaml.safe_load(path.read_text())
        devices = data["devices"] if isinstance(data, dict) else data
    else:
        raise ValueError(f"Unsupported inventory format: {suffix}")

    for dev in devices:
        if not dev.get("hostname") or not dev.get("ip"):
            raise ValueError(f"Inventory entry needs 'hostname' and 'ip': {dev}")
        dev.setdefault("device_type", "cisco_ios")
        dev.setdefault("role", "")

    if only:
        wanted = {name.lower() for name in only}
        devices = [d for d in devices if d["hostname"].lower() in wanted]
    return devices


def get_credentials():
    return {
        "username": os.getenv("NET_USERNAME") or input("SSH username: "),
        "password": os.getenv("NET_PASSWORD") or getpass("SSH password: "),
        "secret": os.getenv("NET_SECRET", ""),
    }





def connect(device, creds, timeout=15):
    from netmiko import ConnectHandler  

    conn = ConnectHandler(
        device_type=device["device_type"],
        host=device["ip"],
        username=creds["username"],
        password=creds["password"],
        secret=creds.get("secret", ""),
        conn_timeout=timeout,
    )
    if creds.get("secret"):
        conn.enable()
    return conn


def send_parsed(conn, command):
    output = conn.send_command(command, use_textfsm=True)
    if isinstance(output, str):
        if not output.strip():
            return []
        raise ValueError(f"TextFSM could not parse '{command}'. Is ntc-templates installed?")
    return output


def run_task(devices, creds, task):
    from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

    rows, errors = [], []
    for dev in devices:
        host = dev["hostname"]
        try:
            conn = connect(dev, creds)
        except (NetmikoTimeoutException, NetmikoAuthenticationException, OSError) as exc:
            print(f"[FAIL] {host:<18} cannot connect: {type(exc).__name__}")
            errors.append({"hostname": host, "ip": dev["ip"], "error": type(exc).__name__})
            continue
        try:
            with conn:
                rows.extend(task(conn, dev))
            print(f"[ OK ] {host}")
        except Exception as exc:  
            print(f"[FAIL] {host:<18} task error: {exc}")
            errors.append({"hostname": host, "ip": dev["ip"], "error": str(exc)})
    return rows, errors





def add_common_args(parser):
    parser.add_argument("-i", "--inventory", default=str(DEFAULT_INVENTORY),
                        help="Inventory file (.csv/.json/.yaml)")
    parser.add_argument("-d", "--device", action="append", metavar="HOSTNAME",
                        help="Only run on this hostname (repeatable)")
    parser.add_argument("-f", "--format", choices=["csv", "json", "yaml"], default="csv",
                        help="Output format (default: csv)")
    return parser





def _flatten(value):
    return ";".join(map(str, value)) if isinstance(value, (list, tuple)) else value


def save_output(rows, fmt, prefix, output_dir=None):
    output_dir = Path(output_dir or OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{prefix}_{stamp}.{fmt}"

    if fmt == "csv":
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
        with path.open("w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow({k: _flatten(v) for k, v in row.items()})
    elif fmt == "json":
        path.write_text(json.dumps(rows, indent=2))
    elif fmt == "yaml":
        path.write_text(yaml.safe_dump(rows, sort_keys=False))
    else:
        raise ValueError(f"Unsupported format: {fmt}")
    print(f"\nSaved {len(rows)} row(s) -> {path}")
    return path


def _cell(value):
    value = _flatten(value)
    return "-" if value is None else str(value)


def print_table(rows, columns):
    if not rows:
        print("(no rows)")
        return
    widths = [max(len(c), *(len(_cell(r.get(c))) for r in rows)) for c in columns]
    print("  ".join(c.upper().ljust(w) for c, w in zip(columns, widths)))
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(_cell(row.get(c)).ljust(w) for c, w in zip(columns, widths)))
