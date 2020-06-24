#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
# from flask_wtf import Form
from flask_wtf import FlaskForm
from forms import *
from flask_migrate import Migrate
from pytz import timezone
from tzlocal import get_localzone 
from sqlalchemy import func
from models import Artist, Venue, Show, db, app




# At the moment code doesn't use app.logger for logging that can be done later as there are too many
# prints in use already TBD 


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  query = db.session.query(Venue.id, Venue.name, Venue.state, Venue.city, func.count(Show.venue_id))
  # query = query.join(Show).order_by(Venue.state, Venue.city).group_by(Venue.name, Venue.state, Venue.city)
  query = query.order_by(Venue.state, Venue.city).group_by(Venue.id, Venue.name, Venue.state, Venue.city)
  query = query.all()
  
  
  # for row in query:
  #   # print(row)
  #   # print(type(row))
  #   pass
  # print("***End of print..")

  prev_state = ""
  prev_city = ""
  data = []

  for venue in query:
    venue_data = {
      "id": venue[0],
      "name": venue[1],
      "num_upcoming_shows": venue[4],
    }
    # print("Got venue data", venue_data)
    if prev_state == venue[2] and prev_city == venue[3]:
      data[len(data)-1]["venues"].append(venue_data)
    else:
      data.append({
        "city": venue[3],
        "state": venue[2],
        "venues": [venue_data]
      })
      prev_state = venue[2]
      prev_city = venue[3]

    # if venue
    
  # print("Final data string", data)
  # if venue.city == prev_city and venue.state = prev_state:

  # data=[{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]
  return render_template('pages/venues.html', areas=data);

# @app.route('/venues')
# def venues():
#   # TODO: replace with real venues data.
#   #       num_shows should be aggregated based on number of upcoming shows per venue.
#   query = db.session.query(Venue.id, Venue.name, Venue.state, Venue.city, func.count(Show.venue_id))
#   # query = query.join(Show).order_by(Venue.state, Venue.city).group_by(Venue.name, Venue.state, Venue.city)
#   query = query.join(Show).order_by(Venue.state, Venue.city).group_by(Venue.id, Venue.name, Venue.state, Venue.city)
#   print(type(Show.show_time))
#   query = query.filter(Show.show_time > datetime.now()).all()
  
  
#   for row in query:
#     print(row)
#     print(type(row))
#   print("***End of print..")
#   prev_state = ""
#   prev_city = ""
#   data = []

#   for venue in query:
#     venue_data = {
#       "id": venue[0],
#       "name": venue[1],
#       "num_upcoming_shows": venue[4],
#     }
#     print("Got venue data", venue_data)
#     if prev_state == venue[2] and prev_city == venue[3]:
#       data[len(data)-1]["venues"].append(venue_data)
#     else:
#       data.append({
#         "city": venue[3],
#         "state": venue[2],
#         "venues": [venue_data]
#       })
#       prev_state = venue[2]
#       prev_city = venue[3]

#     # if venue
    
#   print("Final data string", data)
#   # if venue.city == prev_city and venue.state = prev_state:

