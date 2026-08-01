# 🔧 VulnForge — Exploit Tool

> ⚠️ **AVERTISSEMENT** — Usage exclusivement éducatif et défensif.  
> Toute utilisation non autorisée est **ILLÉGALE** et engage votre responsabilité.

---

## 📖 Pourquoi VulnForge ?

**VulnForge** est un framework d’exploitation modulaire pour les tests d’intrusion.  
Il couvre toute la chaîne : scan, énumération, vulnérabilités, exploitation, payloads, rapport.

---

## 🧩 Modules (10)

| Module | Fonction |
|--------|----------|
| `port_scanner` | Scan de ports TCP |
| `service_enum` | Énumération de services (SMB, SSH, FTP, HTTP) |
| `vuln_checker` | Vérification de vulnérabilités (CVE) |
| `exploit_smb` | Exploitation SMB (EternalBlue) |
| `exploit_ssh` | Brute force SSH |
| `exploit_ftp` | Brute force FTP |
| `exploit_web` | SQLi, XSS, LFI |
| `privilege_escalation` | Détection d’élévation |
| `payload_generator` | Génération de payloads (reverse/bind) |
| `report` | Rapports JSON + HTML |

---

## 🔐 Sécurité

Un token est obligatoire pour exécuter l'outil :

```bash
echo "VULNFORGE_AUTHORIZED" > vulnforge.token
```

---

## ⚙️ Installation

```bash
git clone https://github.com/theanonspider/VulnForge.git
cd VulnForge
pip install -r requirements.txt
echo "VULNFORGE_AUTHORIZED" > vulnforge.token
```

---

## 🚀 Exemples d’utilisation

```bash
# 1. Scan de ports
python vulnforge.py scan -t 192.168.1.1 -p 1-1000

# 2. Exploitation SMB
python vulnforge.py exploit -t 192.168.1.1 -e eternalblue

# 3. Génération de payload
python vulnforge.py generate-payload -p reverse --lhost 10.0.0.1 --lport 4444
```

---

## 📄 Sortie

Rapports dans `reports/` : **JSON + HTML**.

---

## ⚖️ Licence

Usage éducatif et défensif uniquement.

---

## 👤 Auteur

**@theanonspider** — Cybersécurité éthique. 🐺
