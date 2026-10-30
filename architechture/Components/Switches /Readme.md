# Switch Configuration
## Switch Links — Access vs Trunk

In a switched network, a port can be configured in one of two main modes: **access** or **trunk**. The mode determines how the port handles VLAN traffic.

---

### Access Link

An **access link** carries traffic for **a single VLAN** only. It connects an **end device** (PC, printer, server, access point) to the switch.

```cisco
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 60
```

## Trunk Link
A trunk link carries traffic for multiple VLANs simultaneously over a single physical link. It connects switch-to-switch, switch-to-router (router-on-a-stick), or switch-to-hypervisor.

```cisco
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk allowed vlan 20,60,80
 switchport trunk native vlan 99
````

❗Pay attention to the connectivity by checking the ACLs configured
