(cd app/db && alembic upgrade head)
python app/main.py --load cities
python app/main.py --load conditions
crond -f -L 2