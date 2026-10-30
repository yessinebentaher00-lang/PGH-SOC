the PGHSOC concept is dealt within twwo complementary perspectives; we shall know how do different components are intercommunicating and managing different transaction, we must identify as well what solution do we need and predict the data that we are planning exactly to protect.\
Here we managed to prepare our logical and physical work concept:
 * [ Physical architechture](#Physical-architechture) 
 * [ Logical architechture](#Logical-architechture)

# Physical architechture
## Overview
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9a3b55a04d703ccbe550bbd2cea578cbd30102ac/assets/C1.png)

PGHSOC is a security solution implemented within a tiny simulated workspace environment, and here are the main areas and network compositions details 

### Areas

**LAN** : this part is composes to different workers endpoints 

**WAN** : Internet source area access

**DMZ** : gathers mainly the transactions and communication Services (mailing, web and FTP servers) 

**Edge layer** : contains redundant equipments as backups in order to bypass services abruption and failover

<ins>**SOC layer**</ins> : here where our solution basically functions, whether this part is composed as well of 2 necessary sensitive services (DB and AD servers) this area takes actions in supervising events and system healths, tracking malicious events and trying to prevent common issues occurence and problems immediate elimination and stability recovery

## Physical requirements

this architechture is composed of 2 Routers and 5 switches, 2 FWs and 10 labs for workers (simply ubuntu users in our case) wwindows server for AD and ubuntu servers for other services 

# Logical architechture
## Overview
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9a3b55a04d703ccbe550bbd2cea578cbd30102ac/assets/C2.png)
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9a3b55a04d703ccbe550bbd2cea578cbd30102ac/assets/C3.png)
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9a3b55a04d703ccbe550bbd2cea578cbd30102ac/assets/C4.png)

