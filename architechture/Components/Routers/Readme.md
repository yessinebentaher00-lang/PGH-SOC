
# Router Configuration — Cisco CSR1000V

This section documents the configuration of the **Cisco CSR1000V** edge router that connects the PGHSOC infrastructure to the internet (WAN) and routes traffic between the internal VLANs.

**Platform:** Cisco CSR1000V
**Serial (UDI):** `9T8JCAX9YL8`
**Role:** Edge router — NAT, inter-VLAN routing, HSRP
**WAN interface:** `GigabitEthernet1` (DHCP from ISP)
**LAN interfaces:** `Gi2.60`, `Gi3`, `Gi4.80` (802.1Q sub-interfaces)

---

## 1. Global Settings

```cisco
redunduncy


aaa new-model
ip name-server 8.8.8.8
ip cef accounting per-prefix
multilink bundle-name authenticated
license udi pid CSR1000V sn 9T8JCAX9YL8
no license smart enable
diagnostic bootup level minimal
spanning-tree extend system-id
```
❗recuncuncy Enables the redundancy framework (required for HSRP on some platforms). HSRP itself is configured per-interface (standby commands above).

❗aaa new-model — Enables the AAA access-control framework (authentication, authorization, accounting).

❗spanning-tree extend system-id — Extends the bridge ID with the system ID (needed for 4096+ VLANs).

## 2. Interfaces & VLAN Sub-interfaces
### 2.1 WAN — GigabitEthernet1 (DHCP + NAT outside)
```cisco
interface GigabitEthernet1
 ip address dhcp
 ip nat outside
 negotiation auto
 no mop enabled
 no mop sysid
```
ip address dhcp — obtains the public IP from the ISP dynamically.

ip nat outside — marks this interface as the outside of the NAT domain.

negotiation auto — auto-negotiates speed/duplex.

no mop enabled — disables the Maintenance Operation Protocol (legacy DECnet, not needed).

### 2.2 Trunk interface — GigabitEthernet2
```cisco
interface GigabitEthernet2
 no ip address
 negotiation auto
 no mop enabled
 no mop sysid
```
This is the 802.1Q trunk carrying VLAN 60 to the sub-interface below.

### 2.3 VLAN 60 — GigabitEthernet2.60 (NAT inside + HSRP)
````cisco
interface GigabitEthernet2.60
 encapsulation dot1Q 60
 ip address 192.168.60.20 255.255.255.0
 ip nat inside
 standby 2 ip 192.168.60.253
 standby 2 priority 110
 standby 2 preempt
 standby 2 name HSRP_GROUP_2
````
encapsulation dot1Q 60 — tags traffic for VLAN 60.

ip address 192.168.60.20/24 — the router's IP in VLAN 60.

ip nat inside — marks this interface as the inside of NAT.

HSRP group 2 — virtual IP 192.168.60.253, priority 110 (higher than default 100), preempt enabled → this router becomes the active HSRP gateway when available.

### 2.4 VLAN 20 — GigabitEthernet3 (NAT inside)
````cisco
interface GigabitEthernet3
 ip address 192.168.20.20 255.255.255.0
 ip nat inside
 negotiation auto
 no mop enabled
 no mop sysid
````
Directly routed VLAN 20 (192.168.20.0/24).

Marked as NAT inside.

### 2.5 Trunk interface — GigabitEthernet4
````cisco
interface GigabitEthernet4
 no ip address
 negotiation auto
 no mop enabled
 no mop sysid
````
Carries VLAN 80 to the sub-interface below.

### 2.6 VLAN 80 — GigabitEthernet4.80 (NAT inside + HSRP)
````cisco
interface GigabitEthernet4.80
 encapsulation dot1Q 80
 ip address 192.168.1.3 255.255.255.0
 ip nat inside
 standby 1 ip 192.168.1.253
 standby 1 preempt
 standby 1 name HSRP_GROUP_1
````
VLAN 80 uses the 192.168.1.0/24 subnet.

HSRP group 1 — virtual IP 192.168.1.253, default priority 100, preempt enabled.

## 3. NAT Configuration
````cisco
ip nat inside source list 1 interface GigabitEthernet1 overload
ip nat inside source list NAT_ACL interface GigabitEthernet1 overload
ip nat inside source list 1 interface Gi1 overload — PAT (port address translation) for ACL 1, using the WAN interface IP.
````
ip nat inside source list NAT_ACL interface Gi1 overload — PAT for the named ACL NAT_ACL, using the same WAN IP.

⚠️ Note: Two NAT statements pointing to the same outside interface with overload is valid, but ACL 1 is not defined anywhere in this configuration. You likely meant to reference NAT_ACL only — consider removing the first line to avoid confusion.

NAT ACL
````cisco
ip access-list standard NAT_ACL
 permit 192.168.60.0 0.0.0.255
````
Only VLAN 60 (192.168.60.0/24) is permitted to be NAT-translated.

VLANs 20 and 80 are marked ip nat inside but are not in NAT_ACL → they will not reach the internet unless you add them. If they are meant to be internet-facing, add:

````cisco
ip access-list standard NAT_ACL
 permit 192.168.20.0 0.0.0.255
 permit 192.168.1.0 0.0.0.255
````
## 4. Routing & Management
````cisco

ip route 192.168.1.3 255.255.255.255 192.168.1.1
````
ip route 192.168.1.3 255.255.255.255 192.168.1.1 — Host route for 192.168.1.3 (this router's own Gi4.80 IP) pointing to 192.168.1.1.




crypto key generate rsa modulus 2048
