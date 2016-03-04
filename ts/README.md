# Overview
Time series prediction presents its own challenges which are different from
machine-learning problems.  As with many other classes of problems, there are
a number of common features in these predictions.

## Fetch the data:
http://s3.amazonaws.com/thedataincubator/coursedata/mldata/train.txt.gz

The columns of the data correspond to the
  - year
  - month
  - day
  - hour
  - temp
  - dew_temp
  - pressure
  - wind_angle
  - wind_speed
  - sky_code
  - rain_hour
  - rain_6hour
  - city

We will focus on using the temporal elements to predict the temperature.

## Per city model

It makes sense for each city to have it's own model.  Build a "groupby"
estimator that takes an estimator as an argument and builds the resulting
"groupby" estimator on each city.  That is, `fit` should fit a model per city
while the `predict` method should look up the corresponding model and perform a
predict on each.

# Submission
Replace the return values in `__init__.py` with predictions from your models.
Avoid running "on-the-fly" computations or scripts in this file. Ideally you
should load your pickled model from file (in the global scope) then call
`model.predict(line)`.

# Questions

## month_hour_model
There are two ways to handle seasonality.  Seasonality features are nice
because they are good at projecting arbitrarily far into the future.

The simplest (and perhaps most robust) is to have a set of indicator variables
for each month. That is to say, make the assumption that the temperature at any
given time is a function of only the month of the year, and the hour of the
day, and use that to predict the temperature value.  As you can imagine, the
temperature values will be stripped out in the actual text records that are
passed.

**Question**: Should month be a continuous or categorical variable?


## fourier_model
Since we know that temperature is roughly sinusoidal, we know that a reasonable
model might be

    $$ y_t = y_0 \sin(2\pi\frac{t - t_0}{T}) + \epsilon $$

where $k$ and $t_0$ are parameters to be learned and $T$ is one year for
seasonal variation.  While this is linear in $y_0$, it is not linear in $t_0$.
However, we know from Fourier analysis, that the above is
equivalent to

    $$ y_t = A \sin(2\pi\frac{t}{T}) + B \cos(2\pi\frac{t}{T}) + \epsilon $$

which is linear in $A$ and $B$.

Create a model containing sinusoidal terms on one or more time scales,
and fit it to the data using a linear regression.

