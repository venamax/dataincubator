# Building a Dashboard

In this miniproject, we're going to build an interactive web "Bus dashboard" app utilizing NYC's transit data. As such, we'll be focusing on explanatory visualization.

- We're going to use [Bokeh](http://bokeh.pydata.org/en/latest/) to power our dashboard. 
- We'll use [Heroku](https://devcenter.heroku.com/articles/python-gunicorn) and [Flask](http://flask.pocoo.org/) for our web stack.
- If you're a Fellow or Scholar, you'll recognize this stack from the 12-day milestone project. 
- The miniproject contains plenty of room to experiment with front-end web technologies such as [Leaflet.js](http://leafletjs.com/) and [D3.js](https://d3js.org). If you're comfortable with web development, consider trying these new technologies to broaden your skillset.

Unlike some of the other miniprojects, this one is a bit less structured. The below outline and sample app are meant as a guideline. If there's a particular direction you'd like to explore with this data, by all means submit some custom visualizations! If you prefer, feel free to visualize the open bus data in your city of choice.


## Dataset and Plan [Do ASAP: Request Developer Access from MTA]

We're going to use an [Archive of transit data](http://data.beta.nyc/dataset/unofficial-mta-transit-data-archive/resource/106dd52f-8755-40a0-aa3d-dfa6195a8d21) and the [Live Feed](http://bustime.mta.info/wiki/Developers/Index/) of MTA Bus data (you'll need to request an API key, stop reading and fill out the form for this now!).

- The former is useful for determining overall reliability of a given bus line at a given time/location, the latter is useful for live stop information, of course!
- Aside from the archived bus time data, also extremely useful is the [GTFS data](https://developers.google.com/transit/gtfs/) in the Archive (under the `gtfs` folder). This includes scheduled departure times, route information, stop ID locations, etc.

## An overview of the data 

### Historical Data
The historical archive of data includes archives of real-time bus information (positions for each bus at a given time) as well as schedule data for each bus trip. It's a little messy. Here's the code we use to clean it up.

```python
#ETL
import pandas as pd
import numpy as np
from datetime import timedelta, datetime


def convert_to_int64(row):
    try:
        return np.int64(row)
    except ValueError:
        return np.nan

def utc_to_est(row):
    try:
        return row - timedelta(hours=5)
    except:
        raise

csv_f = pd.read_csv
#sub with the CSV files you downloaded
archive = pd.concat([csv_f("bus_time_first.csv"),
                     csv_f("bus_time_second.csv")])

#gtfs data for joins
trips = pd.read_csv("trips.txt")
stops = pd.read_csv("stops.txt")
schedules = pd.read_csv("stop_times.txt")
schedules.departure_time = pd.to_datetime(schedules.departure_time)
archive.timestamp = pd.to_datetime(archive.timestamp).apply(utc_to_est)
archive.next_stop_id = archive.next_stop_id.apply(convert_to_int64)

#query and clean
live_archive = archive[archive.block_assigned > 0] # "assigned" to a route

#throw away trips with <15 reports, probably not real
good_trips_only = today.groupby(today.trip_id).filter(lambda group: len(group) > 15)
" dataset

#merged dataframe with both trip information and stop information
partial = good_trips_only.merge(trips, on='trip_id') 
df = partial.merge(stops, left_on="next_stop_id", right_on="stop_id")
```

### Live Data 
This data is similarly formatted to the historical data, except live-updating every ~30 seconds (dependent on the physical bus transponders' reporting ability). You'll notice many of the values (stop IDs, trip IDs) fortunately use the same GTFS identifying information, so we can join as we did we the above code (this is _not_ a given with open government data). We leave this as an exercise. The `VehicleMonitoring` endpoint ([link](http://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring)) is particularly useful.

Here's some more code that will make your life easier - you can use this to flatten out the large nested tree that the `VehicleMonitoring` endpoint gives back.

```python
#This is useful for the live MTA Data
def flatten_dict(root_key, nested_dict, flattened_dict):
    for key, value in nested_dict.iteritems():
        next_key = root_key + "_" + key if root_key != "" else key
        if isinstance(value, dict):
            flatten_dict(next_key, value, flattened_dict)
        else:
            flattened_dict[next_key] = value
    return flattened_dict
```

## Part 1: Initial Setup / Getting an App Live

Your first step should be setting up a skeleton app with Flask and Bokeh. [This repository](https://github.com/thedataincubator/flask-demo) is a good place to start. 

We're partial to Continuum Analytics' python distribution and package manager, `conda` (they make bokeh too). You already have `conda` on this machine and can run the command

```
conda env create --name viz --file conda-requirements.txt
```

to set up a new environment from the base requirements file we've provided. Then, run

```
source activate viz
```

to enter the environment, and

```
pip install -r requirements.txt
```

to finish installing the dependencies to a local env.

## Part 2: Plot Some Data [Python]
Let's start our dashboard with a simple visualization: the number of unique buses on the road at any given time. 
- Download 4-5 days' worth of data from this [archive of live updates](http://data.mytransit.nyc/bus_time/)
- `vehicle_id` contains a number that uniquely identifies each vehicle on the road that's currently reporting information. You'll want to count this value to determine how many buses are on the road.
- You'll want to sample counts at some fixed interval (e.g. every 15mins, 30mins, or 1hr). The granularity is up to you.

** Your visualization should**:
1. Display a count of currently reporting vehicles at each time within a user-selected interval (eg. 2015-01-28 from 9AM EST to 12PM EST)
2. Allow the user to select different days and intervals. 
3. Another interesting visualization might be a simple histogram of the distribution of sampled counts. What does this distribution look like? Following up with this histogram, can you create another visualization to explain the trends you're seeing in count frequency?

**Making this production-ready**:
Keeping all this data in memory is not tractible if you want to, for example, deploy this dashboard to Heroku. To return this result, you'll need to keep track of just what vehicles are on the road during each hour interval.

## Part 3: Integrating Live Data [Python]

Now, add in the information from the live `VehicleMonitoring` endpoint. 

**Your visualization should** 
1. Display how many buses are currently on the road.
2. Compare current bus counts with historical data - maybe download more days and aggregate counts (once you have the code to extract counts from one `.csv` file, you should be able to extract counts from any number of the `.csv` archive files.
3. Consider adding a chart that groups by borough or route. A [box and whisker](http://www.datavizcatalogue.com/methods/box_plot.html)_ plot might be useful to help us understand the live vehicle count in the context of historical bus data.

## Part 4: Heatmap

Let's take the data you plotted in part 2 and turn it into a live-updating heatmap.

You can do this in a fully web-based way using the following stack:
**Frontend**
- [Leaflet.js](http://leafletjs.com/)
- [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat)
- [D3.js](https://d3js.org/)

**Backend**
- Pandas

**Your Visualization Should**
1. Allow the user to see the progression of bus concentrations on a map throughout various time intervals (use animation)
2. Example [here](heroku app link)
