# DB_webshop

DB exam project - creating a webshop using 3 different databases in an appropriate manner.

```
docker compose down
docker compose up --build -d
```

### mysql setup

### Data insert with dump file

run the following file in mysql workbench:

```
webshop_sql_dump2.sql
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
