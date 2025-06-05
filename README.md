# DB_webshop

_By Pelle Vedsmand and Nicolai Rosendahl_

DB exam project - creating a webshop using 3 different databases in an appropriate manner.
This project uses the following databases:

- Mysql
- Mongodb
- Redis

### Setup of the containers

\***_Note all of the commands should be run from the root of the project!_**

Firstly the containers have to be setup. This is achieved by running the following commands to build the correct container setup:

```
docker compose down
docker compose up --build -d
```

### Mysql setup

The Mysql data and structure is saved in a "dump file".
Firstly connect to your mysql db that is spun up by the docker container on `7003:3306`
To insert the tables, procedures, triggers and data, execute the following file in mysql workbench:

```
mysql_creation_script.sql
```

### Using the Streamlit application

The docker container should have spun up a streamlit application on port 8501

```
http://localhost:8501/
```

<br> 
<br> 
<br> 
<br>

### "If no Docker container appears"

_If for some reason the streamlit application does not launch correctly, you can run the following command to spin up another:
`docker exec - it python-app streamlit run streamlit_app/start.py`_
