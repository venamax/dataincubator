# Building a Dashboard

In this miniproject, we're going to build an interactive web "Bus dashboard" app utilizing NYC's transit data. As such, we'll be focusing on explanatory visualization.

- We're going to use [Bokeh](http://bokeh.pydata.org/en/latest/) to power our dashboard. 
- We'll use [Heroku](https://devcenter.heroku.com/articles/python-gunicorn) and [Flask](http://flask.pocoo.org/) for our web stack.
- If you're a Fellow or Scholar, you'll recognize this stack from the 12-day milestone project. 
- The miniproject contains plenty of room to expermient front-end web technologies such as [Leaflet.js](http://leafletjs.com/) and [D3.js](https://d3js.org). If you're comfortable with Bokeh, consider trying these new technologies to broaden your skillset.

Unlike some of the other miniprojects, this one is a bit less structured. The below outline and sample app are meant as a guideline. If there's a particular direction you'd like to explore with this data, by all means submit some custom visualizations! If you prefer, feel free to visualize the open bus data in your city of choice.

## Dataset and Plan [Do ASAP: Request Developer Access from MTA]

We're going to use an [Archive of transit data](http://data.beta.nyc/dataset/unofficial-mta-transit-data-archive/resource/106dd52f-8755-40a0-aa3d-dfa6195a8d21) and the [Live Feed](http://bustime.mta.info/wiki/Developers/Index/) of MTA Bus data (you'll need to request an API key, stop reading and fill out the form for this now!).

- The former is useful for determining overall reliability of a given bus line at a given time/location, the latter is useful for live stop information, of course!

- Aside from the archived bus time data, also extremely useful is the [GTFS data](https://developers.google.com/transit/gtfs/) in the Archive (under the `gtfs` folder). This includes scheduled departure times, route information, stop ID locations, etc.


- Want a pre-filtered dataset to play with some visualizations? We've got you covered.
`s3://thedataincubator-course/viz-miniproject/manhattan.csv` contains 7 days' of nicely filtered data joined to some basic stop information.


## An overview of the data 

### Historical Data
The historical archive of data includes archives of real-time bus information (positions for each bus at a given time) as well as schedule data for each bus trip. It's a little messy. If you're using our dataset, you can use the following snippet to quickly load the data with datetime indices.

```python
date_format_str = "%Y-%m-%d %H:%M:%S"
date_parser = lambda u: pd.datetime.strptime(u, date_format_str)
df = pd.read_csv("manhattan.csv",  
                 parse_dates=True,
                 date_parser=date_parser,
                 index_col=0) # peek into the csv: col 0 is 'timestamp'
```


### Live Data 
This data is similarly formatted to the historical data, except live-updating every ~30 seconds (dependent on the physical bus transponders' reporting ability). You'll notice many of the values (stop IDs, trip IDs) fortunately use the same GTFS identifying information, so we can join without too much trouble (this is _not_ a given with open government data). We leave this as an exercise. The `VehicleMonitoring` endpoint ([link](http://bustime.mta.info/wiki/Developers/SIRIVehicleMonitoring)) is particularly useful.

Here's some more code that will make your life easier - once you have an API key, fill that out along with the `MTA_API_BASE` constant and you should be able to query the API without too much extra code.

```python
import json
import pandas as pd

def _flatten_dict(root_key, nested_dict, flattened_dict):
    for key, value in nested_dict.iteritems():
        next_key = root_key + "_" + key if root_key != "" else key
        if isinstance(value, dict):
            _flatten_dict(next_key, value, flattened_dict)
        else:
            flattened_dict[next_key] = value
    return flattened_dict
    
#This is useful for the live MTA Data
def nyc_current():
    resp = requests.get(MTA_API_BASE.format(MTA_API_KEY)).json()
    info = resp['Siri']['ServiceDelivery']['VehicleMonitoringDelivery'][0]['VehicleActivity']
    return pd.DataFrame([_flatten_dict('', i, {}) for i in info])
```


## Part 1: Initial Setup / Getting an App Live

Your first step should be setting up a skeleton app with Flask and Bokeh. [This repository](https://github.com/thedataincubator/flask-demo) is a good place to start. 

One important note: we've found that the conda buildpack provided in that repository consumes lots of space during compilation (and runs up against heroku space limitations quickly). We've had good luck with this [numpy / scipy buildpack](https://github.com/thenovices/heroku-buildpack-scipy) (nb. once you have numpy, you have pandas). Using this buildpack, we were able to push the 80MB `manhattan.csv` file provided above as a static, low-fuss database that we load into pandas during app start.


## Part 2: Plot Some Data [Python]
Let's start our dashboard with a simple visualization: the number of unique buses on the road at any given time. 
- Download 4-5 days' worth of data from this [archive of live updates](http://data.mytransit.nyc/bus_time/) (or use our pre-filtered dataset).
- `vehicle_id` contains a number that uniquely identifies each vehicle on the road that's currently reporting information. You'll want to count this value to determine how many buses are on the road.
- You'll want to sample counts at some fixed interval (e.g. every 15mins, 30mins, or 1hr). The granularity is up to you. Our pre-filtered dataset takes ~3 minute windows every 15 minutes.

** Your visualization should**:
1. Display a count of currently reporting vehicles at each time within a user-selected interval (eg. 2015-01-28 from 9AM EST to 12PM EST)
2. Allow the user to select different days and intervals. 
3. Another interesting visualization might be a simple histogram of the distribution of sampled counts. What does this distribution look like? Following up with this histogram, can you create another visualization to explain the trends you're seeing in count frequency?

**Making this production-ready**:
If you do this miniproject "from scratch" (ie downloading and processing the data manually), you'll quickly find that you cannot deploy the entire dataset to heroku. You'll need to just provide the relevant, processed data for your visualization when you upload.


## Part 3: Integrating Live Data [Python]

Now, add in the information from the live `VehicleMonitoring` endpoint. 

**Your visualization should** 
1. Display how many buses are currently on the road.
2. Compare current bus counts with historical data - maybe download more days and aggregate counts (once you have the code to extract counts from one `.csv` file, you should be able to extract counts from any number of the `.csv` archive files. 
3. Consider adding a chart that groups by borough or route. A [box and whisker](http://www.datavizcatalogue.com/methods/box_plot.html) plot might be useful to help us understand the current vehicle count in the context of historical bus data.

## Part 4: Map some data [JS, Python]

Using the dataset's geolocation information, let's make a heatmap of bus positions at a given time.

You can do this in a fully web-based way using the following stack:

**Frontend**
- [Leaflet.js](http://leafletjs.com/)
- [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat)
- [D3.js](https://d3js.org/)

**Backend**
- Pandas

Your frontend code should use D3 to asynchronously query the server/load the location points for buses at a specified time. From there, pass those points into a Leaflet heatmap.

## Part 5: Animate the plot [JS, Python]

Now, given the ability to look at the heatmap of any given time, let's suppose we want to visualize the ebb and flow of buses throughout a given day. Try animating the heatmap to develop something similar to this:
![buses](http://i.imgur.com/DIid7p7.gif)
