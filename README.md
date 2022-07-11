# Intern Test Server

This is a simple api server made with [FastAPI](https://fastapi.tiangolo.com) framework and PostgreSQL database. Feel free to clone the repository and play with the code.

## Live Server

The server is Live at this url: https://intern-test-server.herokuapp.com

See the docs
- [Redoc](https://intern-test-server.herokuapp.com/redoc)
- [Swagger](https://intern-test-server.herokuapp.com/docs)

## Local Setup

Clone the Project

```
git clone git@github.com:AhsanShihab/Intern-Test-Server.git
```
or
```
git clone https://github.com/AhsanShihab/Intern-Test-Server.git
```

(Optional) Create a virtual environment and activate the environment

```
cd Intern-Test-Server
python3 -m venv venv  
source venv/bin/activate 
```

Install required packages

```
pip3 install -r requirements.txt
```

You need a running PostgreSQL server. Run one locally, preferably in a docker container, or in the cloud, then set the uri in the environment varibale `DB_URL`  or harcode it in 'database.py' file.

Then start the server

```
uvicorn main:app --reload  
```

Check the documentation,
- [Redoc](http://127.0.0.1:8000/redoc)
- [Swagger](http://127.0.0.1:8000/docs)

