#!/var/ossec/framework/python/bin/python3
import json, sys, requests, uuid, re
from datetime import datetime

LOG = '/var/ossec/logs/integrations.log'

def log(msg):
    with open(LOG, 'a') as f:
        f.write(f"{datetime.now()} - {msg}\n")

def send_to_thehive(title, description, severity, observables, tags, hive_url, api_key):
    payload = {
        "title": title[:150],
        "description": description,
        "type": "wazuh_alert",
        "source": "wazuh",
        "sourceRef": str(uuid.uuid4())[:8],
        "severity": severity,
        "tlp": 2,
        "tags": tags,
        "observables": observables,
        "status": "New"
    }
   
    url = f"{hive_url.rstrip('/')}/api/alert"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
   
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        log(f"Response: {r.status_code}")
        if r.status_code == 201:
            log(f"SUCCESS: {title[:50]}")
        else:
            log(f"FAILED: {r.text[:200]}")
    except Exception as e:
        log(f"ERROR: {e}")

log("=== SCRIPT STARTED ===")
log(str(sys.argv))

if len(sys.argv) < 4:
    log("ERROR: need 3 args")
    sys.exit(1)

alert_file = sys.argv[1]
api_key = sys.argv[2]
hive_url = sys.argv[3]

with open(alert_file) as f:
    alert = json.load(f)

# DEBUG: Log the entire alert structure to see what fields exist
log("=== ALERT STRUCTURE ===")
log(f"Alert keys: {list(alert.keys())}")

rule = alert.get('rule', {})
rule_id = rule.get('id', '')
rule_level = rule.get('level', 0)
rule_desc = rule.get('description', '')
agent = alert.get('agent', {}).get('name', 'unknown')

log(f"Processing rule: {rule_id}")

# ============================================
# 1. PRSOCIETY AUTHENTICATION ALERTS
# ============================================
if rule_id in ['110002', '110003', '110004', '110005', '110006', '110007', '110008', '110009', '110014']:
   
    # Try MULTIPLE locations to find username
    username = (
        alert.get('prsociety.username') or
        alert.get('username') or
        alert.get('data', {}).get('username') or
        alert.get('data', {}).get('user') or
        'unknown'
    )
   
    # Try MULTIPLE locations to find source IP
    src_ip = (
        alert.get('prsociety.src_ip') or
        alert.get('src_ip') or
        alert.get('data', {}).get('src_ip') or
        alert.get('data', {}).get('srcip') or
        'unknown'
    )
   
    # Try MULTIPLE locations to find auth status
    auth_status = (
        alert.get('prsociety.auth-status') or
        alert.get('auth-status') or
        alert.get('data', {}).get('auth-status') or
        alert.get('data', {}).get('auth_status') or
        'unknown'
    )
   
    user_agent = (
        alert.get('prsociety.user_agent') or
        alert.get('user_agent') or
        alert.get('data', {}).get('user_agent') or
        ''
    )
   
    log(f"AUTH - User: {username}, IP: {src_ip}, Status: {auth_status}")
   
    # Also log where we found them for debugging
    if username == 'unknown':
        log("WARNING: Could not find username in any location")
        log(f"Full alert for debugging: {json.dumps(alert, indent=2)[:500]}")
   
    title = f"[PRSociety AUTH] {auth_status} - {username} from {src_ip}"
    desc = f"""## Authentication Alert

| Field | Value |
|-------|-------|
| Account | {username} |
| Status | {auth_status} |
| Source IP | {src_ip} |
| Risk Level | {rule_level} |
| Rule | {rule_desc} |
| Agent | {agent} |
| User Agent | {user_agent} |

### Full Alert
```json
{json.dumps(alert, indent=2)[:1000]}
```"""
   
    severity = 2 if rule_level < 8 else (3 if rule_level < 12 else 4)
    observables = []
    if src_ip and src_ip != 'unknown':
        observables.append({"dataType": "ip", "data": src_ip})
    if username and username != 'unknown':
        observables.append({"dataType": "user", "data": username})
    tags = ["wazuh", "prsociety", "authentication", f"status_{auth_status.lower()}" if auth_status != 'unknown' else "status_unknown"]
   
    send_to_thehive(title, desc, severity, observables, tags, hive_url, api_key)

# ============================================
# 2. PHISHING/EMAIL ALERTS (Mailcow)
# ============================================
elif int(rule_id) >= 120000 and int(rule_id) <= 120021:
    sender = alert.get('sender') or alert.get('prsociety.sender') or alert.get('data', {}).get('sender') or 'unknown'
    receiver = alert.get('receiver') or alert.get('prsociety.receiver') or alert.get('data', {}).get('receiver') or 'unknown'
    subject = alert.get('subject') or alert.get('prsociety.subject') or alert.get('data', {}).get('subject') or 'unknown'
    body = alert.get('body') or alert.get('prsociety.body') or alert.get('data', {}).get('body') or ''
    body = body[:500]
   
    log(f"PHISHING - From: {sender}, To: {receiver}, Subject: {subject[:50]}")
   
    title = f"[MAILCOW PHISHING] {rule_desc[:60]}"
    desc = f"""## Phishing Email Alert

| Field | Value |
|-------|-------|
| Sender | {sender} |
| Receiver | {receiver} |
| Subject | {subject} |
| Rule | {rule_desc} |
| Agent | {agent} |

### Email Body Preview
{body}

### Full Alert
```json
{json.dumps(alert, indent=2)[:1000]}
```"""
   
    severity = 3 if rule_level >= 8 else 2
    observables = []
    if sender and '@' in sender:
        observables.append({"dataType": "email", "data": sender})
    if receiver and '@' in receiver:
        observables.append({"dataType": "email", "data": receiver})
    tags = ["wazuh", "mailcow", "phishing", f"rule_{rule_id}"]
   
    send_to_thehive(title, desc, severity, observables, tags, hive_url, api_key)


else:
    log(f"SKIPPED - Rule {rule_id} not in monitored list")

log("=== SCRIPT FINISHED ===\n")




