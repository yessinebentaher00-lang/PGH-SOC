
## For switch 4

``` text 
!
no aaa new-model
!
!
!
!
!
!
!
!
ip name-server 8.8.8.8
ip name-server 192.168.77.10
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface GigabitEthernet0/0
 switchport trunk allowed vlan 77
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet0/1
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet0/2
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet0/3
 switchport trunk allowed vlan 77
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet1/0
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet1/1
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet1/2
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet1/3
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet2/0
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet2/1
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet2/2
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet2/3
 switchport access vlan 77
 switchport mode access
 negotiation auto
!
interface GigabitEthernet3/0
 negotiation auto
!
interface GigabitEthernet3/1
 negotiation auto
!
interface GigabitEthernet3/2
 negotiation auto
!
interface GigabitEthernet3/3
 negotiation auto
!
interface Vlan77
 ip address 192.168.77.1 255.255.255.0
!
interface Group-Async1
 physical-layer async
 no ip address
 encapsulation slip
!
ip default-gateway 192.168.77.1
ip forward-protocol nd
!
ip http server
!
ip route 0.0.0.0 0.0.0.0 192.168.77.254
ip route 192.168.1.0 255.255.255.0 192.168.77.254
ip route 192.168.1.0 255.255.255.0 192.168.77.253 11
ip route 192.168.10.0 255.255.255.0 192.168.77.254 4
ip route 192.168.10.0 255.255.255.0 192.168.77.253 5
ip route 192.168.20.0 255.255.255.0 192.168.77.254 3
ip route 192.168.20.0 255.255.255.0 192.168.77.253 6
ip route 192.168.60.0 255.255.255.0 192.168.77.254 6
ip route 192.168.60.0 255.255.255.0 192.168.77.253 10
ip route 192.168.99.0 255.255.255.0 192.168.77.254 2
ip route 192.168.99.0 255.255.255.0 192.168.77.253 7
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!
!
```

## For switch 5

!
ip name-server 8.8.8.8
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface GigabitEthernet0/0
 switchport trunk allowed vlan 80
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet0/1
 switchport trunk allowed vlan 80
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet0/2
 switchport trunk allowed vlan 80
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet0/3
 switchport trunk allowed vlan 80
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet1/0
 negotiation auto
!
interface GigabitEthernet1/1
 negotiation auto
!
interface GigabitEthernet1/2
 negotiation auto
!
interface GigabitEthernet1/3
 negotiation auto
!
interface GigabitEthernet2/0
 negotiation auto
!
interface GigabitEthernet2/1
 negotiation auto
!
interface GigabitEthernet2/2
 negotiation auto
!
interface GigabitEthernet2/3
 negotiation auto
!
interface GigabitEthernet3/0
 negotiation auto
!
interface GigabitEthernet3/1
 negotiation auto
!
interface GigabitEthernet3/2
 negotiation auto
!
interface GigabitEthernet3/3
 negotiation auto
!
interface Vlan80
 ip address 192.168.1.1 255.255.255.0
!
ip default-gateway 192.168.1.1
ip forward-protocol nd
!
ip http server
!
ip route 0.0.0.0 0.0.0.0 192.168.1.4
ip route 192.168.10.0 255.255.255.0 192.168.1.2
ip route 192.168.20.0 255.255.255.0 192.168.1.2
ip route 192.168.77.0 255.255.255.0 192.168.1.2
ip route 192.168.99.0 255.255.255.0 192.168.1.2

## For switch 2

``` text
ip name-server 192.168.77.10
ip cef
no ipv6 cef
!
!
!
spanning-tree mode pvst
spanning-tree extend system-id
!
!
!
!
!
!
!
!
!
!
!
!
!
!
!
interface GigabitEthernet0/0
 switchport access vlan 20
 negotiation auto
!
interface GigabitEthernet0/1
 switchport access vlan 20
 negotiation auto
!
interface GigabitEthernet0/2
 switchport access vlan 20
 negotiation auto
!
interface GigabitEthernet0/3
 switchport trunk allowed vlan 10,20
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet1/0
 switchport trunk allowed vlan 10,20
 switchport trunk encapsulation dot1q
 switchport mode trunk
 negotiation auto
!
interface GigabitEthernet1/1
 negotiation auto
!
interface GigabitEthernet1/2
 negotiation auto
!
interface GigabitEthernet1/3
 negotiation auto
!
interface GigabitEthernet2/0
 negotiation auto
!
interface GigabitEthernet2/1
 negotiation auto
!
interface GigabitEthernet2/2
 negotiation auto
!
interface GigabitEthernet2/3
 negotiation auto
!
interface GigabitEthernet3/0
 negotiation auto
!
interface GigabitEthernet3/1
 negotiation auto
!
interface GigabitEthernet3/2
 negotiation auto
!
interface GigabitEthernet3/3
 negotiation auto
!
interface Vlan10
 ip address 192.168.10.20 255.255.255.0
 shutdown
!
interface Vlan20
 ip address 192.168.20.1 255.255.255.0
!
router ospf 1
 router-id 192.168.10.1
 network 192.168.10.0 0.0.0.255 area 0
 network 192.168.20.0 0.0.0.255 area 0
!
ip forward-protocol nd
!
ip http server
!
ip route 0.0.0.0 0.0.0.0 192.168.20.254
ip ssh server algorithm encryption aes128-ctr aes192-ctr aes256-ctr
ip ssh client algorithm encryption aes128-ctr aes192-ctr aes256-ctr
!

```
