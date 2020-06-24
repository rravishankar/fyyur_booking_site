from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate
from logging import Formatter, FileHandler

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.String(500))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    shows = db.relationship('Show', lazy=True, cascade="all, delete-orphan", backref='Venue')


    def __init__(self, name, city, state, address, phone, genres, image_link, website, facebook_link, seeking_talent=False, seeking_description=""):
      self.name = name
      self.city = city
      self.state = state
      self.address= address
      self.genres = genres
      self.phone = phone
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.website = website
      self.seeking_talent = seeking_talent
      self.seeking_description = seeking_description


    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.facebook_link} {self.website} {self.seeking_talent} {self.seeking_description}>'
    
    def detail(self):
        return{
            'id' :self.id,
            'name' :self.name,
            'genres' : self.genres.split('+'),
            'address' :self.address,
            'state' :self.state,
            'city' :self.city,
            'phone' :self.phone,
            'website' :self.website,
            'facebook_link':self.facebook_link,
            'seeking_talent' :self.seeking_talent,
            'description' :self.seeking_description,
            'image_link' :self.image_link
        }
    def short(self):
        return{
            'id':self.id,
            'name':self.name,
        }
    
    def long(self):
        print(self)
        return{
            'id' :self.id,
            'name' :self.name,
            'city' : self.city,
            'state' :self.state,
        }        
    
    def delete(self):
      db.session.delete(self)
      db.session.commit()


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(500)) #Changed to 500 from 120 as 120 may not be sufficient
    #Ideally genres and artist id can be a separate table with combination of both as private key and 
    #that table should be queried for the same. Here we'll store it separated by +
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    show_association = db.relationship('Show', lazy=True, cascade="all, delete-orphan", backref='Artist')

    def __init__(self, name, city, state, phone, genres, image_link, website, facebook_link, seeking_venue=False, seeking_description=""):
      self.name = name
      self.city = city
      self.state = state
      self.genres = genres
      self.phone = phone
      self.image_link = image_link
      self.facebook_link = facebook_link
      self.website = website
      self.seeking_venue = seeking_venue
      self.seeking_description = seeking_description


    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.genres} {self.image_link} {self.facebook_link} {self.facebook_link} {self.website} {self.seeking_venue} {self.seeking_description}>'

    def detail(self):
        return{
            'id' :self.id,
            'name' :self.name,
            'genres' : self.genres.split('+'),
            'state' :self.state,
            'city' :self.city,
            'phone' :self.phone,
            'website' :self.website,
            'facebook_link':self.facebook_link,
            'seeking_venue' :self.seeking_venue,
            'description' :self.seeking_description,
            'image_link' :self.image_link
        }
    def short(self):
        return{
            'id':self.id,
            'name':self.name,
        }

    def long(self):
        print(self)
        return{
            'id' :self.id,
            'name' :self.name,
            'city' : self.city,
            'state' :self.state,
        }

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'Show'
    #Ref https://stackoverflow.com/questions/30406808/flask-sqlalchemy-difference-between-association-model-and-association-table-fo
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    show_time = db.Column(db.DateTime(timezone=True), primary_key=True) #Actually better is nullable=False, but should be true by default as it's PK

    def __init__(self,artist_id, venue_id, show_time):
      self.artist_id = artist_id
      self.venue_id = venue_id
      self.show_time = show_time


    def __repr__(self):
        return f'<Show {self.artist_id} {self.venue_id} {self.show_time}>'
