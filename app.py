#import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
	"""List all available api routes."""
	return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/y-m-d (input start date)<br/>"      
        f"/api/v1.0/y-m-d/y-m-d (input start and end date)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
	# Query for the dates and prcp from the last year.
	results = session.query(Measurement.date, Measurement.prcp).\
		filter(Measurement.date >= "2016-08-23").\
		order_by(Measurement.date).all()

	# Convert the query results to a Dictionary using date as the key and prcp as the value.
	prcp_list = []
	for result in results:
		prcp_dict = {}
		prcp_dict["date"] = result.date
		prcp_dict["prcp"] = result.prcp
		prcp_list.append(prcp_dict)

	# Return the JSON representation of your dictionary.	
	return jsonify(prcp_list)


@app.route("/api/v1.0/stations")
def stations():
	# Return a JSON list of stations from the dataset.
	results = session.query(Station.station).all()

	# Convert list of tuples into normal list
	stations = list(np.ravel(results))

	return jsonify(stations)


@app.route("/api/v1.0/tobs")
def tobs():
	# Query for the dates and temperature observations from the last year.
	results = session.query(Measurement.date, Measurement.tobs).\
		filter(Measurement.date >= "2016-08-23").\
		order_by(Measurement.date).all()

	# Convert the query results to a Dictionary using date as the key and tobs as the value.
	tobs_list = []
	for result in results:
		tobs_dict = {}
		tobs_dict["date"] = result.date
		tobs_dict["tobs"] = result.tobs
		tobs_list.append(tobs_dict)

	# Return the JSON representation of your dictionary.	
	return jsonify(tobs_list)


@app.route("/api/v1.0/<start>")
def start(start):
	# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
	# start_date = dt.datetime(2017, 8, 18)
	start_date = dt.datetime.strptime(start, '%Y-%m-%d')

	#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
	filter(Measurement.date >= start_date).all()

	result = list(np.ravel(results))

	return jsonify(result)



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
	# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
	# start_date = dt.datetime(2017, 8, 10)
	# end_date = dt.datetime(2017, 8, 20)
	start_date = dt.datetime.strptime(start, '%Y-%m-%d')
	end_date = dt.datetime.strptime(end, '%Y-%m-%d')

	#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
	results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
	filter(Measurement.date >= start_date).\
	filter(Measurement.date <= end_date).all()

	result = list(np.ravel(results))

	return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)

