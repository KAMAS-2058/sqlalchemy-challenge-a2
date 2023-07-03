# Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
station_list = Base.classes.station
measurement_weather = Base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Data setup
#################################################

#################################################
# Flask Routes
#################################################

@app.route("/")
def main_page():
    return('hello')


@app.route('/api/v1.0/precipitation')
def main_page():
    
    most_recent_data = session.query(measurement_weather.date)\
                                .order_by(measurement_weather.date.desc())\
                                .first()

    # Calculate the date one year from the last date in data set.
    aug_last_year = dt.date(2016, 8, 22) 
    print(aug_last_year)
    # Perform a query to retrieve the data and precipitation scores
    prev_percp = session.query(measurement_weather.date, measurement_weather.prcp).\
                        filter(measurement_weather.date >= aug_last_year).\
                        order_by(measurement_weather.date.desc()).all()

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    prev_year_df = pd.DataFrame(prev_percp)
    prev_year_df = prev_year_df.set_index('date')

    # Sort the dataframe by date
    prev_year_df_date_sort = prev_year_df.sort_values(by='date',ascending = True)
    
    return jsonify(dict(prev_year_df_date_sort)) 
        

@app.route('/api/v1.0/stations')
def main_page():

    stations = session.query(measurement_weather.station, func.count(measurement_weather.station))

    return jsonify(dict(stations))

@app.route('/api/v1.0/tobs')
def main_page():

    active_temp_query = session.query(func.min(measurement_weather.tobs),
                                     func.max(measurement_weather.tobs),
                                     func.avg(measurement_weather.tobs))\
                                     .filter(measurement_weather.station == most_active[0][0])\
                                     .all()


    return jsonify(dict(active_temp_query))

# @app.route('/api/v1.0/<start>')
# def main_page():
   



#    return   

# @app.route('/api/v1.0/start/<end>')
# def main_page():
#     return()


if __name__ == '__main__':
    app.run(debug=True)