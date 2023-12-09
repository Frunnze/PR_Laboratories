# routes.py

from models.database import db
from models.electro_scooter import ElectroScooter
import requests


class CRUDScooter:
    def __init__(self, leader: bool, followers: dict=None):
        self.leader = leader
        if self.leader:
            self.followers = followers
    
    def create(self, data):
        # Validate and extract required parameters
        name = data['name']
        battery_level = data['battery_level']
        # Create a new Electro Scooter
        electro_scooter = ElectroScooter(name=name, battery_level=battery_level)
        # Add the Electro Scooter to the database
        db.session.add(electro_scooter)
        db.session.commit()

        if self.leader:
            for follower in self.followers:
                requests.post(f"http://{follower['host']}:{follower['port']}/api/electro-scooters",
                                json = data,
                                headers = {"Token" : "leader"})
                print("requests:", requests)


    def update(self, scooter_id, scooter, data):
        scooter.name = data.get('name', scooter.name)
        scooter.battery_level = data.get('battery_level', scooter.battery_level)
        db.session.commit()

        if self.leader:
            for follower in self.followers:
                requests.put(f"http://{follower['host']}:{follower['port']}/api/electro-scooters/{scooter_id}",
                                json = data,
                                headers = {"Token" : "leader"})
            
    
    def delete(self, scooter_id, scooter, password):
        db.session.delete(scooter)
        db.session.commit()

        if self.leader:
            for follower in self.followers:
                requests.delete(f"http://{follower['host']}:{follower['port']}/api/electro-scooters/{scooter_id}",
                                headers = {"Token" : "leader", "X-Delete-Password": password})