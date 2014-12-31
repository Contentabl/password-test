rm app.db
rm -rf db_repository
python -m app.database.db_create
echo "Creating random users"
python -m app.database.create_users
python run.py