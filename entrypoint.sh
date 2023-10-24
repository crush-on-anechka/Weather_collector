cd app/db
alembic upgrade head
cd ../..
python app/main.py --start program
