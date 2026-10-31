# Mailing Server Details and Configuration

*[Mail Server Installation and Configuration](#Mail-Server-Installation-and-Configuration)


*[Mailing Server Details](Mailing-Server-Details)

## Mail Server Installation and Configuration 
This section documents the installation and configuration of the Mailcow mail server used to simulate email traffic, generate phishing detection logs, and provide a realistic target for security monitoring within the SOC environment.

### Prerequisites
Operating System: Ubuntu 22.04 LTS or 24.04 LTS (fresh installation recommended) 

Hardware: Minimum 6 GB RAM, 2 CPU cores, 30 GB storage (ClamAV and Rspamd are memory-intensive) 

Domain Name: A Fully Qualified Domain Name (FQDN), e.g., mail.yourdomain.local

DNS Records: Properly configured A, MX, and CNAME records (see Section 3)

Root/Sudo Access: Required for Docker and Mailcow installation

Port 25: Must be open and not blocked by your ISP/provider 

### 1. System Preparation
Update the system packages:

````bash
sudo apt update && sudo apt upgrade -y
````
Install the required system packages:

````bash
sudo apt install -y git openssl curl gawk coreutils grep jq
````
### 2. Install Docker and Docker Compose
Mailcow requires Docker Engine version 24.0.0 or higher and Docker Compose version 2.0 or higher .

````bash
curl -sSL https://get.docker.com/ | CHANNEL=stable sh
sudo systemctl enable --now docker
````
Install the Docker Compose plugin:

````bash
sudo apt install -y docker-compose-plugin
````
Verify the installation:

````bash
docker --version
docker compose version
````
3. Configure DNS Records
Before running Mailcow, configure the following DNS records for your domain :

Type	Name	Value
A	mail	your_server_ip
MX	@	mail.your_domain (priority 10)
TXT	@	v=spf1 mx a -all
CNAME	autodiscover	mail.your_domain
CNAME	autoconfig	mail.your_domain

4. Clone and Configure Mailcow
Clone the Mailcow repository:

```` bash
cd /opt
sudo git clone https://github.com/mailcow/mailcow-dockerized
cd mailcow-dockerized
````
Generate the configuration file:

````bash
sudo ./generate_config.sh
````
When prompted:

Hostname: Enter your FQDN (e.g., mail.yourdomain.local)

Timezone: Confirm or change to your timezone

Branch: Select the stable/master branch 

Review the generated configuration:

````bash
grep -E '^(MAILCOW_HOSTNAME|HTTP_PORT|HTTPS_PORT|TZ)=' mailcow.conf
````
### 5. Start Mailcow
Download the Docker images and start the containers:

````bash
sudo docker compose pull
sudo docker compose up -d
````
Verify all containers are running:

````bash
sudo docker compose ps
````
Access the admin interface at: https://mail.yourdomain.local/admin

Default credentials:

Username: admin

Password: moohoo 

### 6. Create Domain and Mailboxes
Log in to the admin interface.

Navigate to E-Mail → Configuration → + Add domain.

Add your domain and copy the generated DKIM record to your DNS provider .

Navigate to Mailboxes → Mailboxes → + Add mailbox to create test users (e.g., mostafa@pghconnect.local, maria@pghconnect.local).

### 7. Configure Wazuh Agent to Collect Mailcow Logs
The Wazuh agent on the Mailcow server must be configured to monitor the container logs for phishing detection.

Edit the Wazuh agent configuration:

````bash
sudo nano /var/ossec/etc/ossec.conf
````
Add the following block inside <ossec_config> to monitor Mailcow container logs:

````xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/lib/docker/containers/*/*.log</location>
</localfile>
````
Alternatively, if you have configured Mailcow to write logs to a specific file, use that path instead .

## Mailing Server Details

Restart the Wazuh agent:

````bash
sudo systemctl restart wazuh-agent
````
