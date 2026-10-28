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

## Phisshing attack attempt detection:

| **Rule ID** | **Name** | **Level** | **Severity** | **Utility** |
|---------|------|-------|----------|---------|
| 120001  | Mailcow Base Rule | 0 | Basic | Base Rule for all Mailing json logs to get parsed to wazuh Server |
| 120002  | External Email Received | 3 | Low | User successfully authenticated from each distingushed IP |
| 120010  | Urgent/Action Subject | 5 | Medium | Failed login due to incorrect password |
| 120011  | Password/Credential Subject | 5 | Medium | Login attempt with non-existent username (enumeration) |
| 120012  | Financial/Brand Impersonation| 7 | High | 3+ failed attempts within a short window |
| 120013  | Sender Domain Spoofing | 9 | High | Multiple rate limit events in 60 seconds |
| 120014  | Invalid Sender Format | 10 | High | IP exceeded 10 rate limit events (ongoing attack) |
| 120015  | Internal to Internal Email | 12 | Critical | Large-scale attack from multiple IPs |
| 120016  | oooooo | o | oo | ooooooo |
| 120017  | Suspicious Body Content | 3 | Low | User logged out of the application |
| 120018  | IP Address URL | 4 | Low | User session was restored |
| 120019  | Multiple URLs | 4 | Low | User session was restored |
| 120020  | Sensitive Info Request | 4 | Low | User session was restored |
| 120021  | Attachment Mention | 4 | Low | User session was restored |

**This stays as asterisks**

