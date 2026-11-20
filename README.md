# OpsBoard — DevOps Operations Dashboard

## Run locally (Windows PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open http://localhost:5000.

## API
- `GET /health` — application and SQLite health
- `GET /api/tasks` — list tasks; optional `status`, `category`, `search` query parameters
- `GET /api/stats` — dashboard statistics
- `POST /api/tasks` — create a task
- `PATCH /api/tasks/<id>` — update task fields
- `DELETE /api/tasks/<id>` — delete a task

Task data is stored in `tasks.db` using SQLite. The database is created automatically and seeded with sample DevOps tasks only when empty.

## Docker
```bash
docker build -t opsboard .
docker run --rm -p 5000:5000 -v opsboard-data:/app/data opsboard
```
For persistent Docker storage, set `DATABASE_PATH=/app/data/tasks.db` when running the container:
```bash
docker run --rm -p 5000:5000 -e DATABASE_PATH=/app/data/tasks.db -v opsboard-data:/app/data opsboard
```
