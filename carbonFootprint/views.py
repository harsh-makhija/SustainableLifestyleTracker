from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user
from sqlalchemy import null

from app import db
from carbonFootprint.form import CarbonFootprintTransportForm, CarbonFootprintFoodForm, CarbonFootprintOvernightForm
from models import Co2Values

carbonfootprint_blueprint = Blueprint('carbonfootprint', __name__, template_folder='templates')


@carbonfootprint_blueprint.route("/carbonfootprint", methods=['GET', 'POST'])
@login_required
def carbonfootprint_view():
    if current_user.role == "admin":
        table = Co2Values.query.filter_by(email=current_user.email).all()
        if not table:
            new_calculation = Co2Values(
                id=current_user.id,
                email=current_user.email,
                transportval=0,
                foodval=0,
                electricalval=0,
                finalval=None
            )
            db.session.add(new_calculation)
            db.session.commit()
    """
        Function renders all relevant carbon footprint links for the current user

    """



    return render_template("carbonfootprintPages/CarbonfootprintMain.html", name=current_user.firstname)


@carbonfootprint_blueprint.route("/carbonfootprint/HowWeCalculate", methods=['GET', 'POST'])
@login_required
def how_we_calculate():
    """
        This route is used to view the how we calculate page
    """
    return render_template("carbonfootprintPages/HowWeCalculate.html")


@carbonfootprint_blueprint.route("/carbonfootprint/CarbonFootprintCalculator", methods=['GET', 'POST'])
@login_required
def carbon_footprint_calculator_transport():

    form = CarbonFootprintTransportForm()

    # Dictionary to store the values of the different transport types & their emission values
    # Source "https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2022"
    # See paper titled "Conservation factors 2022: condensed set"
    transport_dictionary = {
        'car petrol': 192,
        'car diesel': 171,
        'car electric': 53,
        'bus': 105,
        'train': 41
    }

    # Dictionary to check the input from user
    choices_dictionary = {
        'yes': 2, 'no': 1
    }
    # Checks if the form is validated
    if form.validate_on_submit():
        # Gets the value of the transport type from the dictionary
        co2Value = transport_dictionary.get(form.transportation.data)

        # Calculates the emission for a single travel
        singleEmissionTravel = co2Value * int(form.distance.data)

        # Gets the value of the times travelled daily from the dictionary using user input
        timesTravelledDaily = choices_dictionary.get(form.toAndFromWork.data)

        # Calculates the emission for a single day
        dailyEmission = singleEmissionTravel * timesTravelledDaily

        # Calculates the emission for a week
        weeklyEmission = dailyEmission * form.daysTravelled.data

        # Calculates the emission for a year
        yearlyEmission = weeklyEmission * form.weeksWorked.data

        # Converts the emission from grams to kilograms
        emissionsKG = int(yearlyEmission) / 1000

        co2_values = Co2Values.query.get(current_user.id)
        co2_values.transportval = emissionsKG
        db.session.commit()

        # Redirects to the carbon footprint calculator page with the emission value
        return render_template("carbonfootprintPages/CarbonFootprintCalculatorTravel.html", form=form,
                               emissions=emissionsKG)

    return render_template("carbonfootprintPages/CarbonFootprintCalculatorTravel.html", form=form)


"""
    This route is used to view the carbon footprint calculator page
"""


@carbonfootprint_blueprint.route("/carbonfootprint/FoodCalculator", methods=['GET', 'POST'])
@login_required
def carbon_footprint_food_calculator():

    form = CarbonFootprintFoodForm()
    # Dictionary for Carbon emissions values of different foods.
    # Source: https://www.science.org/doi/10.1126/science.aaq0216

    food_dictionary = {
        'Beef': 50,
        'Pork': 7.6,
        'Cheese': 11,
        'Fish': 6,
        'Poultry': 5.7,
        'Lamb': 20
    }

    if form.validate_on_submit():
        # For each meat the value is / 100 to find the multiplier and then multiplied by the value of each meat
        beef_value = int(form.beef.data) / 100 * food_dictionary.get('Beef') * 52
        pork_value = int(form.pork.data) / 100 * food_dictionary.get('Pork') * 52
        cheese_value = int(form.cheese.data) / 100 * food_dictionary.get('Cheese') * 52
        fish_value = int(form.fish.data) / 100 * food_dictionary.get('Fish') * 52
        poultry_value = int(form.poultry.data) / 100 * food_dictionary.get('Poultry') * 52
        lamb_value = int(form.lamb.data) / 100 * food_dictionary.get('Lamb') * 52

        yearlyEmissionFood = beef_value + pork_value + cheese_value + fish_value + poultry_value + lamb_value
        co2_values = Co2Values.query.get(current_user.id)

        co2_values.foodval = yearlyEmissionFood
        db.session.commit()

        return render_template("carbonfootprintPages/FoodCalculator.html", form=form, emissions=yearlyEmissionFood)
    return render_template("carbonfootprintPages/FoodCalculator.html", form=form)


