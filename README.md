# 🔧 VulnForge — Exploit Framework for Authorized Testing

> ⚠️ **AVERTISSEMENT** — Cet outil est conçu exclusivement pour :
> - Des tests d'intrusion **autorisés** (pentests, Red Team)
> - La **formation** et la **recherche** en cybersécurité défensive
> - Des démonstrations d'impact dans un cadre **contractuel**
>
> **Toute utilisation sur un système sans autorisation écrite est ILLÉGALE.**
> L'auteur décline toute responsabilité en cas d'usage malveillant.

---

## 📖 Description

**VulnForge** est un framework d'exploitation modulaire pour les tests d'intrusion autorisés.

Il permet de :
- Scanner des ports et services
- Vérifier les vulnérabilités connues (CVE)
- Lancer des exploits (SMB, SSH, FTP, Web)
- Générer des payloads (reverse/bind shells)
- Détecter des vecteurs d'élévation de privilèges
- Générer des rapports complets (JSON + HTML)

---

## 🔐 Sécurité intégrée

L'exécution est **bloquée** sans un fichier d'autorisation :

1. Créer le fichier `vulnforge.token` à la racine
2. Écrire `VULNFORGE_AUTHORIZED` dedans

Sans ce fichier, le programme refuse de s'exécuter.

---

## 🧩 Modules (10)

| Module | Fonction |
|--------|----------|
| `port_scanner` | Scan TCP/UDP |
| `service_enum` | Énumération de services (SMB, SSH, FTP, HTTP, etc.) |
| `vuln_checker` | Vérification de vulnérabilités (CVE) |
| `exploit_smb` | Exploitation SMB (EternalBlue, SMBGhost) |
| `exploit_ssh` | Brute force SSH + exploitation |
| `exploit_ftp` | Brute force FTP + exploitation |
| `exploit_web` | Exploitation web (SQLi, XSS, LFI) |
| `privilege_escalation` | Détection d'élévation de privilèges (Windows/Linux) |
| `payload_generator` | Génération de payloads (reverse shell, bind shell) |
| `report` | Génération de rapports (JSON + HTML) |

---

## ⚙️ Installation

```bash
git clone https://github.com/theanonspider/VulnForge.git
cd VulnForge
pip install -r requirements.txt
```

---

## 🚀 Utilisation

### 1. Créer le token d'autorisation

```bash
echo "VULNFORGE_AUTHORIZED" > vulnforge.token
```

### 2. Exemples de commandes

```bash
# Scanner les ports d'une cible
python vulnforge.py scan -t 192.168.1.1 -p 1-1000

# Énumérer les services sur une cible
python vulnforge.py enum -t 192.168.1.1 -s all

# Vérifier les vulnérabilités (nécessite le JSON des services)
python vulnforge.py vuln_check -t 192.168.1.1 -s '[{"service":"smb","port":445}]'

# Lancer un exploit SMB
python vulnforge.py exploit -t 192.168.1.1 -e eternalblue

# Générer un payload reverse shell
python vulnforge.py generate_payload -p reverse --lhost 10.0.0.1 --lport 4444

# Détecter les vecteurs d'élévation de privilèges
python vulnforge.py priv_esc -t localhost

# Générer un rapport
python vulnforge.py report -o ./reports -f html
```

### 3. Voir toutes les commandes

```bash
python vulnforge.py --help
```

---

## 📄 Sortie

Tous les modules génèrent un rapport dans le dossier `reports/` :
- `vulnforge_report_<timestamp>.json` (données brutes)
- `vulnforge_report_<timestamp>.html` (visualisation)

---

## 🛠️ Compatibilité

| OS | Modules fonctionnels |
|----|----------------------|
| Windows 10/11 | ✅ Tous les modules |
| Linux | ✅ Tous les modules |
| macOS | ⚠️ Partiel (non testé) |

---

## ⚖️ Licence

Ce projet est fourni à des fins **exclusivement éducatives et défensives**.
Toute utilisation non autorisée est interdite.

---

## 👤 Auteur

Projet maintenu par **@theanonspider** — Pour la cybersécurité éthique. 🐺
