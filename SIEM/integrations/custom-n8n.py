


#!/usr/bin/env python3
import sys
import json
import requests
import os
from datetime import datetime

DEBUG_LOG = "/tmp/custom-n8n-debug.log"

def log(msg):
    try:
        with open(DEBUG_LOG, 'a') as f:
            f.write(f"{datetime.now().isoformat()}: {msg}\n")
    except:
        pass

log("=== SCRIPT STARTED ===")
log(f"Args: {sys.argv}")

# === WEBHOOKS ===
N8N_BRUTEFORCE_WEBHOOK = "http://192.168.77.200:5678/webhook-test/Critical"
N8N_PHISHING_WEBHOOK = "http://192.168.77.200:5678/webhook-test/phishing_alert"
N8N_PRIVILEGE_ESCALATION_WEBHOOK = "http://192.168.77.200:5678/webhook-test/Priv"

# === SINGLE WEBHOOK FOR ALL ENUMERATION RULES ===
N8N_ENUMERATION_WEBHOOK = "http://192.168.77.200:5678/webhook-test/AD"

# === END CONFIGURATION ===

# === USER TO IP MAPPING ===
# Based on your network assignments
USER_IP_MAPPING = {
    "maria": "192.168.20.4",
    "mostafa": "192.168.20.3",
    "ahmed": "192.168.20.3",
    "Administrator": "192.168.77.10",
    "web_server": "192.168.10.5",
    "mail-server": "192.168.10.12",
    "wazuh": "192.168.77.100",
    "velo": "192.168.20.6",
    "monitor": "192.168.77.50",
    "thehive": "192.168.77.60",
    "automator": "192.168.77.70",
}
# === END USER IP MAPPING ===

def get_enumerator_ip(username):
    """Return the IP address for a given username based on mapping"""
    if not username:
        return "UNKNOWN"
   
    username_lower = username.lower().strip()
   
    # Direct match
    if username_lower in USER_IP_MAPPING:
        return USER_IP_MAPPING[username_lower]
   
    # Partial match for common patterns
    for key, ip in USER_IP_MAPPING.items():
        if key in username_lower or username_lower in key:
            return ip
   
    return "UNKNOWN"

# Brute force rules (110006, 110007, 110008)
BRUTEFORCE_RULES = [110006, 110007, 110008]

# Phishing rules (120010-120021)
PHISHING_RULES = [120010, 120011, 120012, 120013, 120014, 120015, 120017, 120018, 120019, 120020, 120021]

# Sudo/Privilege Escalation rules (5401-5407)
PRIVILEGE_ESCALATION_RULES = [5401, 5402, 5403, 5404, 5405, 5407]

# Suspicious commands rules (110051-110060)
SUSPICIOUS_RULES = [110051, 110052, 110053, 110054, 110055, 110056, 110057, 110058, 110059, 110060]

# AD Enumeration rules - ALL GO TO SAME WEBHOOK
ENUMERATION_RULES = [110401, 110402, 110403]

