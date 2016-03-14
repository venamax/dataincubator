# Project Title

Music offers an extremely rich and interesting playing field. The objective of this miniproject is to develop models that are able to recognize the genre of a musical piece, starting from the raw waveform or from pre-computed features. This is a typical example of a classification problem on time series data.

The model will be assessed based on the accuracy score of your classifier.  There is a reference solution.  The reference solution has a score of 1. *(Note that this doesn't mean that the accuracy of the reference solution is 1)*.

## Instructions for accessing the data

Raw audio files with music pieces can be found [here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/music_train.tar.gz).

The music belongs to one for each genres:
- electronic
- folkcountry
- jazz
- raphiphop
- rock

Mapping of filename to genre for the **training set** is found [here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/music_train_labels.csv)

Raw audio **test set** can be found [here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/music_feature_extraction_test.tar.gz).

These files are randomized and anonymized.

An additional dataset of pre-computed features can be found [here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/df_train_anon.csv).

*Hints*
- All songs are sampled at 44100 Hz.


## Submission instructions

For the questions involving predicting genre from raw audio files (Questions 1 & 2), you will need to run your model on the test set provided and submit your predictions as a static file. This is a dictionary of the form:

    {
    "fe_test_0001.mp3":"electronic",
    "fe_test_0002.mp3":"rock",
    ....
    }

Replace the default values in `__init__.py` with your answers. Avoid running "on-the-fly" computations or scripts in the file. The less moving parts there are, the easier it is on the grader.

For the question involving building a model on the pre-computed features (Question 3), you will need to package your model with the solution in the same way as in the ML miniproject.

# Questions

## Question 1 (these names should match the functions in `__init__.py`)
## Raw Features Predictions
The simplest features that can be extracted from a music time series are the [zero crossing rate](https://en.wikipedia.org/wiki/Zero-crossing_rate) and the [root mean square energy](https://en.wikipedia.org/wiki/Root_mean_square).

1) Build a function or a transformer that calculates these two features starting from a raw file input.
In order to go from a music file of arbitrary length to a fixed set of features you will need to use a sliding window approach, which implies making the following choices:

1) what window size are you going to use?
2) what's the overlap between windows?

Besides that, you will need to decide how you are going to summarize the values of such features for the whole song. Several strategies are possible:
-  you could decide to describe their statistics over the whole song by using descriptors like mean, std and higher order moments
-  you could decide to split the song in sections, calculate statistical descriptors for each section and then average them
-  you could decide to look at the rate of change of features from one window to the next (deltas).
-  you could use any combination of the above.

Your goal is to build a transformer that will output a "song fingerprint" feature vector that is based on the 2 raw features mentioned above. This vector has to have the same size, regardless of the duration of the song clip it receives.

2) Train an estimator that receives the features extracted by the transformer and predicts the genre of a song.

Use Scikit-Learn [LabelEncoder](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) to generate your own encoding for the labels.

Use this pipeline to predict the genres for the 145 files in the `music_feature_extraction_test.tar.gz` set and submit your predictions as a dictionary in the `__init__.py` file.

*Hints*
- Extracting features from time series can be computationally intensive. Make sure you choose wisely which features to calculate.
- You can use MRJob or PySpark to distribute the feature extraction part of your model and then train an estimator on the extracted features.


## Question 2
## All Features Predictions
The approach of question 1 can be generalized to any number and kind of features extracted from a sliding window. Use the [librosa library](http://bmcfee.github.io/librosa/) to extract features that could better represent the genre content of a musical piece.
You could use:
- spectral features to capture the kind of instruments contained in the piece
- MFCCs to capture the variations in frequencies along the piece
- Temporal features like tempo and autocorrelation to capture the rythmic information of the piece
- features based on psychoacoustic scales that emphasize certain frequency bands.
- any combination of the above

As for question 1, you'll need to summarize the time series containing the features using some sort of aggregation. This could be as simple as statistical descriptors or more involved, your choice.

As a general rule, build your model gradually. Choose few features that seem interesting, calculate the descriptors and generate predictions.

Make sure you `GridSearchCV` the estimators to find the best combination of parameters.

Use this pipeline to predict the genres for the 145 files in the `music_feature_extraction_test.tar.gz` set and submit your predictions as a static list in the `__init__.py` file.

**Question:**
Does your transformer make any assumption on the time duration of the music piece? If so how could that affect your predictions if you receive longer/shorter pieces?

This model works very well on 1 of the classes. Which one? Why do you think that is?

## Question 3
## All Features Model
The `df_train_anon.csv` file contains 549 pre-computed features for the training set. The last column contains the genre.

Build a model to generate predictions from this featureset. Steps in the pipeline could include:

- a normalization step (not all features have the same size or distribution)
- a dimensionality reduction or feature selection step
- ... any other transformer you may find relevant ...
- an estimator
- a label encoder inverse transform to return the genre as a string

Use GridSearchCV to find the scikit learn estimator with the best cross-validated performance and sumbit it as a packaged model.

*Hints*
- Use a dimensionality reduction technique (e.g. PCA) or a feature selection criteria when possible.
- Use GridSearchCV to improve score.
- The model needs to return the genre as a string. You'll need to create a wrapper class around scikit-learn estimators in order to do that.
