from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, ValidationError
from wtforms.validators import DataRequired, AnyOf, URL, Length
import re

state_choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]

genres_choices = [
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]

class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    def validate_phone(form, field):
        # if not re.search(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", field.data):
        print("validate_phone: Got phone ", field.data)
        if not re.search(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", field.data):
        # if not re.search(r"^\+(?:[0-9]*?){6,14}[0-9]$", field.data):
            print("VenueForm: validate_phone: Phone not validated")
            raise ValidationError("Invalid phone number")
        return True

    def validate_genres (form, field):
        genres_values = [choice[1] for choice in genres_choices]
        for value in field.data:
            print("validate_genres: Got genre ", value)
            if value not in genres_values:
                print("VenueForm: validate_genres: Genres not validated")
                raise ValidationError("Invalid genre " + value + " for Artist " + self.name)
        return True
    
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genres_choices
    )
    seeking_talent = BooleanField('seeking_talent')
    seeking_description = StringField('seeking_description', validators=[DataRequired(), Length(max=500)])
    image_link = StringField('image_link', validators= [DataRequired(), URL(), Length(max=500)])
    website = StringField('website', validators= [DataRequired(), URL(), Length(max=120)])

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

class ArtistForm(Form):
    def validate_phone(form, field):
        print("validate_phone: Got phone ", field.data)        
        if not re.search(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", field.data):
            raise ValidationError("Invalid phone number" + field.data)

    def validate_genres (form, field):
        genres_values = [choice[1] for choice in genres_choices]
        for value in field.data:
            print("validate_genres: Got genre {}".format(value))
            if value not in genres_values:
                raise ValidationError("Invalid genre " + value + " for Artist " + self.name)


    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=state_choices
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone',
        validators=[DataRequired()]
    )
    
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=genres_choices
    )
    seeking_venue = BooleanField('seeking_venue')
    seeking_description = StringField('seeking_description', validators=[DataRequired(), Length(max=500)])
    image_link = StringField('image_link', validators= [DataRequired(), URL(), Length(max=500)])
    website = StringField('website', validators= [DataRequired(), URL(), Length(max=120)])
    facebook_link = StringField(
        # TODO implement enum restriction - 
        # looks like URL validation is done already - not doing anything
        'facebook_link', validators=[URL()]
    )


# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
