rm app.db
rm -rf db_repository
python -m app.database.db_create
python run.py