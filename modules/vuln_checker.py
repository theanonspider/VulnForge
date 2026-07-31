"""
VulnForge Module : Vulnerability Checker
Check known vulnerabilities (CVE) based on detected services.
"""

from datetime import datetime

class VulnCheckerModule:
    def __init__(self):
        self.results = {
            "module": "vuln_checker",
            "timestamp": datetime.now().isoformat(),
            "target": "",
            "vulnerabilities": []
        }

        # Base de données de vulnérabilités connues (simplifiée)
        self.vuln_db = {
            "smb": {
                "445": [
                    {"cve": "CVE-2017-0144", "name": "EternalBlue", "risk": "Critical", "description": "SMBv1 remote code execution"},
                    {"cve": "CVE-2017-0143", "name": "EternalChampion", "risk": "Critical", "description": "SMBv1 remote code execution"},
                    {"cve": "CVE-2020-0796", "name": "SMBGhost", "risk": "Critical", "description": "SMBv3 remote code execution"},
                ]
            },
            "ssh": {
                "22": [
                    {"cve": "CVE-2018-15473", "name": "OpenSSH User Enumeration", "risk": "Medium", "description": "Allows user enumeration via timing attack"},
                    {"cve": "CVE-2021-41617", "name": "OpenSSH Privilege Escalation", "risk": "High", "description": "Local privilege escalation in OpenSSH"},
                ]
            },
            "ftp": {
                "21": [
                    {"cve": "CVE-2015-3306", "name": "ProFTPD RCE", "risk": "Critical", "description": "Remote code execution in ProFTPD 1.3.5"},
                    {"cve": "CVE-2019-12815", "name": "ProFTPD SQL Injection", "risk": "High", "description": "SQL injection in ProFTPD mod_sql"},
                ]
            },
            "http": {
                "80": [
                    {"cve": "CVE-2017-5638", "name": "Apache Struts RCE", "risk": "Critical", "description": "Remote code execution in Apache Struts 2"},
                    {"cve": "CVE-2021-44228", "name": "Log4Shell", "risk": "Critical", "description": "Remote code execution via Log4j"},
                ]
            },
            "https": {
                "443": [
                    {"cve": "CVE-2014-0160", "name": "Heartbleed", "risk": "Critical", "description": "OpenSSL memory leak"},
                    {"cve": "CVE-2017-5638", "name": "Apache Struts RCE", "risk": "Critical", "description": "Remote code execution in Apache Struts 2"},
                ]
            },
            "mysql": {
                "3306": [
                    {"cve": "CVE-2016-6662", "name": "MySQL RCE", "risk": "High", "description": "Remote code execution in MySQL"},
                    {"cve": "CVE-2018-25032", "name": "MariaDB RCE", "risk": "High", "description": "Remote code execution in MariaDB"},
                ]
            },
            "rdp": {
                "3389": [
                    {"cve": "CVE-2019-0708", "name": "BlueKeep", "risk": "Critical", "description": "Remote code execution in RDP"},
                    {"cve": "CVE-2020-0609", "name": "RDP RCE", "risk": "Critical", "description": "Remote code execution in RDP"},
                ]
            },
            "redis": {
                "6379": [
                    {"cve": "CVE-2019-9210", "name": "Redis RCE", "risk": "Critical", "description": "Remote code execution in Redis"},
                    {"cve": "CVE-2022-0543", "name": "Redis Lua Sandbox Escape", "risk": "High", "description": "Lua sandbox escape in Redis"},
                ]
            },
        }

    def run(self, target, services, ports=None):
        """
        Check vulnerabilities based on detected services.
        - target : IP address or domain
        - services : list of detected services (from service_enum)
        - ports : dict of {service: port}
        """
        print(f"[*] Checking vulnerabilities on {target}...")

        self.results["target"] = target

        total_vulns = 0

        for service in services:
            service_name = service.get("service", "").lower()
            service_port = str(service.get("port", ""))

            if not service_name:
                continue

            print(f"    [*] Checking {service_name} on port {service_port}...")

            # Vérifier si le service est dans la base de vulnérabilités
            if service_name in self.vuln_db:
                if service_port in self.vuln_db[service_name]:
                    vulns = self.vuln_db[service_name][service_port]
                    if vulns:
                        for vuln in vulns:
                            self.results["vulnerabilities"].append({
                                "service": service_name,
                                "port": service_port,
                                "cve": vuln["cve"],
                                "name": vuln["name"],
                                "risk": vuln["risk"],
                                "description": vuln["description"]
                            })
                            print(f"        [+] {vuln['cve']} - {vuln['name']} ({vuln['risk']})")
                            total_vulns += 1
                    else:
                        print(f"        [-] No known vulnerabilities for {service_name} on port {service_port}")
                else:
                    print(f"        [-] No known vulnerabilities for {service_name} on port {service_port}")
            else:
                print(f"        [-] No known vulnerabilities for {service_name}")

        print(f"    [✓] Vulnerability check complete. {total_vulns} vulnerabilities found.")
        return self.results
