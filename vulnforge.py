#!/usr/bin/env python3
"""
🔧 VulnForge — Exploit Framework for Authorized Testing
"""

import click
import json
import os
import sys
from datetime import datetime

# Modules V1
from modules.port_scanner import PortScannerModule
from modules.service_enum import ServiceEnumModule
from modules.vuln_checker import VulnCheckerModule
from modules.exploit_smb import ExploitSMBModule
from modules.exploit_ssh import ExploitSSHModule
from modules.exploit_ftp import ExploitFTPModule
from modules.exploit_web import ExploitWebModule
from modules.privilege_escalation import PrivilegeEscalationModule
from modules.payload_generator import PayloadGeneratorModule
from modules.report import ReportModule

VERSION = "1.0.0"
CONFIG_FILE = "config.json"
TOKEN_FILE = "vulnforge.token"
BANNER = """
╔══════════════════════════════════════════════╗
║                                              ║
║   🔧  VULNFORGE — Exploit Framework       ║
║        Version 1.0                          ║
╚══════════════════════════════════════════════╝
"""

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def check_token():
    config = load_config()
    if not config.get("token_required", True):
        return True
    if not os.path.exists(TOKEN_FILE):
        print(f"[!] Authorization token required. Create {TOKEN_FILE}")
        return False
    with open(TOKEN_FILE, "r") as f:
        token = f.read().strip()
    if token != "VULNFORGE_AUTHORIZED":
        print("[!] Invalid token.")
        return False
    return True

@click.group()
@click.version_option(version=VERSION, prog_name="VulnForge")
def main():
    """🔧 VulnForge — Exploit Framework for Authorized Testing"""
    if not check_token():
        sys.exit(1)

# ============ SCAN ============
@main.command()
@click.option("--target", "-t", required=True, help="Target IP or domain")
@click.option("--ports", "-p", default="1-1000", help="Port range (ex: 22,80,443 or 1-1000)")
@click.option("--timeout", default=1, help="Connection timeout (seconds)")
@click.option("--threads", default=100, help="Number of threads")
def scan(target, ports, timeout, threads):
    """Scan ports on a target"""
    module = PortScannerModule()
    result = module.run(target, ports, timeout, threads)
    print(json.dumps(result, indent=2))

# ============ ENUM ============
@main.command()
@click.option("--target", "-t", required=True, help="Target IP or domain")
@click.option("--service", "-s", default="all", help="Service to enumerate (smb, ssh, ftp, http, all)")
@click.option("--ports", help="Specific ports to check (comma-separated)")
def enum(target, service, ports):
    """Enumerate services on a target"""
    module = ServiceEnumModule()
    result = module.run(target, service, ports)
    print(json.dumps(result, indent=2))

# ============ VULN_CHECK ============
@main.command()
@click.option("--target", "-t", required=True, help="Target IP or domain")
@click.option("--services", "-s", required=True, help="Services JSON string (from enum result)")
def vuln_check(target, services):
    """Check for known vulnerabilities (CVE)"""
    import json as json_lib
    try:
        services_list = json_lib.loads(services)
        if not isinstance(services_list, list):
            print("[!] Services must be a JSON array")
            return
    except:
        print("[!] Invalid JSON format for services")
        return
    module = VulnCheckerModule()
    result = module.run(target, services_list)
    print(json_lib.dumps(result, indent=2))

# ============ EXPLOIT ============
@main.command()
@click.option("--target", "-t", required=True, help="Target IP")
@click.option("--exploit", "-e", default="eternalblue", help="Exploit to use (eternalblue, smbghost, ssh, ftp, web)")
@click.option("--port", default=445, help="Target port")
@click.option("--username", help="Username for brute force")
@click.option("--password", help="Password for brute force")
@click.option("--wordlist", help="Path to wordlist (user:pass)")
def exploit(target, exploit, port, username, password, wordlist):
    """Launch an exploit against a target"""
    exploit_lower = exploit.lower()
    
    if exploit_lower in ["eternalblue", "smbghost"]:
        module = ExploitSMBModule()
        result = module.run(target, exploit_lower, port)
    elif exploit_lower == "ssh":
        module = ExploitSSHModule()
        result = module.run(target, port, username, password, wordlist)
    elif exploit_lower == "ftp":
        module = ExploitFTPModule()
        result = module.run(target, port, username, password, wordlist)
    elif exploit_lower == "web":
        module = ExploitWebModule()
        result = module.run(target)
    else:
        print(f"[!] Unknown exploit: {exploit}")
        return
    print(json.dumps(result, indent=2))

# ============ GENERATE PAYLOAD ============
@main.command()
@click.option("--payload", "-p", default="reverse", help="Payload type (reverse, bind)")
@click.option("--lhost", required=True, help="Listener IP")
@click.option("--lport", default=4444, help="Listener port")
@click.option("--format", "-f", default="raw", help="Format (raw, base64, hex, powershell, bash)")
@click.option("--os", default="linux", help="Target OS (linux, windows)")
def generate_payload(payload, lhost, lport, format, os):
    """Generate a payload (reverse shell, bind shell, etc.)"""
    module = PayloadGeneratorModule()
    result = module.run(payload, lhost, lport, format, os)
    print(json.dumps(result, indent=2))

# ============ PRIVILEGE ESCALATION ============
@main.command()
@click.option("--target", "-t", default="localhost", help="Target IP or hostname")
@click.option("--remote", is_flag=True, help="Check remote target (requires credentials)")
@click.option("--username", help="Username for remote access")
@click.option("--password", help="Password for remote access")
def priv_esc(target, remote, username, password):
    """Attempt privilege escalation detection on target"""
    module = PrivilegeEscalationModule()
    result = module.run(target, remote, username, password)
    print(json.dumps(result, indent=2))

# ============ REPORT ============
@main.command()
@click.option("--output", "-o", default="./reports", help="Output directory")
@click.option("--format", "-f", default="html", help="Report format (html, json, both)")
@click.option("--module-results", "-m", multiple=True, help="Module results JSON to include")
def report(output, format, module_results):
    """Generate a report of all findings"""
    module = ReportModule(output)
    import json as json_lib
    for result_json in module_results:
        try:
            data = json_lib.loads(result_json)
            module.add_module_result(data.get("module", "unknown"), data)
        except:
            pass
    
    if format in ["html", "both"]:
        module.generate_html()
    if format in ["json", "both"]:
        module.generate_json()

if __name__ == "__main__":
    main()