#   # data=[{
#   #   "city": "San Francisco",
#   #   "state": "CA",
#   #   "venues": [{
#   #     "id": 1,
#   #     "name": "The Musical Hop",
#   #     "num_upcoming_shows": 0,
#   #   }, {
#   #     "id": 3,
#   #     "name": "Park Square Live Music & Coffee",
#   #     "num_upcoming_shows": 1,
#   #   }]
#   # }, {
#   #   "city": "New York",
#   #   "state": "NY",
#   #   "venues": [{
#   #     "id": 2,
#   #     "name": "The Dueling Pianos Bar",
#   #     "num_upcoming_shows": 0,
#   #   }]
#   # }]
#   return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():

  venue_query = Venue.query.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))
  venue_list = list(map(Venue.short, venue_query)) 
  response = {
    "count":len(venue_list),
    "data": venue_list
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  # return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

def get_artist_details_for_venue(artist_id, artist_name, artist_image_link, start_time):
  return {
    'artist_id' :artist_id,
    'artist_name' :artist_name,
    'artist_image_link' :artist_image_link,
    'start_time' :start_time + 'Z' 
  }
    

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  #start of code

  #start first code
  # venues = Venue.query.all()
  # for venue in venues:
  #   print("Got venue", venue)
  #   dt_unware = datetime.now()
  #   localtz = get_localzone()
  #   dt_aware = localtz.localize(dt_unware)
  #   shows_before = Show.query.filter(Show.show_time < dt_aware).filter(Show.venue_id == venue.id).all()
  #   num_shows_before = len(shows_before)
  #   # artists_before = shows_before.join(Artist).order_by(Artist.id)
    
  #   # print("Got {} past show(s) for venue {}:{}\n Got artists: artist".format(num_shows_before, venue.name, shows_before))
  #   shows_after = Show.query.filter(Show.show_time >= dt_aware).filter(Show.venue_id == venue.id).all()
  #   num_shows_after = len(shows_after)
  #   print("Got {} upcoming show(s) for venue {}:{}".format(num_shows_after, venue.name, shows_after))
  #end first code
  final_string = ""
  venue = Venue.query.get(venue_id)
  if venue:
    # print("Got venue {} for id {}".format(venue, venue.id))

    # Get current time with timezone
    dt_unware = datetime.now()
    localtz = get_localzone()
    dt_aware = localtz.localize(dt_unware)

    shows_before = Show.query.order_by(Show.show_time).filter(Show.show_time < dt_aware).filter(Show.venue_id == venue.id).all()
    num_shows_before = len(shows_before)

    shows_after = Show.query.order_by(Show.show_time).filter(Show.show_time >= dt_aware).filter(Show.venue_id == venue.id).all()
    num_shows_after = len(shows_after)
    
    venue_details = Venue.detail(venue)

    past_shows = []
    upcoming_shows = []
    for show in shows_before:
      artist = Artist.query.get(show.artist_id)
      show_time_no_tz = show.show_time.replace(tzinfo=None)
      # print("Object type is ", type(show_time_no_tz), show_time_no_tz)
      artist_details = get_artist_details_for_venue(show.artist_id,artist.name,artist.image_link,show_time_no_tz.isoformat())
      
      past_shows.append(artist_details)
      
    for show in shows_after:
      artist = Artist.query.get(show.artist_id)
      show_time_no_tz = show.show_time.replace(tzinfo=None)
      artist_details = get_artist_details_for_venue(show.artist_id,artist.name,artist.image_link,show_time_no_tz.isoformat())
      upcoming_shows.append(artist_details)

    # print("Got {} past show(s) for venue {}:{}\n".format(num_shows_before, venue.name, past_shows))
    final_json = venue.detail()
    final_json['past_shows'] = past_shows
    final_json['past_shows_count'] = num_shows_before
    final_json['upcoming_shows'] = upcoming_shows
    final_json['upcoming_shows_count'] = num_shows_after
    # print("Got final string", final_json)
    return render_template('pages/show_venue.html', venue=final_json)

  return render_template('errors/404.html')


  
  #end of code

  #original code

  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  # return render_template('pages/show_venue.html', venue=data)
  
#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  seeking_venue = False

  data = VenueForm(request.form)

  valid_form = data.validate()
  # print("create_venue_submission:Got form validate", valid_form)
  if valid_form == False:
    print(data.errors)
    flash('An error occurred - form field(s) not valid. Venue ' + request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


  try:
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # print("Got data from request", request.form.getlist('genres'))
    
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    address = request.form['address']
    phone = request.form['phone']
    genres_list = request.form.getlist('genres')
    genre_string = ""
    append_string = ""
    for genre in genres_list:
      genre_string = genre_string + append_string + genre
      append_string = "+"
    # print("Got final genre string", genre_string)
    # print("Got seeking_description string", request.form['seeking_description'])
    
    
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    # seeking_venue = request.form['seeking_venue']
    seeking_talent = False
    if "seeking_talent" in request.form and request.form['seeking_talent'] == "y":
      seeking_talent = True
    # print("Setting seeking_venue ", seeking_talent)
    seeking_description = request.form['seeking_description']
    venue = Venue(name=name,
    city=city,
    state=state,
    address=address,
    phone=phone,
    genres = genre_string,
    image_link = image_link,
    facebook_link = facebook_link,
    website = website,
    seeking_talent = seeking_talent,
    seeking_description = seeking_description
    )
    # print("Venue", venue)
    db.session.add(venue)
    db.session.commit()
  except expression as identifier:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    # abort(400)
  else:
    flash('Venue ' + request.form['name'] + ' was successfully listed!')



  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  #   TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  print("delete_venue:Got to delete venue!!")
  try:
    #NOTE: Need to do this as cascade on delete option is not working the way it is probably supposed to,
    # so deleting this Venue from Show table first. We need to workaround
    # Ref @Alex's comment at https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete#:~:text=delete()%20(which%20doesn't,not%20all%20databases%20support%20it). 
    #For now removing from Show table and then deleting from Venue
    #This may need to be reworked and optiimzed for performance TBD
    #Delete has been tested using POSTMAN (sending the DELETE request with http://localhost:5000/venues/<VENUE_ID>)
    Show.query.filter_by(venue_id=venue_id).delete()
    
    # print("delete_venue:Deleted venues from Show table")
    Venue.query.filter_by(id=venue_id).delete()
    # print("delete_venue:Deleted venues from Venue table")

    # print("Delete got", v, type(v))
    db.session.commit()
    # print("delete_venue:Commited!")
  except Exception as e:
    print("delete_venue:Got exception", e)
    db.session.rollback()
  finally:
    db.session.close()

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]

  artist_list = Artist.query.all()
  artist_data = []
  for artist in artist_list:
    artist_data.append({
    "id": artist.id,
    "name": artist.name,    
    })

  # return render_template('pages/artists.html', artists=data)
  return render_template('pages/artists.html', artists=artist_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  artist_query = Artist.query.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))
  artist_list = list(map(Artist.short, artist_query)) 
  response = {
    "count":len(artist_list),
    "data": artist_list
  }
  # print(response)
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  # return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

