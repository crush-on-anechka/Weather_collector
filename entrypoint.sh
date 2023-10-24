(cd app/db && alembic upgrade head)
python app/main.py --start program
