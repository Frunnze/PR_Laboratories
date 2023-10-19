from models.database import db
from models.electro_scooter import ElectroScooter

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def migrate_data(app):

    #  Get the Flask app context.
    with app.app_context():

        # Set the path of the source and target database for migration.
        db_path = "instance/your_database.db"
        source_db = f'sqlite:///{db_path}'
        target_db = 'postgresql://postgres:123@localhost/psql_database'

        # Create the SQLAlchemy engines.
        source_engine = create_engine(source_db)
        target_engine = create_engine(target_db)

        # Create a session class.
        Session = sessionmaker(bind=source_engine)
        session = Session()

        # Create the database tables for the ElectroScooter model in the target database
        ElectroScooter.metadata.create_all(target_engine)

        # Go through all records in the source database and copy them to the target db
        for scooter in session.query(ElectroScooter).all():
            scooter_copy = ElectroScooter(name=scooter.name, battery_level=scooter.battery_level)
            db.session.add(scooter_copy)

        # Commit the changes.
        db.session.commit()

    return app