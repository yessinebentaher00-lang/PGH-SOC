# PGHSOC Web Interface

Just to clarify everything from the start our solution web UI is a sub functionality of our workspace simulated web service interface **PGHConnect** that only some special actors can only be authorized to gain such access.\


In this part you will be able to take full comprehension of our PGHConnect architechture and interfaces details as well as installation and preparation and essentially how do we manage to integrate web service with PGHSOC solution and the link between its logs and other SOC solutions

 * [Installation and prequisities](#Installation-and-prequisities)
 * [PGHConnect interfafces and functionalities](#PGHConnect-interfafces-and-functionalities)
 * [PGHSoc features and integrated solutions](#PGHSoc-features-and-integrated-solutions)

## Installation and prequisities

This section documents the installation and configuration of the web server used to host the PGHConnect web interface, which serves as a simulated authentication portal and log generator for the SOC environment epecially treated under the first scenario incident.

### Prerequisites

- Ubuntu Server 22.04 LTS (or 24.04)
- sudo privileges
- Internet access for package installation

### 1. Update the System

```bash
sudo apt update && sudo apt upgrade -y
```

2. Install Apache2
```bash
sudo apt install apache2 -y
```
Enable Apache2 to start on boot:

```bash
sudo systemctl enable apache2
sudo systemctl start apache2
```
Verify the installation:

```bash
sudo systemctl status apache2
```
Access the default page at: http://<server-ip>/

3. Install PHP
The web application uses PHP for the logging script (logger.php).

```bash
sudo apt install php libapache2-mod-php php-mysql -y
```
Restart Apache2 to load PHP:

```bash
sudo systemctl restart apache2
```

4. Deploy the Web Application Files
Copy the application files to the Apache web root:

```bash
sudo cp index.html style.css main.js logger.php /var/www/html/
sudo cp style.css  /var/www/html/css/
sudo cp main.js /var/www/html/js/
```
Set the correct ownership and permissions:

```bash
sudo chown -R www-data:www-data /var/www/html/
sudo chmod -R 755 /var/www/html/
```
5. Configure the Logger (logger.php)
The logger.php script writes authentication events to a log file that is later collected by Wazuh.

Create the log directory and file:

```bash
sudo mkdir -p /var/log/pghsoc
sudo touch /var/log/pghsoc/auth.log
```
Set permissions so Apache can write to it:

```bash
sudo chown www-data:www-data /var/log/pghsoc/auth.log
sudo chmod 644 /var/log/pghsoc/auth.log
```
Ensure the log is written in JSON format so Wazuh can parse it automatically. Example log entry:

```json
{"app_service":"prsociety","username":"mostafa","src_ip":"192.168.20.10","auth-status":"WRONG_PASSWORD","timestamp":"2026-03-11T10:00:00Z"}
```
6. Configure Wazuh Agent to Collect the Log
edit the Wazuh agent configuration:

```bash
sudo nano /var/ossec/etc/ossec.conf
```
Add the following block inside <ossec_config>:

```xml
<localfile>
  <log_format>json</log_format>
  <location>/var/log/pghsoc/auth.log</location>
</localfile>
```

!! you can check this part within the ossec.conf file of the web server. 
Restart the Wazuh agent:

```bash
sudo systemctl restart wazuh-agent
```

**! You shall have ossec.conf configured within your web server after dealing with installing your wazuh agent**

7. Verify Log Collection
Generate a test login event by accessing the web interface, then check that the Wazuh manager receives the alert:

```bash
sudo tail -f /var/ossec/logs/alerts/alerts.json | grep prsociety
```

## PGHConnect interfafces and functionalities

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/307a3894c7e3c45b7e0e4c3a3abff52084b4a013/assets/D2.png)

All the workers have the right to access the authentication pannel.
in case ofsuccessfull login, the user might access to the workspace ssimulated UI in which he might consult later news, his details, schedules and planning.
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/307a3894c7e3c45b7e0e4c3a3abff52084b4a013/assets/D3.png)

Thus and most important, only the SOC members have the right to access the PGHSOC platform and this done from the start by the system from the authentication till the beginning

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/307a3894c7e3c45b7e0e4c3a3abff52084b4a013/assets/D4.png)



## PGHSoc features and integrated solutions

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/307a3894c7e3c45b7e0e4c3a3abff52084b4a013/assets/D1.png)

The administrator have fully access to all solutions thus based on the ID code inserted analysts have the access to Wazuh velociraptor and the SOAR solutions (TheHive cortex and MISP) and the System supervisors and administrators have access to the rest monitoring solutions 
 ![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/307a3894c7e3c45b7e0e4c3a3abff52084b4a013/assets/D5.png)

! our web server is ordered under a role-based management in which each individual has the right to fullfill certain legal options under the priviliges he got and all his actions are being tracked down and suspicious ones will get instantly monitored and treated (talking especially about malicious authentication insertions).
