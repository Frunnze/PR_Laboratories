# app.py
from flask import Flask
from flasgger import Swagger
import time
import random

from models.database import db
from crud import CRUDScooter
from raft import RAFTFactory


def create_app():
    app = Flask(__name__)
    # Access the DB
    db_path = "/Users/air/Desktop/PR/Labs/LAB8/service2/s2database.db"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    db.init_app(app)
    # Initialize swagger
    Swagger(app)
    return app

if __name__ == "__main__":
    service_info = {
        "host" : "127.0.0.1",
        "port" : 8001,
        "leader" : None
    }

    # Election
    raft = RAFTFactory(service_info)
    raft.election()
    time.sleep(random.randint(1,3))
    if raft.role == "leader":
        service_info["leader"] = True
    else:
        service_info["leader"] = False

    # Create the CRUD object.
    crud = CRUDScooter(service_info["leader"], raft.followers)

    # Starting the server.
    app = create_app()
    import endpoints
    app.run(
        host = service_info["host"],
        port = service_info["port"]
    )