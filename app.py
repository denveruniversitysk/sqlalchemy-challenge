# Import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, scoped_session,sessionmaker
from sqlalchemy import create_engine, func 

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False})

# Reflect an existing database
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
measure = Base.classes.measurement
station = Base.classes.station

# Create session link to Python DB
session = scoped_session(sessionmaker(bind=engine))
session = Session(engine)

# Flask Setup
app = Flask(__name__)


# List all routes available
@app.route("/")
def home():
    print("/api/v1.0/precipitation"
    "/api/v1.0/stations"
    "/api/v1.0/tobs"
    "/api/v1.0/<start>"
    "/api/v1.0/<start>/<end>")
    return (f"Welcome to the Hawaii Climate API!<br/>"
            f"--------------------------<br/>"
            f"Routes:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations</br>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/start<br/>"
            f"/api/v1.0/startend<br/>")

# Convert the query results to a dictionary using date as the key and prcp as the value
@app.route("/api/v1.0/precipitation")
def precipitation():
    pre_results = session.query(measure.date,measure.prcp).all()
    pre_dictionary = list(np.ravel(pre_results))
    return jsonify(pre_dictionary)

# Return a JSON list of stations from the dataset
@app.route("/api/v1.0/stations")
def stations():
    sta_results = session.query(station.station,station.name).all()
    sta_dictionary = list(np.ravel(sta_results))
    return jsonify(sta_dictionary)

# Query the dates and temperature observations of the most active station for the last year of data
# Return a JSON list of temperature observations (TOBS) for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    temp_results = session.query(measure.date,measure.tobs).\
        filter(measure.date>="2016-08-23").\
        filter(measure.date<="2017-08-23").all()
    temp_dictionary = list(np.ravel(temp_results))
    return jsonify(temp_dictionary)

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
@app.route("/api/v1.0/start")
def start():
    start_results = session.query(func.min(measure.tobs), func.max(measure.tobs),
                                       func.avg(measure.tobs)).filter(measure.date.between(dt.date(2016,8,23),dt.date(2016,8,23))).all()
    return jsonify(start_results)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
@app.route("/api/v1.0/startend")
def startend():
    startend_results = session.query(func.min(measure.tobs), func.max(measure.tobs),
                                       func.avg(measure.tobs)).filter(measure.date.between(dt.date(2016,8,23),dt.date(2017,8,23))).all()
    
    return jsonify(startend_results) 

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)