cwd=$(pwd)
db_name=gunpla_db
backup_name=$(date +'%m-%d-%Y')-$db_name-backup.sql

# mkdir backups
pg_dump $db_name > $cwd/backups/$backup_name
psql postgres -f create_and_seed_db.sql
