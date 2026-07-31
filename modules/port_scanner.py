"""
VulnForge Module : Port Scanner
Scan TCP ports on a target IP or domain.
"""

import socket
import concurrent.futures
import time
from datetime import datetime

class PortScannerModule:
    def __init__(self):
        self.results = {
            "module": "port_scanner",
            "timestamp": datetime.now().isoformat(),
            "target": "",
            "ports": [],
            "open_ports": [],
            "total_ports_scanned": 0
        }

    def run(self, target, ports, timeout=1, threads=100):
        """
        Scan TCP ports on a target.
        - target : IP address or domain
        - ports : string like "22" or "22,80,443" or "1-1000"
        - timeout : connection timeout in seconds
        - threads : number of concurrent threads
        """
        print(f"[*] Scanning {target} on ports {ports}...")

        self.results["target"] = target

        # Parse port range
        port_list = self._parse_ports(ports)
        self.results["total_ports_scanned"] = len(port_list)

        if not port_list:
            print("[!] No valid ports to scan")
            return self.results

        # Scan ports
        open_ports = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_port = {
                executor.submit(self._scan_port, target, port, timeout): port
                for port in port_list
            }
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    if result:
                        open_ports.append(result)
                        print(f"    [+] Port {port} open")
                except Exception as e:
                    print(f"    [!] Error on port {port}: {e}")

        self.results["open_ports"] = open_ports
        self.results["ports"] = port_list

        print(f"    [✓] Scan complete. {len(open_ports)} open ports found.")
        return self.results

    def _parse_ports(self, ports_str):
        """Parse port string into a list of ints"""
        port_list = []
        try:
            if '-' in ports_str:
                start, end = ports_str.split('-')
                start, end = int(start), int(end)
                if start < 1: start = 1
                if end > 65535: end = 65535
                port_list = list(range(start, end + 1))
            else:
                for p in ports_str.split(','):
                    p = p.strip()
                    if p:
                        port_list.append(int(p))
        except ValueError:
            print("[!] Invalid port format. Use 22,80,443 or 1-1000")
            return []
        return port_list

    def _scan_port(self, target, port, timeout):
        """Attempt TCP connection to a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()
            if result == 0:
                return port
        except socket.gaierror:
            print(f"[!] Invalid target: {target}")
            return None
        except Exception:
            return None
        return None
