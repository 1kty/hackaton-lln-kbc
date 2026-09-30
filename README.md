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

Pour l’API chatbot, générez la base à l’emplacement par défaut :

```powershell
python seeder/seed_clients.py --count 100 --seed 42 --db seeder/clients.db
```

## Consulter la base

```powershell
python -m streamlit run db_viewer.py
```

Ouvrez ensuite l’adresse locale affichée dans le terminal (par défaut `http://localhost:8501`). Le viewer permet de rechercher les profils, filtrer par situation et canal préféré, puis consulter les signaux, besoins et recommandations d’un client.

## API chatbot

Copiez `backend/.env.example` vers `backend/.env` et renseignez `OPENAI_API_KEY` (optionnel : `OPENAI_MODEL`, `OPENAI_BASE_URL`, `DATABASE_PATH`).

```powershell
python -m pip install -r requirements.txt
copy backend\.env.example backend\.env
uvicorn backend.app.main:app --reload --port 8000
```

- `GET http://localhost:8000/health`
- `GET http://localhost:8000/api/customers/KBC-DEMO-000001`
- `POST http://localhost:8000/api/chat` avec `{ "message": "...", "client_id": "KBC-DEMO-000001", "history": [] }`
