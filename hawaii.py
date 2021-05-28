from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
import numpy as np
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from sqlalchemy import desc

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
print (Base.classes.keys())
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask app begin
app = Flask(__name__)

@app.route("/")
def home():
    print("server received request for 'Home' page...")
    return """/api/v1.0/precipitation<br/>
    /api/v1.0/stations<br/>
    /api/v1.0/TOBS<br/>
    /api/v1.0/&ltstartdate&gt<br/>
    /api/v1.0/&ltstartdate&gt/&ltenddate&gt"""

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, func.avg(Measurement.prcp)).\
      filter(Measurement.date < "2017-08-24").\
      filter(Measurement.date > "2016-08-23").\
        order_by(Measurement.date).\
        group_by(Measurement.date).\
        all()
    session.close()
    precipitations = {}
    for item in results:
        precipitations[item[0]] = item[1]
    return jsonify(precipitations)



# /api/v1.0/station
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.name, Station.station).all()
    session.close()

    all_stations=[]

    for name, station in results:
        all_stations_dict={}
        all_stations_dict[name] = station 
        all_stations.append(all_stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/TOBS")
def TOBS():
    session = Session(engine)
    row = session.query(Measurement.station \
                        ,func.count(Measurement.station)
                        ,func.max(Measurement.date) )\
                .group_by(Measurement.station) \
                .order_by(desc(func.count(Measurement.station))).all()

    activeStation = row[0][0]
    maxDate = row[0][2]

    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date < maxDate).\
        filter(Measurement.station == activeStation).\
        all()
    precipitations = {}
    for item in results:
        precipitations[item[0]] = item[1]
    return jsonify(precipitations)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")

def start_end(start=None, end=None): 
    session = Session(engine) 
    the_temps = [func.min(Measurement.prcp), func.max(Measurement.prcp), func.avg(Measurement.prcp)]
    if not end:
       results = session.query(*the_temps).\
       filter(Measurement.date <= start).all()
       temps = list(np.ravel(results))
       return jsonify(temps)

    results = session.query(*the_temps).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))

    return jsonify(temps=temps)






if __name__ == "__main__":
    app.run(debug=True)