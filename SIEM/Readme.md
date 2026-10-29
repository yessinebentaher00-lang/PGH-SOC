In this part, we shall discover the main rules that were probably necessary to englobe most of the realistic cases faced in each scenario:

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

## Linux Audit — AD Attack Tools:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 112001 | BloodHound AD Discovery | 10 | High | BloodHound tool executed (AD discovery) |
| 112002 | Kerberoasting/DCSync Tool | 12 | Critical | Kerberoasting or DCSync tool detected |

## Active Directory Enumeration:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 110400 | AD Enumeration Base Rule | 0 | Basic | Base rule for AD enumeration events |
| 110401 | Local Group Enumeration | 8 | Medium | Event ID 4799 — group enumeration detected |
| 110402 | Administrators Group Enumerated | 12 | Critical | Critical group enumeration targeting Admins |

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

## Best practices:

**1-** Use local_rules.xml for Minor Tweaks: If you are just making small adjustments or adding a few rules, you can use the default local_rules.xml file located at **/var/ossec/etc/rules/local_rules.xml** .

**2-** Overwriting Built-in Rules: If you need to modify a rule that comes with Wazuh by default, do not edit the original file. Copy the rule into a file in /var/ossec/etc/rules/, make your changes, and add the overwrite="yes" attribute to the rule tag .

**3-** Check File Permissions: After copying files, ensure the Wazuh service can read them. The files should typically be owned by the wazuh user and group (e.g., **sudo chown wazuh:wazuh /var/ossec/etc/rules/local_rules.xml**) .

**4-** Restart the Manager: After adding or modifying rules or decoders, restart the Wazuh manager for the changes to take effect **(sudo systemctl restart wazuh-manager)**.

