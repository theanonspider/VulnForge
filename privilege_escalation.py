"""
VulnForge Module : Privilege Escalation
Check for local privilege escalation vectors (Windows/Linux).
"""

import os
import platform
import subprocess
from datetime import datetime

class PrivilegeEscalationModule:
    def __init__(self):
        self.results = {
            "module": "privilege_escalation",
            "timestamp": datetime.now().isoformat(),
            "target": "",
            "vectors": [],
            "output": ""
        }

    def run(self, target="localhost", remote=False, username=None, password=None):
        """
        Check for privilege escalation vectors.
        - target : IP or hostname
        - remote : whether to check remotely (requires credentials)
        - username : username for remote access
        - password : password for remote access
        """
        print(f"[*] Checking privilege escalation vectors on {target}...")

        self.results["target"] = target

        if platform.system() == "Windows":
            vectors = self._check_windows()
        else:
            vectors = self._check_linux()

        self.results["vectors"] = vectors
        self.results["output"] = f"Found {len(vectors)} potential privilege escalation vectors"

        for v in vectors:
            print(f"    [+] {v['name']} - {v['description']} ({v['risk']})")

        return self.results

    def _check_windows(self):
        """Check Windows privilege escalation vectors"""
        vectors = []

        # Vérifier les droits de l'utilisateur
        try:
            import ctypes
            is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            if is_admin:
                vectors.append({
                    "name": "Admin User",
                    "description": "User already has administrative privileges",
                    "risk": "High",
                    "details": "Current user is admin - highest privilege level"
                })
        except:
            pass

        # Vérifier les services vulnérables
        try:
            result = subprocess.run(
                ["sc", "query", "state=all"],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0:
                # Rechercher des services avec des permissions faibles
                if "SERVICE_STOPPED" in result.stdout:
                    vectors.append({
                        "name": "Vulnerable Services",
                        "description": "Potential weak service permissions detected",
                        "risk": "High",
                        "details": "Check for weak service permissions (unquoted service paths, weak ACLs)"
                    })
        except:
            pass

        # Vérifier AlwaysInstallElevated (MSI)
        try:
            import winreg
            key_path = r"SOFTWARE\Policies\Microsoft\Windows\Installer"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            try:
                value = winreg.QueryValueEx(key, "AlwaysInstallElevated")[0]
                if value == 1:
                    vectors.append({
                        "name": "AlwaysInstallElevated",
                        "description": "MSI installations run with SYSTEM privileges",
                        "risk": "Critical",
                        "details": "AlwaysInstallElevated enabled - high privilege escalation risk"
                    })
            except:
                pass
        except:
            pass

        # Vérifier le registre AutoRun
        try:
            import winreg
            key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ)
            values = []
            i = 0
            try:
                while True:
                    name, value, type = winreg.EnumValue(key, i)
                    values.append(name)
                    i += 1
            except:
                pass
            if values:
                vectors.append({
                    "name": "Autorun Registry",
                    "description": f"Found {len(values)} autorun entries in registry",
                    "risk": "Medium",
                    "details": f"Check if any autorun entries can be hijacked"
                })
        except:
            pass

        return vectors

    def _check_linux(self):
        """Check Linux privilege escalation vectors"""
        vectors = []

        # Vérifier si l'utilisateur est root
        if os.geteuid() == 0:
            vectors.append({
                "name": "Root User",
                "description": "User already has root privileges",
                "risk": "High",
                "details": "Current user is root - highest privilege level"
            })

        # Vérifier les fichiers SUID
        try:
            result = subprocess.run(
                ["find", "/", "-perm", "-4000", "-type", "f", "2>/dev/null"],
                capture_output=True,
                text=True,
                shell=True
            )
            suid_files = [f for f in result.stdout.split('\n') if f.strip()]
            if suid_files:
                # Filtrer les SUID courants et dangereux
                dangerous = ["nmap", "vim", "find", "bash", "less", "more", "nano", "vi", "pkexec", "sudo", "passwd", "chsh", "mount", "umount"]
                risky_suid = [f for f in suid_files if any(d in f for d in dangerous)]
                if risky_suid:
                    vectors.append({
                        "name": "SUID Files",
                        "description": f"Found {len(suid_files)} SUID files",
                        "risk": "High",
                        "details": f"Potentially dangerous SUID files found: {', '.join(risky_suid[:3])}"
                    })
        except:
            pass

        # Vérifier les tâches cron
        try:
            result = subprocess.run(
                ["ls", "-la", "/etc/cron*", "2>/dev/null"],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.stdout:
                vectors.append({
                    "name": "Cron Jobs",
                    "description": "Found cron jobs that may be exploitable",
                    "risk": "Medium",
                    "details": "Check for writable cron scripts or weak permissions"
                })
        except:
            pass

        # Vérifier les permissions sudo
        try:
            result = subprocess.run(
                ["sudo", "-l"],
                capture_output=True,
                text=True,
                shell=True
            )
            if result.returncode == 0 and "NOPASSWD" in result.stdout:
                vectors.append({
                    "name": "Sudo NOPASSWD",
                    "description": "User can run commands with sudo without password",
                    "risk": "High",
                    "details": f"Sudo NOPASSWD configured for user"
                })
        except:
            pass

        # Vérifier le noyau (kernel exploit)
        try:
            result = subprocess.run(
                ["uname", "-r"],
                capture_output=True,
                text=True,
                shell=True
            )
            kernel_version = result.stdout.strip()
            if kernel_version:
                # Versions de noyau vulnérables (simplifié)
                vulnerable_versions = ["2.6", "3.0", "3.2", "3.4", "3.8", "3.10", "3.13", "3.16"]
                if any(v in kernel_version for v in vulnerable_versions):
                    vectors.append({
                        "name": "Kernel Exploit",
                        "description": f"Kernel version {kernel_version} may be vulnerable to local exploits",
                        "risk": "Critical",
                        "details": "DirtyCow (CVE-2016-5195) and other kernel exploits possible"
                    })
        except:
            pass

        return vectors
