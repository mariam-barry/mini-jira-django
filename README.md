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

## Mode de fonctionnement :

SuperUser : L'administrateur crée un compte maître pour piloter toute la plateforme.

Création de Projet : Les projets sont créés et configurés directement dans l'interface Admin.

Assignation : L'administrateur nomme un Chef de Projet (PM) et ajoute les membres pour chaque projet.

Rôles : Chaque utilisateur reçoit un rôle spécifique qui limite ses droits et ses actions sur le site.

Visibilité : Un utilisateur voit uniquement les projets auxquels l'administrateur l'a rattaché.
