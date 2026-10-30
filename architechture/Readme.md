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

### Monitoring phase

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/2970ae2f4e9a957c86d8ba7ceb1edd227f411580/assets/C5.png)

different events and system health logs are tracked by certain monitoring systems for traceability and supervision

### Collection phase

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/2970ae2f4e9a957c86d8ba7ceb1edd227f411580/assets/C6.png)

only necessary alerts are needed to get tracked by our SIEM system to get later rational study. those alerts are tracked based on defined rules

### Analysis phase

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9a3b55a04d703ccbe550bbd2cea578cbd30102ac/assets/C3.png)

the analysis process starts with **Direct alert handling with IOCs extraction and enrichment then we shall proceed with collecting more details about the incident (Pre and post activities details collection) in order to prepare by the end our final global analysis
### Response phase

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9a3b55a04d703ccbe550bbd2cea578cbd30102ac/assets/C4.png)

Based on the final report generated later actions should get involved (triage, deeper investigation, containment, isolation ....).
this part might be not the last part for certain scenarios. 
