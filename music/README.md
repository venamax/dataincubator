# Project Title

From the point of view of data analysis, music offers an extremely rich and interesting playing field. The objective of this miniproject is to develop models that are able to recognize the genre of a musical piece, starting from the raw waveform or from pre-computed features. This is a typical example of a classification problem on time series data.

The model will be assessed based on the accuracy score of your classifier.  There is a reference solution.  The reference solution has a score of 1.

## Instructions for accessing the data

Raw audio files with music pieces can be found [here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/music_train.tar.gz).

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

Use the folder name as the genre label you are attempting to predict.

Raw audio test files can be found [here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/music_test.tar.gz).

These files are randomized and anonymized.

An additional dataset of pre-computed features can be found [here](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/music_features_train.tar.gz).

*Hints*
- All songs are sampled at 22050 Hz.
- Extracting features from time series can be computationally intensive. Make sure you select which features to calculate wisely.
- You can use MRJob or PySpark to distribute the feature extraction part of your model
- Use a dimensionality reduction technique (e.g. PCA) or a feature selection criteria when possible
- Use GridSearchCV to improve score

## Submission instructions

For the questions involving building a model on raw audio files, you will need to run your model on the test set provided and submit your predictions as a static file. 
Replace the default values in `__init__.py` with your answers. Avoid running "on-the-fly" computations or scripts in the file. The less moving parts there are, the easier it is on the grader.

For the questions involving building a model on the pre-computed features, you will need to package your model with the solution in the same way as in the ML miniproject.

# Questions

## Question 1 (these names should match the functions in `__init__.py`)
## Raw Features Predictions
The simplest features that can be extracted from a music time series are the [zero crossing rate](https://en.wikipedia.org/wiki/Zero-crossing_rate) and the [root mean square energy](https://en.wikipedia.org/wiki/Root_mean_square).

1) Build a transformer that calculates these two features starting from a raw file input.
In order to go from a music file of arbitrary length to a fixed set of features you will need to use a sliding window approach, which implies making the following choices:
- what window size are you going to use?
- what's the overlap between windows?

Besides, you will need to decide how you are going to summarize the values of such features for the whole song. Several strategies are possible:
-  you could decide to describe their statistics over the whole song by using descriptors like mean, std and higher order moments
-  you could decide to split the song in sections, calculate statistical descriptors for each section and then average them
-  you could decide to look at the rate of change of features from one window to the next (deltas).
-  you could use any combination of the above.

Your goal is to build a transformer that will output a "song fingerprint" feature vector that is based on the 2 raw features mentioned above. This vector has to have the same size, regardless of the duration of the song clip it receives.

2) Train an estimator that receives the features extracted by the transformer and predicts the genre of a song.

Feel free to encode the songs with the following map:

```python
genremap = {'blues': 0,
            'classical': 1,
            'country': 2,
            'disco': 3,
            'hiphop': 4,
            'jazz': 5,
            'metal': 6,
            'pop': 7,
            'reggae': 8,
            'rock': 9}
```

or use Scikit-Learn [LabelEncoder](http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) to generate your own encoding.

Use this pipeline to predict the genres for the 100 files in the `music_test.tar.gz` set and submit your predictions as a static list in the `__init__.py` file.


## Question 2
## All Features Predictions
The approach of question 1 can be generalized to any number and kind of features extracted from a sliding window. Use the power of the [librosa library](http://bmcfee.github.io/librosa/) to extract features that could better represent the genre content of a musical piece.
You could use:
- spectral features to capture the kind of instruments contained in the piece
- MFCCs to capture the variations in frequencies along the piece
- Temporal features like tempo and autocorrelation to capture the rythmic information of the piece
- features based on psychoacoustic scales that emphasize certain frequency bands.
- wavelet based features
- any combination of the above

As for question 1, you'll need to summarize the time series containing the features using some sort of aggregation. This could be as simple as statistical descriptors or more involved. Your choice.

As a general rule, build your model gradually. Choose few features that seem interesting, calculate the descriptors and generate predictions.

Make sure you `GridSearchCV` the estimators to find the best combination of parameters.

Use this pipeline to predict the genres for the 100 files in the `music_test.tar.gz` set and submit your predictions as a static list in the `__init__.py` file.

**Question:**
Does your transformer assume a certain duration for the music piece? If so how could that affect your predictions if you receive longer/shorter pieces?

This model works very well on 1 of the classes. Which one? Why do you think that is?

## Question 3
## All Features Model
The `music_features_train.tar.gz` set contains 549 pre-computed features for the the training set. The last two columns contain the genre and the encoded class label.

Build a pipeline to generate predictions from this featureset. Steps in the pipeline could include:

- a normalization step (not all features have the same size or distribution)
- a dimensionality reduction or feature selection step
- ... any other transformer you may find relevant ...
- an estimator

Use GridSearchCV to find the scikit learn estimator with the best cross-validated performance and sumbit it as a packaged model.

Your model should output the correct label in text.