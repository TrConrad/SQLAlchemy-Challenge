# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import json



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available API routes"""

    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query one years worth of Precipitation data """

    # Create our session (link) from Python to the DB
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year = last_date - dt.timedelta(days=365)
    
    sel = [Measurement.date, Measurement.prcp]
    total_precip_data = session.query(*sel).\
        filter(func.date(Measurement.date) <= last_date).\
        filter(func.date(Measurement.date) >= one_year).\
        filter(Measurement.prcp != None).\
        order_by(Measurement.date).all()

    session.close()

    precip_data = []
    for date, precipitation in total_precip_data:
            precip_dict = {"Date": "Precipitation"}
            precip_dict["Date"] = date
            precip_dict["Precipitation"] = precipitation
            precip_data.append(precip_dict)


    return jsonify(precip_data)


@app.route("/api/v1.0/station")
def station():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    

    station_list = session.query(Station.station).\
    all()

    session.close()

    results = list(np.ravel(station_list))
    
    return jsonify(results=results)


@app.route("/api/v1.0/tobs")
def temperature():

    # Create our session (link) from Python to the DB
    session = Session(engine)
     
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    last_date = dt.datetime.strptime(last_date, '%Y-%m-%d')
    one_year = last_date - dt.timedelta(days=365)
    
    sel = [Measurement.date, func.avg(Measurement.tobs)]
    temp_data = session.query(*sel).\
    filter(func.date(Measurement.date) <= last_date).\
    filter(func.date(Measurement.date) >= one_year).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()

    session.close()

    temperature_data = []
    for date, temperature in temp_data:
            temp_dict = {"Date": "Temperature"}
            temp_dict["Date"] = date
            temp_dict["Temperature"] = temperature
            temperature_data.append(temp_dict)

    return jsonify(temperature_data)

@app.route("/api/v1.0/<start>")
def start_date(start):

      # Create our session (link) from Python to the DB
    session = Session(engine)

    start = dt.datetime.strptime(start, "%Y-%m-%d")
     
    beginning_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()

    session.close()

    
   
    temps = list(np.ravel(beginning_temp))
    print(temps)
    print(type(temps))

    if len(temps) > 0:
        return jsonify(temps)
        
    else:
        return jsonify({"error": "Data not available."}), 404


@app.route("/api/v1.0/<start>/<end>")
def time_window(start, end):

     # Create our session (link) from Python to the DB
    session = Session(engine)

    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")
     
    window_temp = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()

    session.close()

    windows = list(np.ravel(window_temp))
    
    if len(windows) > 0:
        return jsonify(windows)
        
    else:
        return jsonify({"error": "Data not available."}), 404

if __name__ == "__main__":
    app.run(debug=True)
