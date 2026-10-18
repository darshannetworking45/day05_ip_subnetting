# Day 05: IPv4 Subnetting & VLSM 🚀

**CCNA Domain:** Network Fundamentals

Welcome to Day 5 of my **30 Days of Network Automation (CCNA Level)** series!

Today, we're using Python to make IPv4 subnetting easier. Instead of calculating every network address, subnet mask, and usable host range manually, we can use Python to handle the calculations and help plan IP addressing more efficiently.

## 🧠 Understanding the Concept

**Subnetting** divides a larger IP network into smaller networks. It's an essential CCNA skill and helps us organize IP addresses, separate network segments, and use address space efficiently.

Here are a few important concepts to understand:

- **Usable hosts:** For a typical IPv4 subnet, the number of usable host addresses is \(2^{\text{host bits}} - 2\). The exceptions include `/31` point-to-point subnets, which support two addresses, and `/32` prefixes, which represent a single address.
- **VLSM (Variable Length Subnet Masking):** VLSM allows us to create subnets of different sizes based on the number of hosts each network needs. A common approach is to sort requirements from largest to smallest before allocating address blocks.
- **Unique IP addressing:** Each interface needs an appropriate IP address for its network. Accidentally assigning the same IP to two interfaces can cause conflicts.
- **Overlapping subnets:** Using the same subnet on different devices can be perfectly normal when those interfaces belong to the same VLAN or link. However, overlapping but different prefixes, such as `10.1.1.0/24` and `10.1.1.128/25`, need investigation when they are intended to be separate networks.

The VLSM planner calculates the required host bits and allocates appropriately sized subnets, using `/30` as the minimum prefix for ordinary IPv4 subnet allocations in this planner.

## 🛠️ Scripts Included

| Script | What it does |
|---|---|
| `01_subnet_calculator.py` | Calculates subnet details and splits networks into smaller subnets |
| `02_vlsm_planner.py` | Allocates subnets based on host requirements defined in YAML |
| `03_ip_overlap_checker.py` | Detects duplicate IP addresses and overlapping subnets |

**Data files included:**

- `vlsm_requirements.yaml` — network and host requirements for the VLSM planner
- `sample_interfaces.csv` — sample interface addresses for offline conflict checks

## ⚡ Run the Scripts

### 1. Calculate and split a subnet

```bash
python day05_ip_subnetting/01_subnet_calculator.py 192.168.1.77/26 --split 28
```

This calculates the network information for `192.168.1.77/26` and splits the network into smaller `/28` subnets.

The calculator saves a report only when you use its `--save` option.

### 2. Create a VLSM plan

```bash
python day05_ip_subnetting/02_vlsm_planner.py -r day05_ip_subnetting/vlsm_requirements.yaml
```

The planner reads the host requirements from the YAML file, allocates appropriately sized networks, and reports usable host capacity and remaining address space.

### 3. Check for duplicate IPs and overlapping subnets

```bash
python day05_ip_subnetting/03_ip_overlap_checker.py --from-csv day05_ip_subnetting/sample_interfaces.csv
```

This runs the checker against the sample CSV file, so you can practise without connecting to a router or switch.

For live checks, the script supports the inventory and device options documented in its CLI help.

### Credentials

Scripts 1 and 2 work without device credentials. Script 3 also supports offline CSV mode, so credentials are unnecessary when using `--from-csv`.

For live device access, set your credentials in the terminal:

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

Never hard-code credentials in your scripts or inventory files.

## 📊 Sample Output

You can run the project's offline tests to reproduce the mock-device results without physical hardware:

```bash
python tests/run_offline_tests.py
```

### 1. VLSM Planner — `02_vlsm_planner.py`

```text
VLSM plan for 192.168.10.0/24:

NAME          HOSTS_NEEDED  SUBNET              NETMASK           USABLE_HOSTS  SPARE
Sales         60            192.168.10.0/26     255.255.255.192   62            2
Guest-WiFi    45            192.168.10.64/26    255.255.255.192   62            17
Engineering   28            192.168.10.128/27   255.255.255.224   30            2
Management    10            192.168.10.160/28   255.255.255.240   14            4
WAN-Link-1    2             192.168.10.176/30   255.255.255.252   2             0
WAN-Link-2    2             192.168.10.180/30   255.255.255.252   2             0

Addresses used: 184/256 (72%); free: 72

Saved 6 row(s) -> output/vlsm_plan_<timestamp>.csv
```

**What does this tell us?**

- Sales and Guest-WiFi each receive a `/26`, providing 62 usable host addresses.
- Engineering receives a `/27`, while Management receives a `/28`.
- Each WAN link receives a `/30`, providing two usable IPv4 addresses under the traditional subnetting model.
- The plan allocates six subnets within the original `/24` network.

### 2. IP Conflict Checker — `03_ip_overlap_checker.py`

```text
Checking 7 interface addresses...

FINDING          A_DEVICE      A_INTERFACE          A_IP          B_DEVICE      B_INTERFACE          B_IP
DUPLICATE-IP     R1-EDGE       GigabitEthernet0/0   10.1.1.1/24   R1-EDGE       GigabitEthernet0/1   10.1.1.1/24
SUBNET-OVERLAP   R1-EDGE       GigabitEthernet0/0   10.1.1.1/24   R1-EDGE       GigabitEthernet0/2   10.1.1.129/25
SUBNET-OVERLAP   R1-EDGE       GigabitEthernet0/1   10.1.1.1/24   R1-EDGE       GigabitEthernet0/2   10.1.1.129/25
DUPLICATE-IP     SW-ACCESS-01  Vlan10               10.10.10.3/24 SW-ACCESS-02  Vlan10               10.10.10.3/24

Saved 4 row(s) -> output/ip_conflicts_<timestamp>.csv
```

**What does this tell us?**

- `R1-EDGE` has the same IP address assigned to two interfaces.
- The `/24` and `/25` prefixes overlap, so their intended network design should be checked.
- Two access switches show the same management IP address, which may indicate a duplicate IP conflict.

These findings need context before making changes. For example, duplicate IP addresses can be valid in separate VRFs, but this script does not model VRF boundaries.

Reports can be exported in CSV, JSON, or YAML format using the supported `-f` option.

## 📦 Requirements

- Python 3.9+
- Dependencies listed in [`requirements.txt`](requirements.txt)

## 🔎 Notes

- Scripts 1 and 2 run entirely offline.
- Script 3 supports `--from-csv` for offline checks; live mode collects interface information from devices in the inventory.
- The subnet calculator writes a report only when `--save` is supplied.
- The checker does not account for VRFs, so review reported conflicts against the actual network design before changing any addresses.

---

**Learn. Build. Troubleshoot. Automate.**

Follow **NetworkWithDarshan** for more practical networking and Python automation content.

GitHub: https://github.com/darshannetworking45