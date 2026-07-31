"""
VulnForge Module : Report Generator
Generate comprehensive reports (JSON, HTML, PDF).
"""

import json
import os
from datetime import datetime

class ReportModule:
    def __init__(self, output_dir="./reports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = {
            "tool": "VulnForge",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "modules": []
        }

    def add_module_result(self, module_name, module_result):
        """Ajoute les résultats d'un module au rapport."""
        self.results["modules"].append({
            "module": module_name,
            "timestamp": datetime.now().isoformat(),
            "data": module_result
        })

    def generate_json(self, filename=None):
        """Génère un rapport JSON."""
        if not filename:
            filename = f"vulnforge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"[+] JSON report generated: {filepath}")
        return filepath

    def generate_html(self, filename=None):
        """Génère un rapport HTML lisible."""
        if not filename:
            filename = f"vulnforge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = os.path.join(self.output_dir, filename)

        # Compter les actions/vulnérabilités
        total_findings = 0
        for module in self.results["modules"]:
            data = module["data"]
            if "vulnerabilities" in data:
                total_findings += len(data["vulnerabilities"])
            elif "open_ports" in data:
                total_findings += len(data["open_ports"])
            elif "valid_credentials" in data:
                total_findings += len(data["valid_credentials"])
            elif "vectors" in data:
                total_findings += len(data["vectors"])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VulnForge Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: #0a0a0f; color: #ccc; font-family: 'Courier New', monospace; padding: 40px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #ff6b35; font-size: 2em; border-bottom: 2px solid #332211; padding-bottom: 15px; margin-bottom: 30px; }}
        h2 {{ color: #ff6b35; font-size: 1.2em; margin-top: 30px; margin-bottom: 15px; border-left: 3px solid #ff6b35; padding-left: 15px; }}
        .meta {{ background: #0f0f1a; border: 1px solid #1a1a2e; padding: 20px; margin-bottom: 20px; }}
        .meta span {{ color: #666; }}
        .module {{ background: #0f0f1a; border: 1px solid #1a1a2e; padding: 20px; margin-bottom: 20px; }}
        .module-title {{ color: #ff6b35; font-size: 1.1em; margin-bottom: 10px; }}
        .finding {{ color: #aaa; padding: 5px 0; border-bottom: 1px solid #111; }}
        .finding:last-child {{ border-bottom: none; }}
        .critical {{ color: #ff0000; }}
        .high {{ color: #ff6b35; }}
        .medium {{ color: #ffa500; }}
        .low {{ color: #ffd700; }}
        .count {{ color: #27ae60; font-weight: bold; }}
        .footer {{ margin-top: 40px; color: #444; text-align: center; font-size: 0.8em; border-top: 1px solid #1a1a2e; padding-top: 20px; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 0.7em; font-weight: bold; }}
        .badge-critical {{ background: #ff0000; color: #fff; }}
        .badge-high {{ background: #ff6b35; color: #fff; }}
        .badge-medium {{ background: #ffa500; color: #fff; }}
        .badge-low {{ background: #ffd700; color: #000; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 VulnForge — Exploit Report</h1>
        
        <div class="meta">
            <div><span>Generated:</span> {self.results['timestamp']}</div>
            <div><span>Tool:</span> {self.results['tool']} v{self.results['version']}</div>
            <div><span>Total findings:</span> <span class="count">{total_findings}</span></div>
            <div><span>Modules executed:</span> <span class="count">{len(self.results['modules'])}</span></div>
        </div>

        <h2>📋 Module Results</h2>
"""

        for module in self.results["modules"]:
            module_name = module["module"]
            data = module["data"]
            
            # Compter les findings
            findings = []
            if "vulnerabilities" in data:
                findings = data["vulnerabilities"]
            elif "open_ports" in data:
                findings = data["open_ports"]
            elif "valid_credentials" in data:
                findings = data["valid_credentials"]
            elif "vectors" in data:
                findings = data["vectors"]

            html += f"""
        <div class="module">
            <div class="module-title">▪ {module_name.upper()} <span style="color: #666;">({len(findings)} findings)</span></div>
"""

            if findings and len(findings) > 0:
                for finding in findings[:20]:
                    if isinstance(finding, dict):
                        name = finding.get("name") or finding.get("cve") or finding.get("service") or finding.get("username") or finding.get("type") or "Finding"
                        desc = finding.get("description") or finding.get("details") or finding.get("output") or finding.get("evidence") or ""
                        risk = finding.get("risk", "").lower()
                        risk_badge = ""
                        if risk == "critical":
                            risk_badge = '<span class="badge badge-critical">CRITICAL</span>'
                        elif risk == "high":
                            risk_badge = '<span class="badge badge-high">HIGH</span>'
                        elif risk == "medium":
                            risk_badge = '<span class="badge badge-medium">MEDIUM</span>'
                        elif risk == "low":
                            risk_badge = '<span class="badge badge-low">LOW</span>'
                        html += f'            <div class="finding">→ {name} {risk_badge} - {desc[:100]}</div>\n'
                    else:
                        html += f'            <div class="finding">→ {str(finding)[:100]}</div>\n'
                
                if len(findings) > 20:
                    html += f'            <div class="finding" style="color: #666;">... and {len(findings) - 20} more</div>\n'
            else:
                html += '            <div class="finding" style="color: #666;">No findings</div>\n'

            html += f"""
        </div>
"""

        html += f"""
        <div class="footer">
            VulnForge v1.0.0 — Exploit Framework<br>
            Generated on {self.results['timestamp']}
        </div>
    </div>
</body>
</html>"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"[+] HTML report generated: {filepath}")
        return filepath

    def generate_pdf(self, filename=None):
        """Génère un rapport PDF (nécessite weasyprint ou autre)."""
        # Pour l'instant, on génère juste un HTML et on indique la conversion
        print("[!] PDF generation requires additional setup (weasyprint or similar)")
        print("    Pour l'instant, utilisez le rapport HTML et convertissez-le en PDF manuellement.")
        return None
