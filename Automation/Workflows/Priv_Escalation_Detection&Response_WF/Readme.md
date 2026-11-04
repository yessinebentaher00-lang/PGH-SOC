# Privelege escalation and malicious command execution

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1b0df335ae64b1c6b30096d1e8e990c331b6a7e9/assets/Y3.png)

this scenario is built for all the problems that might be derived from command malicious insertion or execution. 

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1b0df335ae64b1c6b30096d1e8e990c331b6a7e9/assets/Y33.png)

We have prepared a mitigation workflow that similarely to the phishing scenario must be used automatically after the detection of an alert.

the workflow is composed of 4 main phases:

* 1- Alert Case preparation :

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1b0df335ae64b1c6b30096d1e8e990c331b6a7e9/assets/Y34.png)

this parts deals with process details extraction, Casse preparation, tasks creation and assignment.

! different methodologie was ued in there for tasks creation; unlike the previous one. Four main tasks were created (Enrichment, Alert basic analysis, related alerts analysis and reporting)

* 2- Enrichment phase:


![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1b0df335ae64b1c6b30096d1e8e990c331b6a7e9/assets/Y35.png)

Unlike the previous phishing attack, this one is done thanks the velociraptor integration **(while cortex can't handle only the IOCs enrichment not the processes)**.

* 3- Analysis phase:

  
![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1b0df335ae64b1c6b30096d1e8e990c331b6a7e9/assets/Y36.png)

the analysis core starts with analysing superficially the alert detected and all the process that have been executed details in order to come up with a conclusion. Next another AI agent will move on analysing all the ip related alerts to check his criticality state and by the end a report is generated as a dedcustion. 

* 4- Response phase:

![image alt](https://github.com/yessinebentaher00-lang/PGH-SOC/blob/1b0df335ae64b1c6b30096d1e8e990c331b6a7e9/assets/Y37.png)

Same as the phishing response phasee.(copy-paste :p)


