"""Realistic Cisco IOS sample outputs used by the offline test-harness."""

SHOW_VERSION = """Cisco IOS Software, C2960X Software (C2960X-UNIVERSALK9-M), Version 15.2(7)E4, RELEASE SOFTWARE (fc2)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2019 by Cisco Systems, Inc.
Compiled Tue 02-Jul-19 11:09 by prod_rel_team

ROM: Bootstrap program is C2960X boot loader
BOOTLDR: C2960X Boot Loader (C2960X-HBOOT-M) Version 15.2(3r)E, RELEASE SOFTWARE (fc1)

{host} uptime is 2 weeks, 3 days, 4 hours, 12 minutes
System returned to ROM by power-on
System restarted at 09:12:44 UTC Mon Sep 21 2026
System image file is "flash:c2960x-universalk9-mz.152-7.E4.bin"
Last reload reason: power-on

cisco WS-C2960X-24PS-L (APM86XXX) processor (revision K0) with 524288K bytes of memory.
Processor board ID {serial}
Last reset from power-on
1 Virtual Ethernet interface
28 Gigabit Ethernet interfaces
Base ethernet MAC Address       : 00:1A:2B:3C:4D:5E
Motherboard assembly number     : 73-15890-06
Configuration register is 0xF
"""

SHOW_IP_INT_BRIEF = """Interface              IP-Address      OK? Method Status                Protocol
Vlan1                  unassigned      YES unset  administratively down down
Vlan99                 192.168.100.21  YES manual up                    up
GigabitEthernet0/1     unassigned      YES unset  up                    up
GigabitEthernet0/2     unassigned      YES unset  up                    down
GigabitEthernet0/3     unassigned      YES unset  down                  down
GigabitEthernet0/4     unassigned      YES unset  administratively down down
"""

SHOW_INT_DESC = """Interface                      Status         Protocol Description
Vl1                            admin down     down
Vl99                           up             up       MGMT-SVI
Gi0/1                          up             up       UPLINK-TO-CORE
Gi0/2                          up             down
Gi0/3                          down           down     USER-PC-FLOOR2
Gi0/4                          admin down     down
Gi0/5                          up             up       printer
Gi0/6                          up             up
"""

SHOW_VLAN_BRIEF = """
VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/3, Gi0/4
10   USERS                            active    Gi0/5, Gi0/6
20   VOICE                            active
30   SERVER                           active    Gi0/7
1002 fddi-default                     act/unsup
1003 token-ring-default               act/unsup
1004 fddinet-default                  act/unsup
1005 trnet-default                    act/unsup
"""

SHOW_SWITCHPORT = """Name: Gi0/1
Switchport: Enabled
Administrative Mode: trunk
Operational Mode: trunk
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: On
Access Mode VLAN: 1 (default)
Trunking Native Mode VLAN: 1 (default)
Administrative Native VLAN tagging: enabled
Voice VLAN: none
Administrative private-vlan host-association: none
Administrative private-vlan mapping: none
Administrative private-vlan trunk native VLAN: none
Administrative private-vlan trunk Native VLAN tagging: enabled
Administrative private-vlan trunk encapsulation: dot1q
Administrative private-vlan trunk normal VLANs: none
Administrative private-vlan trunk associations: none
Administrative private-vlan trunk mappings: none
Operational private-vlan: none
Trunking VLANs Enabled: ALL
Pruning VLANs Enabled: 2-1001
Capture Mode Disabled
Capture VLANs Allowed: ALL

Protected: false
Unknown unicast blocked: disabled
Unknown multicast blocked: disabled
Appliance trust: none

Name: Gi0/2
Switchport: Enabled
Administrative Mode: trunk
Operational Mode: trunk
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: On
Access Mode VLAN: 1 (default)
Trunking Native Mode VLAN: 99 (MANAGEMENT)
Administrative Native VLAN tagging: enabled
Voice VLAN: none
Trunking VLANs Enabled: 10,20,30,99
Pruning VLANs Enabled: 2-1001
Capture Mode Disabled
Capture VLANs Allowed: ALL

Name: Gi0/5
Switchport: Enabled
Administrative Mode: static access
Operational Mode: static access
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: native
Negotiation of Trunking: Off
Access Mode VLAN: 10 (USERS)
Trunking Native Mode VLAN: 1 (default)
Administrative Native VLAN tagging: enabled
Voice VLAN: 20 (VOICE)
Trunking VLANs Enabled: ALL
Pruning VLANs Enabled: 2-1001
Capture Mode Disabled
Capture VLANs Allowed: ALL
"""

SHOW_INT_STATUS = """
Port      Name               Status       Vlan       Duplex  Speed Type
Gi0/1     UPLINK-TO-CORE     connected    trunk      a-full a-1000 10/100/1000BaseTX
Gi0/2     UPLINK-TO-CORE-2   connected    trunk      a-full a-1000 10/100/1000BaseTX
Gi0/3     USER-PC-FLOOR2     connected    1          a-full  a-100 10/100/1000BaseTX
Gi0/4                        notconnect   1            auto   auto 10/100/1000BaseTX
Gi0/5     USER-PC-HR         connected    10         a-full  a-100 10/100/1000BaseTX
Gi0/6                        err-disabled 10           auto   auto 10/100/1000BaseTX
Gi0/7     SRV-WEB01          connected    30         a-full a-1000 10/100/1000BaseTX
Gi0/8                        disabled     1            auto   auto 10/100/1000BaseTX
"""

SHOW_INTERFACES = """GigabitEthernet0/0 is up, line protocol is up
  Hardware is CN Gigabit Ethernet, address is 0050.7966.6800 (bia 0050.7966.6800)
  Description: LINK-TO-CORE
  Internet address is 10.1.1.1/24
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 1000Mb/s, media type is RJ45
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:01, output 00:00:02, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 1000 bits/sec, 2 packets/sec
  5 minute output rate 1000 bits/sec, 1 packets/sec
     1234 packets input, 123456 bytes, 0 no buffer
     Received 12 broadcasts (0 IP multicasts)
     0 runts, 0 giants, 0 throttles
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 watchdog, 0 multicast, 0 pause input
     1100 packets output, 110000 bytes, 0 underruns
     0 output errors, 0 collisions, 1 interface resets
GigabitEthernet0/1 is up, line protocol is up
  Hardware is CN Gigabit Ethernet, address is 0050.7966.6801 (bia 0050.7966.6801)
  Internet address is 10.1.1.1/24
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Full-duplex, 1000Mb/s, media type is RJ45
  Last input 00:00:01, output 00:00:02, output hang never
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 output errors, 0 collisions, 1 interface resets
GigabitEthernet0/2 is up, line protocol is up
  Hardware is CN Gigabit Ethernet, address is 0050.7966.6802 (bia 0050.7966.6802)
  Internet address is 10.1.1.129/25
  MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Full-duplex, 1000Mb/s, media type is RJ45
  Last input 00:00:01, output 00:00:02, output hang never
     0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
     0 output errors, 0 collisions, 1 interface resets
"""

COMMANDS = {
    "show version": SHOW_VERSION,
    "show ip interface brief": SHOW_IP_INT_BRIEF,
    "show interfaces description": SHOW_INT_DESC,
    "show vlan brief": SHOW_VLAN_BRIEF,
    "show interfaces switchport": SHOW_SWITCHPORT,
    "show interfaces status": SHOW_INT_STATUS,
    "show interfaces": SHOW_INTERFACES,
}
