# Windows Server (Active Directory) Installation, configuration and Ubuntu Integration

This section documents the installation of **Windows Server 2022** for Active Directory Domain Services (AD DS) and the configuration required to join Ubuntu endpoints to the domain, enabling centralized authentication with the accounts created in AD.

---

#### 1. Download Links and Prerequisites

* **Windows Server 2022 ISO:** [Microsoft Evaluation Center](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022)
* **VMware Workstation Pro (Free for Personal Use):** [Broadcom Support](https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Workstation+Pro)
* **Ubuntu Endpoint:** Ubuntu Server 22.04/24.04 with network access to the Domain Controller.
* **Hardware Requirements (VM):** At least 2 GB RAM (4 GB recommended), 20–32 GB disk space, and a network adapter connected to the same virtual network as your Ubuntu endpoints.

---

#### 2. Windows Server Installation (VMware)

1. **Create the VM:** In VMware Workstation, select **Create a New Virtual Machine** → **Typical**.
2. **Installer disc image:** Select the downloaded Windows Server 2022 ISO.
3. **Guest OS:** Microsoft Windows → Version: Windows Server 2022.
4. **Disk Size:** Set to at least **20 GB**.
5. **Finish and Power On:** Click **Power on this virtual machine**.
6. **Boot from ISO:** When prompted, press any key to boot from the DVD.
7. **Installation:**
   * Select language and click **Next** → **Install now**.
   * Choose **Windows Server 2022 Standard Evaluation (Desktop Experience)**.
   * Accept the license terms → **Custom: Install Windows only**.
   * Select the unallocated disk → **Next** (installation begins).
8. **Set Administrator Password:** After reboot, enter a strong password for the Administrator account.

---

#### 3. Configure Active Directory Domain Services (AD DS)

Once logged in as Administrator:

**Rename the Server (Optional but recommended):**
Open PowerShell and run:
```powershell
Rename-Computer -NewName "DC01" -Restart
```
Install AD DS Role:
Open Server Manager → Add roles and features → Role-based → Select the server → Check Active Directory Domain Services → Next until Install.

Promote to Domain Controller:

After installation, click the flag icon in Server Manager → Promote this server to a domain controller.

Select Add a new forest.

Root domain name: Enter your domain (e.g., pghconnect.local).

Set a Directory Services Restore Mode (DSRM) password.

Continue with defaults until Install (the server will reboot).

Create Users and Groups:

Open Active Directory Users and Computers.

Right-click your domain → New → User.

Create accounts (e.g., mostafa, maria, mohammed).

Add them to appropriate groups (e.g., Domain Users).

4. Ubuntu Integration (Joining the AD Domain)
Here are the exact commands used to join the Ubuntu endpoints to the Active Directory domain.

Step 1: Install the Required Packages
On each Ubuntu endpoint, install the tools needed to discover and join the domain:

```bash
sudo apt update
sudo apt install -y realmd sssd sssd-tools libnss-sss libpam-sss adcli samba-common-bin
```
Step 2: Point DNS to the Windows Server
For Ubuntu to find the domain, its DNS must point to the Windows Server (Domain Controller). Edit your Netplan config or /etc/resolv.conf to use the Windows Server's IP as the nameserver.

Step 3: Discover and Join the Domain
Verify the domain is discoverable, then join it:


**First, verify the domain is discoverable**
```bash
sudo realm discover pghconnect.local
```
**Then, join the domain (you will be prompted for the Administrator password)**
```bash
sudo realm join pghconnect.local
```
If you need to specify the Administrator account explicitly, use this command instead:

```bash
sudo realm join pghconnect.local -U Administrator
```
#### Step 4: Verify the Connection
Test that the AD accounts are recognized on the Ubuntu machine:

bash
**Check if an AD user is recognized**
```bash
id mostafa@pghconnect.local
```
**Or check their groups**
```bash
groups mostafa@pghconnect.local
```
