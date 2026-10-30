# PGHSOC SIEM global configuration
this project dealt with specefic attack scenarios that's why we tried to be selective in our rules and internal additional configuration you shall follow this guide if you are interested to deal with scenarios alike. \
Generally we tried to englobe rules that are related to phishing attacks, different suspicious possibilities related failed authentication, Privilege escalation and malicious executions and also AD enumeration attacks. \
In this guide you might be capable to set up you SIEM environment and manage the detection and the monitoring of your alerts also this part is firmly attached to Services configurations especially the mailing and Web server part as well as theHive and n8n for integration. \
Those are the main big titles that you shall explore in details: 

1. [ Installation and necessery configurations](#Installation-and-necessery-configurations) 
2. [ Rules configuration](#Rules-configuration) 
   * [ PGHConnect authentication issues](#PGHConnect-authentication-issues) 
   * [ Phishing attack attempt detection](#Phishing-attack-attempt-detection) 
   * [ Suspicious Command Detection](#Suspicious-Command-Detection) 
   * [ Active Directory Enumeration](#Active-Directory-Enumeration) 
3. [ Integrations](#Integrations) 
   * [ TheHive](#TheHive-integration) 
   * [ N8N](#N8N-integration) 
   * [ Velociraptor](#Velociraptor-integration) 
4. [ Dashboarding and monitoring](#Dashboarding) 
5. [ Important](#Important) 

# Installation and necessery configurations

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/wazuh.png)


This section covers the installation of the Wazuh SIEM stack (Indexer, Manager, Dashboard) on a single server. The commands below assume **Ubuntu 20.04/22.04 or Debian 11+** with root or sudo privileges.

## 1. System update and prerequisites

Update the system and install the required packages:

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install curl apt-transport-https lsb-release gnupg2 -y
```
## 2. Download and run the Wazuh installation assistant
The Quickstart script installs the Indexer, Manager, and Dashboard automatically, and generates the required certificates.

```bash
curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh
sudo bash ./wazuh-install.sh -a
```
## 3. Retrieve your credentials
At the end of the installation, the script prints: The Dashboard URL (usually https://<your-server-ip>)\

⚠️ Save the admin password immediately. You will need it to log in to the dashboard.

## 4. Access the dashboard
Open your browser and navigate to:
```text
https://<your-server-ip>
```
Log in with the username admin and the password printed in the previous step.

❗You can access the [Wazuh official site](https://documentation.wazuh.com/current/installation-guide/index.html) for more information and setup.
# Rules configuration

## PGHConnect authentication issues:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110001  | PGHSOC Base Rule | 0 | Basic | Base Rule for all authentication attempt for declenching later alerts |
| 110002  | Successfull login | 3 | Low | User successfully authenticated from each distingushed IP |
| 110003  | Wrong Password Attempt | 5 | Medium | Failed login due to incorrect password |
| 110004  | User not found | 5 | Medium | Login attempt with non-existent username (enumeration) |
| 110005  | Rate limit Triggered| 7 | High | 3+ failed attempts within a short window |
| 110006  | Brute force attempt | 9 | High | Multiple rate limit events in 60 seconds |
| 110007  | Critical rate limit exceeded | 10 | High | IP exceeded 10 rate limit events (ongoing attack) |
| 110008  | DDOS | 12 | Critical | Large-scale attack from multiple IPs |
| 110009  | Multiple attack waves | 13 | Critical | 3+ brute force patterns detected from same IP |
| 110010  | User Logout | 3 | Low | User logged out of the application |
| 110014  | Session Restored | 4 | Low | User session was restored |

## Phishing attack attempt detection:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 120001  | Mailcow Base Rule | 0 | Basic | Base Rule for all Mailing json logs to get parsed to wazuh Server |
| 120002  | External Email Received | 4 | Low | Email from external domain to internal |
| 120010  | Urgent/Action Subject | 10 | High | Phishing subject attempt with urgency keywords |
| 120011  | Password/Credential Subject | 10 | High | Phishing subject related to sensitive data |
| 120012  | Financial/Brand Impersonation| 10 | High | Phishing subject impersonating brands |
| 120013  | Sender Domain Spoofing | 8 | High | Sender domain mimics known brands |
| 120014  | Invalid Sender Format | 7 | Medium | Wrong sender format insertion |
| 120015  | Internal to Internal Email | 4 | Low | Email sent within the same domain |
| 120017  | Suspicious Body Content | 9 | High | Suspicious links or attempted actions within the mail body content |
| 120018  | IP Address URL | 10 | High | URLs containing IP addresses |
| 120019  | Multiple URLs | 6 | Medium | Email contains multiple URLs |
| 120020  | Sensitive Info Request | 10 | High | Email requests personal/sensitive information |
| 120021  | Attachment Mention | 8 | High | Email mentions or includes attachment for immediate investigation |

**In addition to the essential detection rules, I have also prepared a set of additional mailing rules based on normal and habitual mail transactions. These rules are still in progress and are not critical for tracking malicious activities; they mainly cover general mailing server operations and routine activities.**

## Additional Mailcow Rules — Health, Authentication, and Compromise Detection:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110100 | Dovecot: Unknown User | 5 | Medium | Failed login due to unknown user (account enumeration) |
| 110101 | Dovecot: Wrong Password | 5 | Medium | Failed login due to incorrect password |
| 110102 | Dovecot: Aborted Login | 4 | Low | Aborted login — possible reconnaissance |
| 110120 | Postfix: Health OK | 1 | Basic | Postfix health status is 100% |
| 110121 | Postfix: Health Degraded | 7 | High | Postfix health below 100% — investigation needed |
| 110122 | Dovecot: Health OK | 1 | Basic | Dovecot health status is 100% |
| 110123 | Dovecot: Health Degraded | 7 | High | Dovecot health below 100% — investigation needed |
| 110130 | SOGo: Health OK | 1 | Basic | SOGo health status is 100% |
| 110131 | SOGo: Health Degraded | 7 | High | SOGo health below 100% — investigation needed |
| 110140 | API Access Detected | 2 | Low | API endpoint accessed (GET/POST) |
| 110141 | API Authentication Failure | 3 | Low | API returned 401/403 — authentication failure |
| 110150 | PHP-FPM API Access | 2 | Low | PHP-FPM API endpoint accessed |
| 110200 | Phishing: Typosquatting Domain | 8 | High | Sender domain mimics known brands (typosquatting) |
| 110201 | Phishing: Common Keywords | 7 | High | Email contains common phishing keywords |
| 110202 | Phishing: Urgency Tactics | 6 | Medium | Email uses urgency tactics (act now, limited time) |
| 110203 | Phishing: Suspicious Attachment | 9 | High | Email contains dangerous attachment types (.exe, .scr, .js) |
| 110205 | Phishing: URL Shortener | 7 | High | Email contains shortened URL (bit.ly, tinyurl) |
| 110207 | Phishing: DMARC/SPF/DKIM Fail | 9 | High | Email authentication failed — possible spoofing |
| 110220 | Rspamd: Phishing Score | 5 | Medium | Rspamd detected phishing score |
| 110221 | Rspamd: High Confidence Phishing | 7 | High | Rspamd high-confidence phishing detected |
| 110222 | Rspamd: High Spam Score | 6 | Medium | Rspamd detected high spam score |
| 110230 | Multiple Auth Attempts (Same IP) | 8 | High | Multiple authentication attempts from same IP — possible brute force |
| 110231 | High Volume Outbound Emails | 10 | High | High volume of outbound emails — possible compromised account sending spam |


## Suspicious Command Detection:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110050 | Command Base Rule | 0 | Basic | Base rule for command monitoring |
| 110051 | Suspicious Command (Yellow) | 6 | Medium | Low-severity suspicious command executed |

## Overridden Built-in Rule:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 92600 | Python Script Executed | 7 | High | Python script execution detected (overridden) |


## Active Directory Enumeration:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110400 | AD Enumeration Base Rule | 0 | Basic | Base rule for AD enumeration events |
| 110401 | Local Group Enumeration | 8 | Medium | Event ID 4799 — group enumeration detected |
| 110402 | Administrators Group Enumerated | 12 | Critical | Critical group enumeration targeting Admins |

## Linux Audit — AD Attack Tools:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 112001 | BloodHound AD Discovery | 10 | High | BloodHound tool executed (AD discovery) |
| 112002 | Kerberoasting/DCSync Tool | 12 | Critical | Kerberoasting or DCSync tool detected |

## Active Directory Kerberos & Authentication:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110100 | AD Security Base Rule | 0 | Basic | Base rule for AD Security events |
| 110101 | Kerberos TGT Requested | 5 | Medium | Successful Kerberos TGT request |
| 110102 | Kerberos Service Ticket | 5 | Medium | Successful Kerberos service ticket request |
| 110103 | Failed Kerberos TGT | 7 | High | Failed Kerberos TGT request |
| 110104 | Account Locked Out | 8 | Medium | User account locked due to failed attempts |
| 110105 | Admin Privileges Assigned | 6 | Medium | Special admin privileges assigned |
| 110106 | User Logon (4624) | 4 | Low | Standard user logon event |

## AD Account Management:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110200 | Account Mgmt Base Rule | 0 | Basic | Base rule for AD account management |
| 110201 | New User Created | 7 | High | New user account created in AD |
| 110202 | User Deleted | 7 | High | User account deleted from AD |
| 110203 | User Enabled | 6 | Medium | User account re-enabled |
| 110204 | User Disabled | 6 | Medium | User account disabled |

## Kerberos Brute Force:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110300 | Kerberos Pre-Auth Base | 0 | Basic | Base rule for Kerberos pre-auth failures |
| 110301 | Kerberos Brute Force | 12 | Critical | 5+ pre-auth failures in 30 seconds |

## AD Attack Detection — Linux (Auditd):

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110500 | Kerberoasting (GetUserSPNs) | 12 | Critical | Kerberoasting attack tool detected |
| 110501 | AS-REP Roasting (GetNPUsers) | 12 | Critical | AS-REP Roasting attack tool detected |
| 110502 | DCSync / Credential Dumping | 15 | Critical | DCSync or secretsdump executed |
| 110503 | Lateral Movement Tools | 13 | Critical | psexec, wmiexec, atexec, smbexec detected |
| 110504 | Golden/Silver Ticket | 15 | Critical | Golden or Silver Ticket attack detected |
| 110505 | Impacket Tool | 10 | High | Impacket framework executed |
| 110506 | CrackMapExec | 10 | High | CrackMapExec tool executed |
| 110507 | Rubeus | 12 | Critical | Rubeus Kerberos attack tool detected |
| 110508 | Mimikatz | 15 | Critical | Mimikatz credential dumping tool detected |

# Integrations
The following integrations are configured in the Wazuh manager's `ossec.conf` file (typically located at `/var/ossec/etc/ossec.conf`). Each integration forwards specific alerts to external tools for **case management**, **automation**, or **forensic response**.

> ⚠️ **Before you start:** Replace all placeholder IPs, ports, and API keys below with the values that match your own environment. Restart the Wazuh manager after any change:
> ```bash
> sudo systemctl restart wazuh-manager
> ```

| Integration | Purpose | Transport |
|---|---|---|
| **TheHive** | Case management for every alert | HTTP webhook |
| **n8n** | Automated triage workflows | HTTP webhook |
| **Velociraptor** | Forensic collection on the endpoint | Active Response script |

---

## TheHive integration:

**Purpose:** Forwards **every** alert generated by Wazuh to TheHive, where it is converted into a case for analysts to triage.

```xml
<integration>
  <name>custom-w2thive</name>
  <hook_url>http://192.168.77.160:9000</hook_url>
  <api_key>evz4gOd8TGqPg2gfePE6RgZXvOBFiOFO</api_key>
  <alert_format>json</alert_format>
</integration>
```

## N8N integration:

each attack scenario entails a webhook that is used to parse detected critical and high alerts for triage and deeper investigation in n8n automated workflows and this explains the existing of 4 different n8n integrations.\
Each webhook is scoped to a specific group of rule IDs, so alerts are routed to the correct workflow. Four integrations are used because each scenario needs its own set of rule_ids to be forwarded.

```xml
<integration>
  <name>custom-n8n</name>
  <hook_url>http://192.168.77.200:5678/webhook-test/Critical</hook_url>
  <rule_id>110006,110007,110008</rule_id>
</integration>
```

## Velociraptor integration:

When a suspicious command has beed executed, Wazuh triggers an Active Response that runs the install-velo.py script on the endpoint, which enrolls the machine into Velociraptor for forensic collection.

```xml
<command>
  <name>install-velo</name>
  <executable>install-velo.py</executable>
  <timeout_allowed>no</timeout_allowed>
</command>

<active-response>
  <disabled>no</disabled>
  <command>install-velo</command>
  <location>local</location>
  <rules_id>5710,5712,5715</rules_id>
</active-response>
```

### 🟥 You shall check those steps in case an error occured:

* Script location: install-velo.py must exist in /var/ossec/active-response/bin/ and be executable (chmod +x).

* Python dependency: The script requires Python 3 on the endpoint. Ensure python3 is installed and in the PATH.

* Rule IDs: The active response triggers only for rules 5710, 5712, 5715 (Wazuh built-in rules for SSH brute force / authentication failures). If you want Velociraptor to trigger on your custom rules (e.g., 110006), add them to the <rules_id> list.

* Permissions: The script runs as the wazuh user. Ensure it has write access to any directories it uses.

* Network connectivity: Velociraptor must be able to reach the Velociraptor server. Verify the server address inside install-velo.py.

# Dashboarding

## Failed authentication attempt scenarios' dashboard
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/BB2.png)

## Phishing attack attempt scenario dashboard
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/BB.png)

## suspicious executions dashboard
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/BB3.png )

**this one in important to detemine whether an unauthorized actor commited privelege escalation attack**

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/BB4.png)

**this entails the major commands that have been executed**

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/BB5.png)

**this part is focused on deeper investigation over the source and the victim details**

## AD Enumeration attack dashboard
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/BB6.png)

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1702e2a111d7727ace529cbe0fbc0bd23b8d9cfd/assets/Detection2.png)



# Important
