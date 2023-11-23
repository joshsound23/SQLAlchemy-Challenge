# Import the dependencies.
from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with = engine) 
measurement = Base.classes.measurement
station = Base.classes.station




app = Flask(__name__)



@app.route("/")
def home():
    """Homepage with available routes."""
    return (
        f"Welcome to the Climate App API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create a session
    session = Session(engine)

    try:


        # Query for the last 12 months of precipitation data
        results = session.query(measurement.date, measurement.prcp) \
                         .filter(measurement.date >= 2016) \
                         .all()

        # Convert query results to a dictionary with date as key and prcp as value
        precipitation_data = {date: prcp for date, prcp in results}

        # Return JSON response
        return jsonify(precipitation_data)


    finally:
        # Close the session
        session.close()


@app.route("/api/v1.0/stations")
def stations():
    
    # Create a session
    session = Session(engine)

    try:
        # Query stations from the Station table
        stations_data = session.query(station.station).all()

        # Convert the query results to a list
        stations_list = [station[0] for station in stations_data]

        # Return JSON response
        return jsonify(stations_list)

    

    finally:
        # Close the session
        session.close()

@app.route("/api/v1.0/tobs")
def tobs():
    """Return JSON list of temperature observations for the previous year."""
    # Create a session
    session = Session(engine)

    try:
        

        # Query for the most active station for the previous year
        most_active_station = session.query(measurement.station) \
                                    .group_by(measurement.station) \
                                    .order_by(func.count().desc()) \
                                    .first()[0]

        # Query temperature observations for the most active station for the previous year
        results = session.query(measurement.date, measurement.tobs) \
                         .filter(measurement.station == most_active_station) \
                         .filter(measurement.date >= 2016) \
                         .all()

        # Convert query results to a list of dictionaries
        tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]

        # Return JSON response
        return jsonify(tobs_data)
    
    finally:
        # Close the session
        session.close()



if __name__ == '__main__':
    app.run(debug=True)