try:
    if len(sys.argv) < 2:
        log("ERROR: No alert file")
        sys.exit(1)
   
    alert_file = sys.argv[1]
    log(f"Reading: {alert_file}")
   
    if not os.path.exists(alert_file):
        log(f"File not found: {alert_file}")
        sys.exit(1)
   
    with open(alert_file, 'r') as f:
        alert = json.load(f)
   
    # Get rule_id
    rule_id_raw = alert.get('rule', {}).get('id')
    log(f"Raw rule_id: {rule_id_raw}")
   
    try:
        rule_id = int(rule_id_raw)
    except (TypeError, ValueError):
        log(f"Could not convert rule_id to int: {rule_id_raw}")
        sys.exit(0)
   
    log(f"Converted rule_id: {rule_id}")
   
    # Determine which webhook to use
    if rule_id in PHISHING_RULES:
        webhook_url = N8N_PHISHING_WEBHOOK
        alert_type = "PHISHING"
        alert_subtype = ""
        log(f"Rule {rule_id} is PHISHING - sending to phishing webhook")
       
    elif rule_id in BRUTEFORCE_RULES:
        webhook_url = N8N_BRUTEFORCE_WEBHOOK
        alert_type = "BRUTEFORCE"
        alert_subtype = ""
        log(f"Rule {rule_id} is BRUTEFORCE - sending to brute force webhook")
       
    elif rule_id in ENUMERATION_RULES:
        webhook_url = N8N_ENUMERATION_WEBHOOK
        alert_type = "AD_ENUMERATION"
        # Determine subtype based on specific rule
        if rule_id == 110401:
            alert_subtype = "LOW_LEVEL_ENUMERATION"
        elif rule_id == 110402:
            alert_subtype = "CRITICAL_ENUMERATION"
        elif rule_id == 110403:
            alert_subtype = "HIGH_ENUMERATION"
        else:
            alert_subtype = "ENUMERATION"
        log(f"Rule {rule_id} is AD ENUMERATION ({alert_subtype}) - sending to single enumeration webhook")
       
    elif rule_id in PRIVILEGE_ESCALATION_RULES or rule_id in SUSPICIOUS_RULES:
        webhook_url = N8N_PRIVILEGE_ESCALATION_WEBHOOK
        if rule_id in PRIVILEGE_ESCALATION_RULES:
            alert_type = "PRIVILEGE_ESCALATION"
            alert_subtype = "SUDO_PRIVILEGE_ESCALATION"
            log(f"Rule {rule_id} is PRIVILEGE ESCALATION - sending to combined webhook")
        else:
            alert_type = "SUSPICIOUS_COMMAND"
            alert_subtype = ""
            log(f"Rule {rule_id} is SUSPICIOUS COMMAND - sending to combined webhook")
       
    else:
        log(f"Skipping rule {rule_id} (not in any target list)")
        sys.exit(0)
   
    # Extract source IP
    src_ip = (
        alert.get('data', {}).get('src_ip') or
        alert.get('data', {}).get('srcip') or
        alert.get('src_ip') or
        alert.get('agent', {}).get('ip') or
        'unknown'
    )
   
    # Extract username (the enumerator)
    username = (
        alert.get('data', {}).get('user') or
        alert.get('data', {}).get('username') or
        alert.get('data', {}).get('dstuser') or
        alert.get('audit', {}).get('user') or
        alert.get('prsociety', {}).get('win', {}).get('eventdata', {}).get('subjectUserName') or
        alert.get('data', {}).get('win', {}).get('eventdata', {}).get('subjectUserName') or
        'unknown'
    )
   
    # === NEW: Get enumerator name and IP ===
    enumerator_name = username if username != 'unknown' else 'UNKNOWN'
    enumerator_ip = get_enumerator_ip(enumerator_name)
    log(f"Enumerator: {enumerator_name} -> IP: {enumerator_ip}")
   
    # Extract command information
    audit_command = alert.get('data', {}).get('audit', {}).get('command') or alert.get('audit', {}).get('command') or ''
    audit_exe = alert.get('data', {}).get('audit', {}).get('exe') or alert.get('audit', {}).get('exe') or ''
   
    # Extract sudo specific data
    sudo_command = alert.get('data', {}).get('command') or alert.get('data', {}).get('COMMAND') or ''
    sudo_user = alert.get('data', {}).get('user') or alert.get('data', {}).get('dstuser') or ''
   
    # Extract enumeration specific data
    enumerated_group = (
        alert.get('prsociety', {}).get('win', {}).get('eventdata', {}).get('targetUserName') or
        alert.get('data', {}).get('win', {}).get('eventdata', {}).get('targetUserName') or
        ''
    )
    target_sid = (
        alert.get('prsociety', {}).get('win', {}).get('eventdata', {}).get('targetSid') or
        alert.get('data', {}).get('win', {}).get('eventdata', {}).get('targetSid') or
        ''
    )
    subject_user_sid = (
        alert.get('prsociety', {}).get('win', {}).get('eventdata', {}).get('subjectUserSid') or
        alert.get('data', {}).get('win', {}).get('eventdata', {}).get('subjectUserSid') or
        ''
    )
    subject_logon_id = (
        alert.get('prsociety', {}).get('win', {}).get('eventdata', {}).get('subjectLogonId') or
        alert.get('data', {}).get('win', {}).get('eventdata', {}).get('subjectLogonId') or
        ''
    )
    enumerated_event_id = (
        alert.get('prsociety', {}).get('win', {}).get('system', {}).get('eventID') or
        alert.get('data', {}).get('win', {}).get('system', {}).get('eventID') or
        ''
    )
   
    # Determine severity based on rule level
    rule_level = alert.get('rule', {}).get('level', 0)
    if rule_level >= 12:
        severity = "CRITICAL"
    elif rule_level >= 8:
        severity = "HIGH"
    elif rule_level >= 5:
        severity = "MEDIUM"
    else:
        severity = "LOW"
   
    # Prepare combined payload
    payload = {
        # Core alert info
        "alert_type": alert_type if alert_type else (alert_subtype if alert_subtype else "UNKNOWN"),
        "alert_subtype": alert_subtype,
        "rule_id": rule_id,
        "rule_description": alert.get('rule', {}).get('description', ''),
        "rule_level": rule_level,
        "severity": severity,
       
        # Agent info
        "agent": alert.get('agent', {}).get('name', 'unknown'),
        "agent_id": alert.get('agent', {}).get('id', 'unknown'),
        "agent_ip": alert.get('agent', {}).get('ip', 'unknown'),
       
        # Source and user
        "src_ip": src_ip,
        "username": username,
        "timestamp": alert.get('timestamp', ''),
        "full_log": alert.get('full_log', '')[:1000],
       
        # === NEW: Enumerator details ===
        "enumerator_name": enumerator_name,
        "enumerator_ip": enumerator_ip,
       
        # Enumeration specific fields
        "enumerated_group": enumerated_group,
        "enumerated_target_sid": target_sid,
        "enumerated_subject_sid": subject_user_sid,
        "enumerated_logon_id": subject_logon_id,
        "enumerated_event_id": enumerated_event_id,
       
        # Suspicious command fields
        "command": audit_command,
        "command_path": audit_exe,
       
        # Sudo/Privilege Escalation fields
        "sudo_command": sudo_command,
        "sudo_user": sudo_user,
       
        # MITRE ATT&CK
        "mitre_id": alert.get('rule', {}).get('mitre', {}).get('id', []),
        "mitre_tactic": alert.get('rule', {}).get('mitre', {}).get('tactic', []),
       
        # Phishing fields
        "email_sender": alert.get('data', {}).get('sender', ''),
        "email_receiver": alert.get('data', {}).get('receiver', ''),
        "email_subject": alert.get('data', {}).get('subject', ''),
        "email_body": alert.get('data', {}).get('body', '')[:500]
    }
   
    log(f"POST to {webhook_url}")
    log(f"Payload: rule_id={rule_id}, type={payload['alert_type']}, enumerator={enumerator_name} ({enumerator_ip})")
   
    response = requests.post(webhook_url, json=payload, timeout=5)
    log(f"Response status: {response.status_code}")
   
    if response.status_code == 200:
        log(f"SUCCESS! Alert {rule_id} sent to {webhook_url}")
        print(f"Alert {rule_id} sent successfully")
    else:
        log(f"Failed: HTTP {response.status_code}")
        log(f"Response body: {response.text[:500]}")
       
except Exception as e:
    log(f"EXCEPTION: {str(e)}")
    import traceback
    log(f"Traceback: {traceback.format_exc()}")
