import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
    results = query1 = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
    session.close()

    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)
    
@app.route("/api/v1.0/stations")
def stations1():

    session = Session(engine)
    results = session.query(Station.station).all()    
    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    results = session.query(Measurement.tobs).\
    filter(Measurement.date >= query_date).\
    filter(Measurement.station == 'USC00519281').all()
    session.close()

    all_tobs = list(np.ravel(results))
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):

    session = Session(engine)
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).all()
    session.close()

    start_tobs = list(np.ravel(results))
    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):

    session = Session(engine)
    results = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    session.close()

    start_end_tobs = list(np.ravel(results))
    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)



