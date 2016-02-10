# Project Title

Music is a very popular and rich source of information. Our objective is to develop a model that is able to recognize the genre of a musical piece, starting from the raw waveform. This is a typical example of a classification problem on time series data.

Your model will be assessed based on the accuracy score of your classifier.  There is a reference solution (which should not be too hard to beat).  The reference solution has a score of 1.

## Instructions for accessing the data

Data can be found here[here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/music_train.tar.gz)

The data is organized in 10 folders, one for each genre:
- blues
- classical
- country
- disco
- hiphop
- jazz
- metal
- pop
- reggae
- rock

## Hints

- Extracting features from time series can be time consuming
- Use MRJob to distribute the feature extraction part of your model when you have lots of features to train on
- Use PCA when possible
- Use GridSearchCV to improve score
- Think of music data as np array

### Example workflow

### Tips and recommendations

## Submission instructions

Here is some boilerplate to start with:
Replace the default values in `__init__.py` with your answers. Avoid running
"on-the-fly" computations or scripts in the file. The less moving parts there
are, the easier it is on the grader.

For modeling questions include information on pickling and unpickling models.

# Questions

## Question 1 (these names should match the functions in `__init__.py`)
## Raw Features Model
The simplest features that can be extracted from a music time series are the zero crossing rate and the root mean square energy.
1) Build a transformer that calculates these two features starting from a raw file input.
In order to go from a music file of arbitrary length to a fixed set of features you will need to use a sliding window approach, which involves few choices:
- how large is the window you're going to consider?
- what's the overlap between windows?
- how do you summarize the values of your features for the whole song? (you could take the mean, or the standard deviation, or the deltas or any other combination).

Your goal is to build a transformer that will output a feature vector that has always the same size, independently of the length of the song clip it receives.

2) Train an estimator that receives the features extracted by the transformer and predicts the genre of a song. You will need to use LabelEncoder in order to 


**Checkpoint**
Checkpoint 1: x
Checkpoint 2: y
Checkpoint 3: z

## Question 2

## Question 3





--------------------------



The venues belong to different cities.  You can image that the ratings in some
cities are probably higher than others and use this as an estimator.

Build an estimator that uses `groupby` and `mean` to compute the
average rating in that city.  Use this as a predictor.

**Question:** In the absence of any information about a city, what score would
you assign a restaurant in that city?

**Note:** `def city_model` etc. takes an argument `record`.

## lat_long_model
You can imagine that a city-based model might not be sufficiently fine-grained.
For example, we know that some neighborhoods are trendier than others.  We
might consider a K Nearest Neighbors or Random Forest based on the latitude
longitude as a way to understand neighborhood dynamics.

You should implement a generic `ColumnSelectTransformer` that is passed which
columns to select in the transformer and use a non-linear model like
`sklearn.neighbors.KNeighborsRegressor` or
`sklearn.ensemble.RandomForestRegressor` as the estimator (why would you choose
a non-linear model?).  Bonus points if you wrap the estimator in
`grid_search.GridSearchCV` and use cross-validation to determine the optimal
value of the parameters.

## category_model
While location is important, we could also try seeing how predictive the
venues' category. Build a custom transformer that massages the data so that it
can be fed into a `sklearn.feature_extraction.DictVetorizer` which in turn
generates a large matrix gotten by One-Hot-Encoding.  Feed this into a Linear
Regression (and cross validate it!).  Can you beat this with another type of
non-linear estimator?

*Hints*:
  - With a large sparse feature set like this, we often use a cross-validated
    regularized linear model.
  - Some categories (e.g. Restaurants) are not very specific.  Others (Japanese
    sushi) are much more so.  How can we account for this in our model (*Hint:*
    look at TF-IDF).

## attribute_knn_model
Venues have (potentially nested) attributes:
```
    {'Attire': 'casual',
     'Accepts Credit Cards': True,
     'Ambience': {'casual': False, 'classy': False}}
```

Categorical data like this should often be transformed by a One Hot Encoding.
For example, we might flatten the above into something like this:

```
    {'Attire_casual' : 1,
     'Accepts Credit Cards': 1,
     'Ambience_casual': 0,
     'Ambience_classy': 0 }
```

Build a custom transformer that flattens attributes and feed this into
`DictVectorizer`.  Feed it into a (cross-validated) linear model (or something
else!)


## full_model
So far we have only built models based on individual features.  We could
obviously combine them.  One (highly recommended) way to do this is through a
`sklearn.pipelline.FeatureUnion`.

Combine all the above models using a feature union.  Notice that a feature
union takes transformers, not models as arguements.  The way around this is to
build a transformer that outputs the prediction in the transform method, thus
turning the model into a transformer.  Use a cross-validated linear regression
(or some other algorithm) to weight these signals.
