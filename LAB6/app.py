# app.py
from flask import Flask
from flasgger import Swagger

from models.database import db
from migrate_data import migrate_data


def create_app():
    app = Flask(__name__)

    # Configure to the postgresql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/psql_database'

    db.init_app(app)

    # Initialize Swagger
    Swagger(app)

    return app

if __name__ == "__main__":
    app = create_app()
    import routes

    # Migrate the data to the postgresql.
    app = migrate_data(app)

    app.run()