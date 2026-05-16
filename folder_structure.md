```
base/
  ├── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py           # Application entry point
    │   ├── config.py         # Environment variables & DB settings
    │   ├── database.py       # Database engine/pool setup
    │   ├── models.py         # SQLAlchemy/SQLModel definitions (Notes table)
    │   ├── routes/           # API endpoints (e.g., notes.py, auth.py)
    │   └── services/         # Business logic (e.g., embedding generation)
    ├── pyproject.toml
    ├── uv.lock
    └── ...
```