def get_venue_details_for_artist(venue_id, venue_name, venue_image_link, start_time):
  return {
    'venue_id' :venue_id,
    'venue_name' :venue_name,
    'venue_image_link' :venue_image_link,
    'start_time' :start_time + 'Z' 
  }


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):  
  
  artist = Artist.query.get(artist_id)
  if artist:
    print("Got artist {} for id {}".format(artist, artist.id))
    pass

    # Get current time with timezone
    dt_unware = datetime.now()
    localtz = get_localzone()
    dt_aware = localtz.localize(dt_unware)

    shows_before = Show.query.order_by(Show.show_time).filter(Show.show_time < dt_aware).filter(Show.artist_id == artist.id).all()
    num_shows_before = len(shows_before)

    shows_after = Show.query.order_by(Show.show_time).filter(Show.show_time >= dt_aware).filter(Show.artist_id == artist.id).all()
    num_shows_after = len(shows_after)
    
    artist_details = Artist.detail(artist)

    past_shows = []
    upcoming_shows = []
    for show in shows_before:
      venue = Venue.query.get(show.venue_id)
      show_time_no_tz = show.show_time.replace(tzinfo=None)
      # print("Object type is ", type(show_time_no_tz), show_time_no_tz)
      # artist_details = get_artist_details_for_venue(show.artist_id,artist.name,artist.image_link,show_time_no_tz.isoformat())
      venue_details = get_venue_details_for_artist(show.venue_id, venue.name, venue.image_link,show_time_no_tz.isoformat())
      past_shows.append(venue_details)
      
    for show in shows_after:
      venue = Venue.query.get(show.venue_id)
      show_time_no_tz = show.show_time.replace(tzinfo=None)
      venue_details = get_venue_details_for_artist(show.venue_id, venue.name, venue.image_link,show_time_no_tz.isoformat())  
      upcoming_shows.append(venue_details)

    # print("Got {} past show(s) for artist {}:{}\n".format(num_shows_before, artist.name, past_shows))
    final_json = artist.detail()
    final_json['past_shows'] = past_shows
    final_json['past_shows_count'] = num_shows_before
    final_json['upcoming_shows'] = upcoming_shows
    final_json['upcoming_shows_count'] = num_shows_after
    # print("Got final string for artist:", final_json)
    return render_template('pages/show_artist.html', artist=final_json)

  return render_template('errors/404.html')

  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_data = Artist.query.get(artist_id)
  if artist_data:
    artist_details = Artist.detail(artist_data)
    form.name.data = artist_details["name"]
    form.genres.data = artist_details["genres"]
    form.city.data = artist_details["city"]
    form.state.data = artist_details["state"]
    form.phone.data = artist_details["phone"]
    form.website.data = artist_details["website"]
    form.facebook_link.data = artist_details["facebook_link"]
    form.seeking_venue.data = artist_details["seeking_venue"]
    form.seeking_description.data = artist_details["description"]
    form.image_link.data = artist_details["image_link"]
    return render_template('forms/edit_artist.html', form=form, artist=artist_details)
  return render_template('errors/404.html')

  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm(request.form)
  artist_data = Artist.query.get(artist_id)
  # print("edit_artist_submission:Got artist ", artist_data)
  valid_form = form.validate()
  # print("edit_artist_submission:Got form validate", valid_form)
  if valid_form == False:
    print(form.errors)
  if valid_form and artist_data:
    artist_data.name = request.form['name']
    artist_data.city = request.form['city']
    artist_data.state = request.form['state']
    artist_data.phone = request.form['phone']
    genres_list = request.form.getlist('genres')
    genre_string = ""
    append_string = ""
    for genre in genres_list:
      genre_string = genre_string + append_string + genre
      append_string = "+"
    # print("Got final genre string", genre_string)
    artist_data.genres = genre_string
    # print("Got seeking_description string", request.form['seeking_description'])
    
    
    artist_data.image_link = request.form['image_link']
    artist_data.facebook_link = request.form['facebook_link']
    artist_data.website = request.form['website']
    # seeking_venue = request.form['seeking_venue']
    seeking_venue = False
    if "seeking_venue" in request.form and request.form['seeking_venue'] == "y":
      seeking_venue = True
    # print("Setting seeking_venue ", seeking_venue)
    artist_data.seeking_venue = seeking_venue
    artist_data.seeking_description = request.form['seeking_description']
    db.session.commit()
      
      

  
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_data = Venue.query.get(venue_id)
  if venue_data:
    venue_details = Venue.detail(venue_data)
    form.name.data = venue_details["name"]
    form.genres.data = venue_details["genres"]
    form.city.data = venue_details["city"]
    form.state.data = venue_details["state"]
    form.address.data = venue_details["address"]
    form.phone.data = venue_details["phone"]
    form.website.data = venue_details["website"]
    form.facebook_link.data = venue_details["facebook_link"]
    form.seeking_talent.data = venue_details["seeking_talent"]
    form.seeking_description.data = venue_details["description"]
    form.image_link.data = venue_details["image_link"]
    return render_template('forms/edit_venue.html', form=form, venue=venue_details)
  return render_template('errors/404.html')


  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # # TODO: populate form with values from venue with ID <venue_id>
  # return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  form = VenueForm(request.form)
  venue_data = Venue.query.get(venue_id)
  # print("edit_venue_submission:Got venue ", venue_data, type(venue_data))
  valid_form = form.validate()
  # print("Got form validate", valid_form)
  if valid_form == False:
    print(form.errors)

  if valid_form and venue_data:
    venue_data.name = request.form['name']
    venue_data.city = request.form['city']
    venue_data.state = request.form['state']
    venue_data.address = request.form['address']    
    venue_data.phone = request.form['phone']
    genres_list = request.form.getlist('genres')
    genre_string = ""
    append_string = ""
    for genre in genres_list:
      genre_string = genre_string + append_string + genre
      append_string = "+"
    # print("Got final genre string", genre_string)
    venue_data.genres = genre_string
    # print("Got seeking_description string", request.form['seeking_description'])
    
    
    venue_data.image_link = request.form['image_link']
    venue_data.facebook_link = request.form['facebook_link']
    venue_data.website = request.form['website']
    # seeking_venue = request.form['seeking_venue']
    seeking_talent = False
    if "seeking_talent" in request.form and request.form['seeking_talent'] == "y":
      seeking_talent = True
    # print("Setting seeking_talent ", seeking_talent)
    venue_data.seeking_talent = seeking_talent
    venue_data.seeking_description = request.form['seeking_description']
    db.session.commit()

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  seeking_venue = False
  data = ArtistForm(request.form)

  
  valid_form = data.validate()
  # print("create_artist_submission:Got form validate", valid_form)
  if valid_form == False:
    print(data.errors)
    flash('An error occurred - form field(s) not valid. Artist ' + request.form['name'] + ' could not be listed.')
    return render_template('pages/home.html')


  try:
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead
    # TODO: modify data to be the data object returned from db insertion
    # print("Got data from form", data.genres)
    # print("Got data from request", request.form.getlist('genres'))
    
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres_list = request.form.getlist('genres')
    genre_string = ""
    append_string = ""
    for genre in genres_list:
      genre_string = genre_string + append_string + genre
      append_string = "+"
    # print("Got final genre string", genre_string)
    # print("Got seeking_description string", request.form['seeking_description'])
    
    
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    # seeking_venue = request.form['seeking_venue']
    if "seeking_venue" in request.form and request.form['seeking_venue'] == "y":
      seeking_venue = True
    # print("Setting seeking_venue ", seeking_venue)
    seeking_description = request.form['seeking_description']
    artist = Artist(name=name,
    city=city,
    state=state,
    phone=phone,
    genres = genre_string,
    image_link = image_link,
    facebook_link = facebook_link,
    website = website,
    seeking_venue = seeking_venue,
    seeking_description = seeking_description
    )
    # print("Artist", artist)
    db.session.add(artist)
    db.session.commit()
  except expression as identifier:
      error = True
      db.session.rollback()
      print(sys.exc_info())
  finally:
      db.session.close()
  if error:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    # abort(400)
  else:
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
    # return jsonify(body)
  #MY-TODO - How do we dump what error occurred?

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  query = db.session.query(Show.artist_id, Show.venue_id, Show.show_time, Venue.name, Artist.name, Artist.image_link).order_by(Show.show_time)
  query = query.join(Venue).join(Artist).all()
  data = []
  for row in query:
    # print(row)
    # print(type(row))
    show_time = row[2]
    # print("Got show time", show_time, type(show_time))
    show_time_no_tz = show_time.replace(tzinfo=None)
    # print("shows:Object type is ", type(show_time_no_tz), show_time_no_tz)
    final_show_time = show_time_no_tz.isoformat() + "Z"
    # print("shows: Got final show time for JSON", final_show_time)
    data.append({
    "venue_id": row[1],
    "venue_name": row[3],
    "artist_id": row[0],
    "artist_name": row[4],
    "artist_image_link": row[5],
    "start_time": final_show_time
  })
  # print("Got shows data", data)
  
  if data == []:
    return render_template('errors/404.html')
  else:
    return render_template('pages/shows.html', shows=data)

  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  # return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  error = False
  try:
    artist_id =  request.form["artist_id"]
    venue_id = request.form["venue_id"]
    show_time = request.form["start_time"]
    # print("Got show time", show_time, type(show_time))
    dt_unware = dateutil.parser.parse(show_time)
    # get local timezone    
    localtz = get_localzone()
    dt_aware = localtz.localize(dt_unware) 
    # print("Got show time obj", dt_aware, type(dt_aware))
    #If venue has a show at a certain time, don't allow show 
    #for +/- 3 hours
    
    # list_current_shows = db.session.query(Show).\
    #   filter(Show.artist_id == artist_id).\
    #     filter(Show.venue_id == venue_id)
    list_current_shows = db.session.query(Show).\
        filter(Show.venue_id == venue_id)
    for show in list_current_shows:
      print ("Got show", show, "for venue id", venue_id)
      time_delta = show.show_time - dt_aware
      print("Timedelta(venue)", time_delta, type(time_delta))
      print(time_delta.days, time_delta.seconds)

      if abs(time_delta.days) < 1 and abs(time_delta.seconds) < 3600:
        print("Timedelta too short for venue, not adding show to listing")
        error = True
        break
    ##TBD Need to do more testing for this time delta thing
    #appears to be working correctly

    # Artist will have only one show per day
    list_current_shows = db.session.query(Show).\
        filter(Show.artist_id == artist_id)
    for show in list_current_shows:
        # print ("Got show", show, "for artist id", artist_id)
        time_delta = show.show_time - dt_aware
        print("Timedelta (artist)", time_delta, type(time_delta))
        print(time_delta.days, time_delta.seconds)
        if abs(time_delta.days) < 1:
          print("Timedelta too short for artist, not adding show to listing")
          error = True
          break
            
    #Bad programming practice - need to see what should be done in Python to break out of try
    #Main path should NOT be indented
    if error == False:
      # print("***Break not working!!")
      show = Show(artist_id=artist_id, venue_id=venue_id, show_time=show_time)
      db.session.add(show)
      db.session.commit()
  except expression as identifier:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    flash('Show' + artist_id + ' was NOT successfully listed!')
  else:
    flash('Show ' + artist_id + ' was successfully listed!')


  

  # on successful db insert, flash success
  
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
