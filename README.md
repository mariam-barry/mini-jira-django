# Mini-Jira en Django

Projet de Licence 3 - ISI Dakar.

## Architecture
Le projet est découpé en 5 applications modulaires :
- **Accounts** : Gestion des utilisateurs personnalisés.
- **Projects** : Gestion des projets et des membres.
- **Tickets** : Cœur du système (CRUD, Temps passé).
- **Sprints** : Planification agile.
- **Audit** : Historique complet des transitions de statut.

## Installation
1. `pip install -r requirements.txt`
2. `python manage.py migrate`
3. `python manage.py runserver`
