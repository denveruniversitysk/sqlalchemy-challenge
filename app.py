# Import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func 

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Save references to each table
measure = Base.classes.measurement
station = Base.classes.station

# Create session link to Python DB
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
            f"/api/v1.0/2016-08-23<br/>"
            f"/api/v1.0/2016-08-23/2017-08-23<br/>")

# List precipitation data from start date to end date
@app.route("/api/v1.0/precipitation")
def precipitation():
    pre_results = session.query(measure.date,measure.prcp).filter(measure.date>="2016-08-23").all()
    pre_dictionary = list(np.ravel(pre_results))
    return jsonify(pre_dictionary)

# List all available stations
@app.route("/api/v1.0/stations")
def stations():
    sta_results = session.query(station.station,station.name).all()
    sta_dictionary = list(np.ravel(sta_results))
    return jsonify(sta_dictionary)

# List temperatures based on start date and end date
@app.route("/api/v1.0/tobs")
def tobs():
    temp_results = session.query(measure.date,measure.tobs).\
        filter(measure.date>="2016-08-23").\
        filter(measure.date<="2017-08-23").all()
    temp_dictionary = list(np.ravel(temp_results))
    return jsonify(temp_dictionary)

# List min, max, and avg for given start date
@app.route("/api/v1.0/<start>")
def start(start):
    sel = session.query(measure.date, func.min(measure.tobs), func.avg(measure.tobs), func.max(measure.tobs))
    start_results = (session.query(*sel)
                       .filter(func.strftime("2016-08-23", measure.date) >= start)
                       .group_by(measure.date)
                       .all())

    dates = []                       
    for result in start_results:
        start_dictionary = {}
        start_dictionary["Date"] = result.dates
        start_dictionary["Lowest Temperature"] = result.func.min(measure.tobs)
        start_dictionary["Average Temperature"] = result.func.avg(measure.tobs)
        start_dictionary["Highest Temperature"] = result.func.max(measure.tobs)
        dates.append(start_dictionary)
    return jsonify(dates)  

# List min, max, and avg for given start and end date
@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
    sel=[measure.date, func.min(measure.tobs),func.avg(measure.tobs), func.max(measure.tobs)]
    
    startend_results = (session.query(*sel)
                    .filter(func.strftime("2016-08-23", measure.date) >= start)
                    .group_by(measure.date)
                    .all())

    dates = []                       
    for result in startend_results:
        start_dictionary = {}
        start_dictionary["Date"] = result.dates
        start_dictionary["Lowest Temperature"] = result.func.min(measure.tobs)
        start_dictionary["Average Temperature"] = result.func.avg(measure.tobs)
        start_dictionary["Highest Temperature"] = result.func.max(measure.tobs)
        dates.append(start_dictionary)
    return jsonify(dates) 

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)