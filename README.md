# 🔧 VulnForge — Exploit Framework

> ⚠️ **AVERTISSEMENT** — Cet outil est conçu exclusivement pour :
> - Des tests d'intrusion **autorisés**
> - La **formation** et la **recherche** en cybersécurité
>
> **Toute utilisation non autorisée est ILLÉGALE.**

## 📖 Description

VulnForge est un framework d'exploitation modulaire pour les tests d'intrusion autorisés.

## 🔐 Sécurité

Un token est obligatoire pour exécuter l'outil :
```bash
echo "VULNFORGE_AUTHORIZED" > vulnforge.token

🚀 Utilisation
bash

python vulnforge.py scan -t 192.168.1.1 -p 1-1000
python vulnforge.py exploit -t 192.168.1.1 -e eternalblue
