# Firewall Configuration


## Dashboarding
![image alt]()


## Rules

<details>
<summary>1. SOC Zone Rules</summary>

| Status | Protocol | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|
| ✅ Enabled | * | SOC Address | 22 | * | * | Anti-Lockout |
| ✅ Enabled | IPv4/IPv6 | * | * | * | * | — |
| ✅ Enabled | IPv4 TCP/UDP | SOC_NET | * | * | 53-443 | — |
| ✅ Enabled | IPv4 TCP/UDP | SOC_NET | * | * | 123 (NTP) | — |
| ✅ Enabled | IPv4 TCP | SOC_NET | * | DMZ_NET | SOC_Agents_Ports | — |
| ✅ Enabled | IPv4 TCP | SOC_NET | * | LAN_NET | 119 (NTP) | — |
| ✅ Enabled | IPv4 TCP | SOC_NET | * | LAN_NET | 514 (Syslog) | — |
| ❌ Disabled | IPv4 TCP | SOC_NET | * | LAN_NET | * | — |
| ❌ Disabled | IPv4 TCP | DMZ_NET | * | LAN_NET | * | — |
| ✅ Enabled | IPv4 TCP | SOC_NET | * | * | * | — |

</details>

<details>
<summary>2. DMZ Zone Rules</summary>

| Status | Protocol | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|
| ✅ Enabled | IPv4 TCP | DMZ_NET | * | SOC_NET | SOC_Agents_Ports | — |
| ✅ Enabled | IPv4 TCP | DMZ_NET | * | SOC_NET | MONITORING_PORTS | — |
| ✅ Enabled | IPv4 TCP | DMZ_NET | * | LAN_NET | 53-123 | — |
| ✅ Enabled | IPv4 TCP | * | * | DMZ_NET | WEB_PORTS | — |
| ✅ Enabled | IPv4 TCP | * | * | DMZ_NET | 21 (FTP) | — |
| ✅ Enabled | IPv4 TCP | * | * | DMZ_NET | Email_Ports | — |
| ✅ Enabled | IPv4+6 | * | * | * | * | — |
| ✅ Enabled | IPv4 TCP | DMZ_NET | * | * | * | — |

</details>

<details>
<summary>3. LAN Zone Rules</summary>

| Status | Protocol | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|
| ✅ Enabled | IPv4 | * | * | LAN net | * | — |
| ✅ Enabled | IPv4 TCP | LAN_NET | * | DMZ_subnets | Mail_Ports | — |
| ✅ Enabled | IPv4 TCP | LAN_NET | * | DMZ_subnets | WEB_PORTS | — |
| ✅ Enabled | IPv4 TCP | LAN_NET | * | SOC_subnets | SOC_Agents_Ports | — |
| ✅ Enabled | IPv4 TCP | LAN_NET | * | SOC_subnets | MONITORING_PORTS | — |
| ✅ Enabled | IPv4 TCP | LAN_NET | * | SOC_subnets | SOC_Agents_Ports | — |
| ✅ Enabled | IPv4 TCP | LAN_NET | * | LAN address | 53 (DNS) | — |
| ✅ Enabled | IPv4 UDP | LAN_NET | * | LAN address | 53 (DNS) | — |
| ✅ Enabled | IPv4 ICMP | LAN_NET | * | * | * | — |
| ✅ Enabled | IPv4 | * | * | LAN_NET | * | — |
| ❌ Disabled | IPv4 TCP | LAN_NET | * | * | * | — |

</details>

<details>
<summary>4. Edge Layer / WAN2 Rules</summary>

| Status | Protocol | Source | Src Port | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|
| ✅ Enabled | IPv4 TCP | WAN2 address | * | * | * | Anti-Lockout |
| ✅ Enabled | IPv4 | * | * | * | * | — |
| ✅ Enabled | IPv4 | * | * | * | * | — |
| ✅ Enabled | IPv4 ICMP | * | * | * | * | — |

</details>

<details>
<summary>5. Floating Rules</summary>

| Status | Interface(s) | Protocol | Source | Destination | Dst Port | Description |
|---|---|---|---|---|---|---|
| ✅ Enabled | LAN | IPv4 TCP | 192.168.20.3 | * | * | Blocked automatically by rule for phishing attempt |
| ✅ Enabled | WAN1 | IPv4 TCP | 192.168.20.3 | * | * | Blocked automatically by rule for phishing attempt |
| ✅ Enabled | DMZ | IPv4 TCP | 192.168.20.3 | * | * | Blocked automatically by rule for phishing attempt |
| ✅ Enabled | WAN2 | IPv4 TCP | 192.168.20.3 | * | * | Blocked automatically by rule for phishing attempt |
| ✅ Enabled | LAN | IPv4 TCP | 192.168.20.4 | * | * | Blocked automatically by rule for phishing attempt |
| ✅ Enabled | LAN | IPv4 TCP | 192.168.20.4 | 192.168.20.3 | * | Blocked automatically by rule for phishing attempt |

</details>


## Routes


## Redunduncy and failover


## Suricata

## Routing (OSPF)

## Monitoring (ntopNG)
