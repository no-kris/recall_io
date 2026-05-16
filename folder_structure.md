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
  ├── frontend/src/
    ├── assets/          # Static files (images, icons)
    ├── components/      # Reusable UI elements (Buttons, Inputs, Cards)
    ├── features/        # Feature-based logic (Self-contained)
    │   ├── auth/        # Auth forms, context, or hooks
    │   └── notes/       # Note saving form, search bar, list items
    ├── hooks/           # Shared React hooks (e.g., useAuth, useDebounce)
    ├── services/        # API calls to your backend (e.g., api.js)
    ├── App.jsx          # Root component & routing
    └── main.jsx         # App entry point
```
