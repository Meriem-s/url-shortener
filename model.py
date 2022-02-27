from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app import db

class Urls(db.Model):
    """
    #SQL Schema 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url_original TEXT NOT NULL,
    url_short TEXT DEFAULT NULL,
    creation_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    count_original INTEGER NOT NULL DEFAULT 0
    """
    
    id = db.Column(db.Integer, primary_key=True)
    url_original = db.Column(db.String(120))
    url_short = db.Column(db.String(120))
    creation_time = db.Column(db.DateTime)
    count_original = db.Column(db.Integer)

    #initiate new object in the constructor
    def __init__(self, url_original, url_short,creation_time, count_original):
        self.url_original = url_original
        self.url_short = url_short
        self.creation_time= creation_time
        self.count_original = count_original
        
    def __repr__(self):
        return f"Urls('{self.id}', '{self.url_original}', '{self.url_short}', '{self.creation_time}', {self.count_original})"

