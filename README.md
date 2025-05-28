# DB_webshop

DB exam project - creating a webshop using 3 different databases in an appropriate manner.

### mysql setup

```
docker compose down
docker compose up --build -d
```

### Data insert with dump file

run the following file in mysql workbench:

```
/app/database/init/webshop_sql_dump.sql
```

### Data insert without dump file

```
cd app/database/init
python Cleaning_CSV.py
```

Run the following scripts to prepare for data insertion

```
mysql_creation_script.sql;
SQL_data_init.sql;
```

The final script has to be run for each of the chunks because of memory limits:

```
Data_import.sql;
```
