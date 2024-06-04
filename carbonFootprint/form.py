from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class CarbonFootprintTransportForm(FlaskForm):
    """
    Developed by Matthew
    """
    # mode of transport
    transportation = SelectField('Transportation', choices=['car petrol', 'car diesel', 'car electric', 'bus', 'train'],
                                 validators=[DataRequired()])

    # Distance travelled
    distance = SelectField('Distance (km)', choices=[5, 10, 15, 20, 25, 30], validators=[DataRequired()])

    #
    toAndFromWork = SelectField('Travel To And From', choices=['yes', 'no'], validators=[DataRequired()])

    daysTravelled = IntegerField('Days Travelled', validators=[DataRequired(), NumberRange(min=1, max=7)])

    weeksWorked = IntegerField('Weeks Worked', validators=[DataRequired(), NumberRange(min=1, max=52)])

    submit = SubmitField()


class CarbonFootprintFoodForm(FlaskForm):
    """
    Developed by Afa
    """
    numbers = [(str(i), str(i)) for i in range(0, 2001, 100)]

    beef = SelectField('Beef', choices=numbers, validators=[DataRequired()])

    lamb = SelectField('Lamb', choices=numbers, validators=[DataRequired()])

    pork = SelectField('Pork', choices=numbers, validators=[DataRequired()])

    cheese = SelectField('Cheese', choices=numbers, validators=[DataRequired()])

    fish = SelectField('Fish', choices=numbers, validators=[DataRequired()])

    poultry = SelectField('Poultry', choices=numbers, validators=[DataRequired()])

    submit = SubmitField()


class CarbonFootprintOvernightForm(FlaskForm):
    """
    Developed by Matthew
    """

    # apply regional data for kwh energy from views.py
    userRegion = SelectField('What region of the UK are you from?',
                             choices=["North Scotland", "South Scotland", "NW England",
                                      "NE England", "Yorkshire", "North Wales", "South Wales",
                                      "East midlands", "West Midlands", "East England",
                                      "South East England", "South England", "South West England"])

    # size of house is indicative of boiler size
    houseSize = SelectField('Select your house size', choices=["Large", "Medium", "Small"],
                            validators=[DataRequired()])

    # charge phone overnight?
    overnightCharge = SelectField('If you charge your phone overnight, how often?',
                                       choices=['Every night', 'Most nights', 'Some nights', 'Never'])
    # Time it takes to charge users phone in hours
    hoursToChargeDevice = IntegerField('How long does it take to charge your phone? (hours)',
                                       validators=[DataRequired(), NumberRange(min=1, max=5)])
    # If user Leaves a light on overnight, how many
    lightsLeftOn = IntegerField('If you leave any lights on overnight, how many?',
                                validators=[DataRequired(), NumberRange(min=0, max=15)])
    # Seasonal questions
    # Over winter if they use heating
    winterHeating = IntegerField('In the winter months, how many hours a night do you typically put the heating on for?',
                                 validators=[DataRequired(), NumberRange(min=0, max=24)])
    # Over summer if they use fan - UK assumption no AC
    #summerCooling = IntegerField('In the summer months, how many hours a night do you use a fan?',
    #                             validators=[DataRequired(), NumberRange(min=0, max=24)])




    # how many hours the user sleeps a night
    hoursSleptAverage = IntegerField('How many hours do you sleep a night?',
                                     validators=[DataRequired(), NumberRange(min=1, max=24)])

    submit = SubmitField()