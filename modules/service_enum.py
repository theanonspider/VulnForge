"""
VulnForge Module : Service Enumeration
Enumerate services (SMB, SSH, FTP, HTTP) on target.
"""

import socket
import re
from datetime import datetime

class ServiceEnumModule:
    def __init__(self):
        self.results = {
            "module": "service_enum",
            "timestamp": datetime.now().isoformat(),
            "target": "",
            "services": []
        }

    def run(self, target, service="all", ports=None):
        """
        Enumerate services on target.
        - target : IP address or domain
        - service : "smb", "ssh", "ftp", "http", "all"
        - ports : list of ports to check (if None, use default ports)
        """
        print(f"[*] Enumerating {service} on {target}...")

        self.results["target"] = target

        # Service → port mapping
        service_ports = {
            "ssh": 22,
            "ftp": 21,
            "http": 80,
            "https": 443,
            "smb": 445,
            "netbios": 139,
            "mysql": 3306,
            "postgres": 5432,
            "rdp": 3389,
            "redis": 6379,
            "elastic": 9200,
        }

        # Determine which services to check
        services_to_check = {}
        if service.lower() == "all":
            services_to_check = service_ports
        elif service.lower() in service_ports:
            services_to_check = {service.lower(): service_ports[service.lower()]}
        else:
            print(f"[!] Unknown service: {service}")
            return self.results

        # If ports provided, override
        if ports:
            port_list = [int(p.strip()) for p in ports.split(',')]
            # Try to match ports to services
            for p in port_list:
                for svc, sp in service_ports.items():
                    if p == sp:
                        services_to_check[svc] = p

        # Enumerate each service
        for svc_name, port in services_to_check.items():
            print(f"    [*] Checking {svc_name} on port {port}...")
            result = self._check_service(target, port, svc_name)
            if result:
                self.results["services"].append(result)
                print(f"        [+] {svc_name} detected: {result.get('banner', '')[:60]}...")
            else:
                print(f"        [-] {svc_name} not detected")

        print(f"    [✓] Enumeration complete. {len(self.results['services'])} services found.")
        return self.results

    def _check_service(self, target, port, service):
        """Check if a service is running on the port and grab banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((target, port))
            if result != 0:
                sock.close()
                return None

            # Try to get banner
            banner = ""
            try:
                if service in ["ssh", "ftp", "smtp"]:
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                elif service in ["http", "https"]:
                    sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                else:
                    sock.send(b"\r\n")
                    banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            except:
                pass

            sock.close()

            # Detect version from banner
            version = self._extract_version(banner, service)

            return {
                "service": service,
                "port": port,
                "banner": banner[:200] if banner else "No banner",
                "version": version
            }

        except Exception as e:
            return None

    def _extract_version(self, banner, service):
        """Extract version info from banner"""
        if not banner:
            return "unknown"

        patterns = {
            "ssh": r"SSH-([\d.]+)",
            "ftp": r"([\d.]+)",
            "http": r"Server: ([^\r\n]+)",
            "smb": r"Windows[\s]+([\d.]+)",
        }

        pattern = patterns.get(service)
        if pattern:
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                return match.group(1)
        return "unknown"