'''
    This route is used to view the carbon footprint calculator page
 '''


@carbonfootprint_blueprint.route("/carbonfootprint/CarbonFootprintCalculatorOvernight", methods=['GET', 'POST'])
@login_required
def overnight_carbon_footprint_calculator():

    form = CarbonFootprintOvernightForm()

    # Dictionary of Regions in England and their carbon (g/co2) intensity per Kwh
    # Source "https://carbonintensity.org.uk/"
    # Using api would be more efficient
    regionalDictionary = {"North Scotland": 0, "South Scotland": 5, "NW England": 15, "NE England": 7,
                          "Yorkshire": 150,
                          "North Wales": 13, "South Wales": 336, "East Midlands": 206, "West Midlands": 171,
                          "East England": 176.0,
                          "South East England": 231, "South England": 165, "South West England": 41}

    # Values assigned to user input - How many nights a week
    nightChargeDictionary = {
        "Every night": 7, "Most nights": 5, "Some nights": 3, "Never": 0

    }

    # Asking the user the size of their house will be indicative of how large their boiler is.
    # Different boilers have different kw usage per hour.
    # Source "https://www.charltonandjenrick.co.uk/news/2023/01/do-you-know-how-much-your-heating-costs-per-hour/"
    boilerDictionary = {
        "Small": 20,
        "Medium": 30,
        "Large": 40
    }

    if form.validate():
        # Store regions carbon intensity
        carbonIntensity = regionalDictionary.get(form.userRegion.data)
        overnightCharge = nightChargeDictionary.get(form.overnightCharge.data)
        hoursChargingPerYear = overnightCharge * int(form.hoursSleptAverage.data) * 52

        # if phone not charged every night

        if overnightCharge != 7:
            nightsNotCharged = 7 - int(form.overnightCharge.data)
            # If phone not charged - Assume they charge their phone during the day for how long it takes to charge
            # Calculate the day hours used for charging

            dayCharge = form.hoursToChargeDevice.data * nightsNotCharged
            hoursChargingPerYear = hoursChargingPerYear + dayCharge

        # Source "https://news.energysage.com/how-many-watts-does-a-phone-charger-use/"
        # 7.3 kwh for charging a phone using 20W plug 9 (standard usb-c) an hour a day for 1 year.
        # divide by 365 for hourly usage =  0.02 kwh per hour charging
        chargerKWH = 0.02
        chargingYearlyKWH = chargerKWH * hoursChargingPerYear

        # in grams/co2
        chargerYearlyEmissions = chargingYearlyKWH * carbonIntensity
        chargerEmissionsKG = chargerYearlyEmissions / 1000

        # Lights calculation
        # Light Emissions KW per hour
        lightEmissionsPerHour = 0.42
        # In kwH for one night
        lightsOnKWH = form.lightsLeftOn.data * form.hoursSleptAverage.data * lightEmissionsPerHour

        # Light Electricity usage per year
        lightEmissionsYearlyKWH = lightsOnKWH * 7 * 52

        # Carbon Conversion
        lightEmissionsKG = (lightEmissionsYearlyKWH * carbonIntensity) / 1000

        # Seasonal Questions
        # Heating generally for the months November, December & January
        boilerKWH = boilerDictionary.get(form.houseSize.data)
        # Multiply by 12 for total weeks in winter months
        heatingKWHPerYear = form.winterHeating.data * boilerKWH * 7 * 12
        heatingEmissionsKG = (heatingKWHPerYear * carbonIntensity) / 1000

        totalEmissions = chargerEmissionsKG + lightEmissionsKG + heatingEmissionsKG

        co2_values = Co2Values.query.get(current_user.id)
        co2_values.electricalval = int(totalEmissions)
        db.session.commit()
        return render_template("carbonfootprintPages/CarbonFootprintCalculatorOvernight.html", form=form,
                               emissions=int(totalEmissions))
        # Do summer Fan
    print("did not validate")
    return render_template("carbonfootprintPages/CarbonFootprintCalculatorOvernight.html", form=form)


'''
    This route is used to display the carbon footprint logs of the user
'''


@carbonfootprint_blueprint.route("/carbonfootprint/CarbonFootprintLogs", methods=['GET', 'POST'])
@login_required
def carbon_footprint_logs():

    co2_values = Co2Values.query.filter_by(email=current_user.email).all()
    co2Values = Co2Values.query.get(current_user.id)
    transport = co2Values.transportval
    food = co2Values.foodval
    electric = co2Values.electricalval

    finalval = transport + food + electric

    co2Values.finalval = int(finalval)
    db.session.commit()

    if not co2_values:
        flash('There are no logs to view, Please create a log')
        return render_template("carbonfootprintPages/CarbonFootprintLogs.html")
    else:
        return render_template("carbonfootprintPages/CarbonFootprintLogs.html", logs=co2_values)
