from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db_path = "/Users/air/Desktop/PR/Labs/LAB8/service1/s1database.db"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ElectroScooter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    battery_level = db.Column(db.Float, nullable=False)
    
    def __init__(self, name, battery_level):
        self.name = name
        self.battery_level = battery_level

if __name__ == '__main__':
    with app.app_context():
        # Create the tables
        db.create_all()
