# hackaton-lln-kbc

## Générer les données

Les profils sont synthétiques. Le seeder crée `clients.json` et `clients.db` à la racine du projet. SQLite est intégré à Python; seule l’interface de consultation nécessite Streamlit.

```powershell
python -m pip install -r requirements.txt
python seed_clients.py --count 100 --seed 42
```

Pour choisir les fichiers de sortie :

```powershell
python seed_clients.py --count 100 --seed 42 --output clients.json --db clients.db
```

## Consulter la base

```powershell
python -m streamlit run db_viewer.py
```

Ouvrez ensuite l’adresse locale affichée dans le terminal (par défaut `http://localhost:8501`). Le viewer permet de rechercher les profils, filtrer par situation et canal préféré, puis consulter les signaux, besoins et recommandations d’un client.
