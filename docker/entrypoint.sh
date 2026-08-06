#!/bin/sh
set -e

echo "Waiting for database..."
python - <<'PY'
import os, time
import psycopg

host = os.environ.get("DB_HOST", "db")
port = os.environ.get("DB_PORT", "5432")
user = os.environ.get("DB_USER", "cafecore")
password = os.environ.get("DB_PASSWORD", "cafecore")
dbname = os.environ.get("DB_NAME", "cafecore")

for i in range(30):
    try:
        with psycopg.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname,
            connect_timeout=3,
        ):
            print("Database is ready.")
            break
    except Exception as exc:
        print(f"DB not ready ({i+1}/30): {exc}")
        time.sleep(2)
else:
    raise SystemExit("Database did not become ready in time.")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

if [ "${RUN_SEED:-0}" = "1" ]; then
  python manage.py seed_demo || true
fi

exec "$@"
