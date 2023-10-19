# init_db.py
from models.database import db
from models.electro_scooter import ElectroScooter


def init_database(app):
    """
    Creates the SQLite database, creates the necessary tables,
    and populates them with the sample data.
    """
    
    with app.app_context():
        # Create the database tables
        db.create_all()

    return app

if __name__ == "__main__":
    init_database()