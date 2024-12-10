# Intern Test Server

This is a simple api server made with [FastAPI](https://fastapi.tiangolo.com) framework and PostgreSQL database. Feel free to clone the repository and play with the code.

## Local Setup

Clone the Project

```
git clone git@github.com:AhsanShihab/Intern-Test-Server.git
```
or
```
git clone https://github.com/AhsanShihab/Intern-Test-Server.git
```

Create a virtual environment and activate the environment

```
cd Intern-Test-Server
python3 -m venv .venv  
source .venv/bin/activate 
```

Install required packages

```
pip3 install -r requirements.txt
```

You need a running PostgreSQL server. Run one locally, preferably in a docker container. You can run the following command to create a Postgres container:

```
docker run -d --name postgres-17 -p 5432:5432 -e POSTGRES_PASSWORD=password123 -e PGDATA=/var/lib/postgresql/data/pgdata -v ./.db_data:/var/lib/postgresql/data postgres:17
```

Then start the fast api server

```
uvicorn main:app --reload  
```

Check the documentation,
- [Redoc](http://127.0.0.1:8000/redoc)
- [Swagger](http://127.0.0.1:8000/docs)

