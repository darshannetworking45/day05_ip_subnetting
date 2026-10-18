# 🚀 30 Days of Network Automation (CCNA Level)

Welcome to my **30 Days of Network Automation** series!

The goal of this series is to show how Python can help automate everyday networking tasks using concepts covered in the CCNA curriculum.

Each day includes **3 small, practical Python scripts** focused on a networking topic. Rather than just learning commands or writing code from scratch, we'll explore how to use Python to make networking tasks faster, easier, and more consistent.

### 🛠️ Technologies Used

- Python
- Netmiko
- TextFSM / ntc-templates
- argparse
- ipaddress
- CSV, JSON, and YAML

**Current progress: Day 5 of 30**

Every day's folder includes its scripts, a README, a requirements file, and any additional data files needed for the exercises.

## ⚡ Quick Start

### 1. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your device credentials

Linux/macOS:

```bash
export NET_USERNAME=admin
export NET_PASSWORD='your-password'
export NET_SECRET='enable-secret'  # Optional
```

Windows PowerShell:

```powershell
$env:NET_USERNAME = "admin"
$env:NET_PASSWORD = "your-password"
$env:NET_SECRET = "enable-secret"  # Optional
```

### 4. Run a script

```bash
python day01_device_reachability/03_show_version_inventory.py
```

If the username or password environment variables aren't set, the scripts prompt you for the required credentials.

**Security matters:** Device credentials are never stored directly in the Python code or inventory files.

## 📁 Repository Structure

```text
common/
    netutils.py             # Shared networking utilities

inventory/
    devices.csv             # Device inventory in CSV
    devices.yaml            # Device inventory in YAML
    devices.json            # Device inventory in JSON

dayNN_<topic>/
    01_*.py                 # Script 1
    02_*.py                 # Script 2
    03_*.py                 # Script 3
    README.md
    requirements.txt        # If required for the day's scripts

tests/
    # Offline tests using mock devices

output/
    # Generated reports (ignored by Git)
```

The inventory files contain the same four lab devices in CSV, YAML, and JSON formats.

The shared `common/netutils.py` module handles reusable tasks such as loading inventory, managing credentials, connecting to devices through SSH, parsing command output with TextFSM, and exporting results.

Each day's folder can also include small data files required by its scripts.

## 🧰 Common Command-Line Options

Most device scripts support these options:

| Flag | Description |
|---|---|
| `-i, --inventory` | Select a CSV, JSON, or YAML inventory. Default: `inventory/devices.csv` |
| `-d, --device` | Target a specific hostname; repeatable |
| `-f, --format` | Choose the output format: `csv`, `json`, or `yaml` |

You can update `inventory/devices.csv` to match your own lab setup.

The `device_type` field should use a Netmiko-supported device type, such as `cisco_ios` or `cisco_wlc_ssh`, depending on the device and connection method.

Check each day's README for any additional options.

## 🔒 Safety Rules

All scripts follow a few basic safety practices:

- **Read-only audits:** Reporting scripts use show commands and do not intentionally modify device configurations.
- **Dry-run by default:** Scripts that make configuration changes preview the planned actions. Use `--apply` when you're ready to execute supported changes.
- **Graceful error handling:** If a device fails, the script reports the problem and continues with other devices where possible.
- **Lab first:** Test changes in CML, GNS3, EVE-NG, or a Cisco DevNet sandbox before using them on production equipment.

**Note:** Python scripts that connect through SSH cannot directly manage Packet Tracer's simulated Cisco devices in the same way as real devices or supported virtual appliances.

## 🧪 Test Without Physical Hardware

Run the offline test suite:

```bash
python tests/run_offline_tests.py
```

The tests replace Netmiko's connection function with a mock device that returns realistic Cisco IOS output. Where configured, the scripts use the real `ntc-templates` for parsing and exercise their logic without requiring physical network equipment.

The test suite also covers failure scenarios, such as unreachable devices, and checks that dry-run mode does not push configuration changes.

Offline tests help validate parsing and script logic, but they do not replace testing against the actual IOS versions and platforms used in your lab.

## 📚 Day-by-Day Progress

| Day | Topic | Folder |
|---|---|---|
| 01 | Device Reachability & Inventory | [day01_device_reachability](day01_device_reachability) |
| 02 | Interface Status & Troubleshooting | [day02_interface_status](day02_interface_status) |
| 03 | VLANs | [day03_vlans](day03_vlans) |
| 04 | Trunks & Switchports | [day04_trunks_switchports](day04_trunks_switchports) |
| 05 | IPv4 Subnetting & VLSM | [day05_ip_subnetting](day05_ip_subnetting) |

## 📦 Requirements

- Python 3.9 or later
- Dependencies listed in [`requirements.txt`](requirements.txt)
- A supported network device or virtual lab for live device testing

For the full dependency list, see the repository's `requirements.txt`.

---

**Learn. Build. Troubleshoot. Automate.**

Follow the journey: **NetworkWithDarshan**

GitHub: https://github.com/darshannetworking45