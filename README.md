# Team 27 
This file contains an overview of our functionality, locations of relevant documentation and sources of data

# Description
- # Sustainable Lifestyle Tracker
  - This web application is used to track your sustainable lifestyle. It uses python, flask, HTML, CSS and Jinja in order to create a functioning application.
- # Exercise Log
  - There is an exercise log feature that allows users to view, create and delete logs. The logs are stored in a database and are displayed on the page. 
- # Carbon Footprint Calculator
  - The footprint calculator allows the user to calculate their carbon emissions based on their lifestyle choices. (see references)
  
## How To Run
1. Clone the repository
2. Run the command `pip install -r requirements.txt` to install the dependencies (may need to double-click .db file in instance folder)
3. Create a flask Configuration with the target app.py
4. Initialise the database by running the commands `from app import db`, `from models import init_db`, `init_db()` in the python shell
5. Run the command `python app.py` to run the application
6. Open the link in your browser
7. Credentials for admin are "admin@email.com", "Admin1!"

## GitHub Repository Link
https://github.com/newcastleuniversity-computing/CSC2033_Team27_22-23

## Functionality
- Flask configuration located in app.py
- Database setup in models.py
- HTML files located in TEMPLATES folder
- Static contains CSS stylesheet and image files
- CSS style sheet split by page.
- Users directory contains all necessary functionality for logging in, out, registering etc.
- exerciseLog Directory contains all functionality for creating, viewing and deleting user logs.
- carbonFootprint Directory contains all algorithms for calculating carbon Emissions

# Relevant Documentation
- **Team Coding standards** document located: ""
- **Accessibility analysis** document located:
- **Testing documentation** is located: ""
- Contribution matrix located: ""

# Visuals
- See Technical Demonstration

# References
Our calculations required data from many sources for calcualting carbon emissions.
All website links are commented in the appropriate places in 'carbonFootprint/views.py'.
Here is a list of them all:
- Travel Emissions
  - https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2022
- Food Emissions
  - https://www.science.org/doi/10.1126/science.aaq0216
- Overnight Choices Emissions
  - https://carbonintensity.org.uk/ - regional carbon intensity
  - https://www.charltonandjenrick.co.uk/news/2023/01/do-you-know-how-much-your-heating-costs-per-hour/ - Boiler emissions
  - https://news.energysage.com/how-many-watts-does-a-phone-charger-use/ - KWH usage of a standard 20W charging plug
