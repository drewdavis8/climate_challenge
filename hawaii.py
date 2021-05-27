from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
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
    results = session.query(Station.name).all()
    session.close()

    all_names = []
    for name in results:
        names_dict = {}
        names_dict["name"] = name
        all_names.append(names_dict)
    return jsonify(all_names)



# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.

@app.route("/api/v1.0/TOBS")
def TOBS():
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





# /api/v1.0/<start> and /api/v1.0/<start>/<end>

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.




if __name__ == "__main__":
    app.run(debug=True)