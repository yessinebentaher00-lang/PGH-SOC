# Monitoring 

Centralized dashboarding are often required to visualize systems health and track their problems within a unified dashboard and that's why we tend to use 3 different monitoring solutions to seperate each functionality apart

* [Pfsense (ntopNG)](#Pfsense (ntopNG))
* [Zabbix](#Zabbix)
* [Grafana](#Grafana)


## Pfsense (ntopNG)

within pfsense the firewall manager is able to check networking issues about each area, all the existing endpoints informations and health as well as details about malicious packets and used protocols.

In a unified dashboard general informations about transactions might be used as a key for deeper investigations for certain threat scenarios.

move to firewall section under the architechture folder for more details about firewall ntopng dashboards usage

## Grafana

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/3f0fe07bf1693c0368610bd1d763ef4ac66661a2/assets/P1%20(1).png)
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/3f0fe07bf1693c0368610bd1d763ef4ac66661a2/assets/P1%20(2).png)

**!Grafana has multiple monitoring benefits while it is used for centralized dashboarding representing different endpoints system health storage details and internal problems as well as it englobes network traffic transactions**

## Zabbix


![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/3f0fe07bf1693c0368610bd1d763ef4ac66661a2/assets/P1%20(3).png)
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/3f0fe07bf1693c0368610bd1d763ef4ac66661a2/assets/P1%20(4).png)
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/3f0fe07bf1693c0368610bd1d763ef4ac66661a2/assets/P1%20(5).png)
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/3f0fe07bf1693c0368610bd1d763ef4ac66661a2/assets/P1%20(6).png)

**!might look optional but it does recovered wwhat it was limited for me to encover by the use of Grafana; connectivity, password alteraction and files modification, it does as well represent advanced features over traffic details (as do ntopng do) unless i limited the access to Zabbix only by system administrators only not firewall manager**


## [Wazuh](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9c571e9a4ed0a8f49e23ac03fcd208727beffa7d/SIEM)

it is generally used as a SIEM but we have configured dashboards for alerts monitoring and tracking 
you can check it by accessing the SIEM part in our project


[← Back](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9c571e9a4ed0a8f49e23ac03fcd208727beffa7d/README.md)
