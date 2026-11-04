# SOAR Integration: Wazuh, TheHive, Cortex, MISP, and n8n

This section documents the integration of the SOAR stack used in the PGH-SOC project. The goal is to automate the lifecycle from detection to case management, threat intelligence enrichment, and incident response. Wazuh acts as the detection source, TheHive as the case management platform, Cortex as the enrichment engine, MISP as the threat intelligence repository, and n8n as the orchestration layer connecting them all.

---

## Integration Architecture

The data flow follows a clear pipeline:

1. **Wazuh** detects an event and generates an alert.
2. **TheHive** receives the alert and creates a case.
3. **TheHive** invokes **Cortex** to extract and enrich observables (IPs, hashes, domains, URLs).
4. **Cortex** queries **MISP** and other analyzers to correlate observables with known threat intelligence.
5. Enrichment results are written back to the TheHive case for analyst review.
6. **n8n** orchestrates notifications and automated actions based on case severity.

---

## Wazuh to TheHive Integration

The first link in the chain is getting Wazuh alerts into TheHive as cases. This is done in two ways.

| Method | Description | Advantage |
|---|---|---|
| **Direct Wazuh Integration** | A Wazuh integration script forwards alerts directly to TheHive's API using the webhook URL and API key. | Simple, low latency |
| **n8n as Orchestrator** | n8n receives the Wazuh alert via webhook and uses an HTTP Request node to create a TheHive case. | Flexible, supports conditional logic and multi-step workflows |

The TheHive node in n8n supports creating alerts, cases, and observables, and can trigger Cortex analyzers directly from the workflow.

---

## Cortex Integration with TheHive

Cortex is the enrichment engine. It receives observables from TheHive and runs analyzers against them.

| Configuration Step | Where It Is Done | Purpose |
|---|---|---|
| Enable Cortex connector | TheHive `application.conf` | Allows TheHive to communicate with Cortex |
| Set Cortex server URL | TheHive `application.conf` | Points to `http://<CORTEX_IP>:9001` |
| Set Cortex API key | TheHive `application.conf` | Authenticates TheHive to Cortex |
| Restart TheHive | System service | Applies the configuration |
| Verify connection | TheHive organization settings | Cortex appears as "Connected" |

When an analyst adds an observable to a TheHive case, they select **Actions → Analyze** and choose a Cortex analyzer. Cortex runs the analyzer and returns the results to the observable's Analysis tab within seconds.

---

## MISP Integration for Threat Intelligence

MISP serves as the threat intelligence repository. It stores IOCs (IPs, domains, hashes) and provides correlation data to Cortex.

| Step | Action | Result |
|---|---|---|
| 1 | TheHive sends an observable (e.g., an IP) to Cortex | Observable is queued for analysis |
| 2 | Cortex runs the MISP analyzer | Cortex queries the MISP API |
| 3 | MISP returns matching events, attributes, or IOCs | Threat intelligence data is retrieved |
| 4 | Cortex formats the results | Enrichment report is generated |
| 5 | Results are returned to TheHive | Analyst sees IOC matches in the case |

This allows analysts to see whether an IP or hash has been observed in previous campaigns or is associated with known threat actors.

---

## n8n Automation Workflows

n8n ties everything together. The typical workflow structure is:

| Step | Action | Tool |
|---|---|---|
| **Trigger** | Wazuh alert webhook or TheHive case creation | n8n Webhook node |
| **Step 1** | Create TheHive case from alert data | TheHive node or HTTP Request |
| **Step 2** | Trigger Cortex enrichment for observables | HTTP Request to Cortex API |
| **Step 3** | Query MISP for threat intelligence context | HTTP Request to MISP API |
| **Step 4** | Send Slack notification with case details | Slack node |

This orchestration pattern is common in open-source SOC builds: n8n acts as the glue that connects Wazuh, TheHive, Cortex, and MISP into a single automated pipeline.

---

## Summary Table

| Component | Role | Integration Point |
|---|---|---|
| **Wazuh** | SIEM / Detection | Sends alerts to TheHive (direct or via n8n) |
| **TheHive** | Case Management | Receives alerts, creates cases, invokes Cortex |
| **Cortex** | Enrichment Engine | Receives observables from TheHive, queries MISP and other analyzers |
| **MISP** | Threat Intelligence | Provides IOC correlation data to Cortex |
| **n8n** | Orchestration | Connects all components, automates case creation and enrichment workflows |

---


[<- back](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/9c571e9a4ed0a8f49e23ac03fcd208727beffa7d/README.md)
