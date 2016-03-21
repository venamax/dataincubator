# Overview

Unstructured data makes up the vast majority of data.  This is a basic intro to
handling unstructured data.  Our objective is to be able to extract the
sentiment (positive or negative) from review text.  We will do this from Yelp
review data.

Your model will be assessed based on how root mean squared error of the number
of stars you predict.  There is a reference solution (which should not be too
hard to beat) that defines the score of 1.

The data is available at on
[S3](http://thedataincubator.s3.amazonaws.com/coursedata/mldata/yelp_train_academic_dataset_review.json.gz).


## Helpful notes:
- You may run into trouble with the size of your models and Digital Ocean's
  memory limit. This is a major concern in real-world applications. Your
  production environment will likely not be that different from Digital Ocean
  and being able to deploy there is important and companies don't want to hire
  data scientists who cannot cope with this. Think about what information the
  different stages of your pipeline need and how you can reduce the memory
  footprint.
- For example, submitting entire GridSearchCV objects will not work reliably
  depending on the size of your models. If you use GridSearchCV, consult the
  documentation to find the attributes that allow you to extract the best
  estimator and/or parameters. (Remember to retrain on the entire dataset
  before submitting).

# Submission
Replace the return values in `__init__.py` with predictions from your models.
Avoid running "on-the-fly" computations or scripts in this file. Ideally you
should load your pickled model from file (in the global scope) then call
`model.predict(record)`.

# Questions

Note that all functions take an argument `record`. Samples of `record` are
given in `test_json.py`. Your model will be passed a single record during
grading.

## bag_of_words_model
Build a linear model based on the count of the words in each document
(bag-of-words model).

**Hints**:
1. Don't forget to use tokenization!  This is important for good performance
   but it is also the most expensive step.  Try vectorizing as a first initial
   step:
   ```Python
       X = feature_extraction.text \
                             .CountVectorizer() \
                             .fit_transform(text)
       y = scores
   ```
   and then running grid-serach and cross-validation only on of this
   pre-processed data.  `CountVectorizer` has to memorize the mapping between
   words and the index to which it is assigned.  This is linear in the size of
   the vocabulary.  The `HashingVectorizer` does not have to remember this
   mapping and will lead to much smaller models.

2. Try choosing different values for `min_df` (minimum document frequency
   cutoff) and `max_df` in `CountVectorizer`.  Setting `min_df` to zero admits
   rare words which might only appear once in the entire corpus.  This is both
   prone to overfitting and makes your data unmanageably large.  Don't forget
   to use cross-validation or to select the right value.  Notice that
   `HashingVectorizer` doesn't support `min_df`  and `max_df`.  However, it's
   not hard to roll your own transformer that solves for these.

3. Try using `LinearRegression` or `RidgeCV`.  If the memory footprint is too
   big, try switching to Stochastic Gradient Descent
   (`sklearn.linear_model.SGDRegressor`) You might find that even ordinary
   linear regression fails due to the data size.  Don't forget to use
   `GridSearchCV` to determine the regularization parameter!  How do the
   regularization parameter `alpha` and the values of `min_df` and `max_df`
   from `CountVectorizer` change the answer?

## normalized_model
Normalization is key for good linear regression. Previously, we used the count
as the normalization scheme.  Try some of these alternative vectorizations:

1. You can use the "does this word present in this document" as a normalization
   scheme, which means the values are always 1 or 0.  So we give no additional
   weight to the presence of the word multiple times.

2. Try using the log of the number of counts (or more precisely, $log(x+1)$).
   This is often used because we want the repeated presence of a word to count
   for more but not have that effect tapper off.

3. [TFIDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) is a common
   normalization scheme used in text processing.  Use the `TFIDFTransformer`.
   There are options for using `idf` and taking the logarithm of `tf`.  Do
   these significantly affect the result?

Finally, if you can't decide which one is better, don't forget that you can
combine models with a linear regression.


## bigram_model
In a bigram model, let's consider both single words and pairs of consecutive
words that appear.  This is going to be a much higher dimensional problem
(large $p$) so you should be careful about overfitting.

Sometimes, reducing the dimension can be useful.  Because we are dealing with a
sparse matrix, we have to use `TruncatedSVD`.  If we reduce the dimensions, we
can use a more sophisticated models than linear ones.

As before, memory problems can crop up due to the engineering constraints.
Playing with the number of features, using the `HashingVectorizer`,
incorporating `min_df` and `max_df` limits, and handling stop-words in some way
are all methods of addressing this issue. If you are using `CountVectorizer`,
it is possible to run it with a fixed vocabulary (based on a training run, for
instance). Check the documentation.

**A side note on multi-stage model evaluation:** When your model consists of a
pipeline with several stages, it can be worthwhile to evaluate which parts of
the pipeline have the greatest impact on the overall accuracy (or other metric)
of the model. This allows you to focus your efforts on improving the important
algorithms, and leaving the rest "good enough".

One way to accomplish this is through ceiling analysis, which can be useful
when you have a training set with ground truth values at each stage. Let's say
you're training a model to extract image captions from websites and return a
list of names that were in the caption. Your overall accuracy at some point
reaches 70%. You can try manually giving the model what you know are the
correct image captions from the training set, and see how the accuracy improves
(maybe up to 75%). Alternatively, giving the model the perfect name parsing for
each caption increases accuracy to 90%. This indicates that the name parsing is
a much more promising target for further work, and the caption extraction is a
relatively smaller factor in the overall performance.

If you don't know the right answers at different stages of the pipeline, you
can still evaluate how important different parts of the model are to its
performance by changing or removing certain steps while keeping everything
else constant. You might try this kind of analysis to determine how important
adding stopwords and stemming to your NLP model actually is, and how that
importance changes with parameters like the number of features.

## food_bigrams
Look over all reviews of restaurants (you may need to look at the dataset from
`ml.py` to figure out which ones correspond to restaurants). We want to find
collocations --- that is, bigrams that are "special" and appear more often than
you'd expect from chance.  We can think of the corpus as defining an empirical
distribution over all ngrams.  We can find word pairs that are unlikely to
occur consecutively based on the underlying probability of their words.
Mathematically, if $p(w)$ be the probability of a word $w$ and $p(w_1 w_2)$ is
the probability of the bigram $w_1 w_2$, then we want to look at word pairs
$w_1 w_2$ where the statistic

  $$ p(w_1 w_2) / (p(w_1) * p(w_2)) $$

is high.  Return the top 100 (mostly food) bigrams with this statistic with
the 'right' prior factor (see below).

*Questions:* This statistic is a ratio and problematic when the denominator
is small.  We can fix this by applying Bayesian smoothing to $p(w)$
(i.e. mixing the empirical distribution with the uniform distribution over
the vocabulary).

1. How does changing this smoothing parameter affect the word pairs you get
   qualitatively?

2. We can interpret the smoothing parameter as adding a constant number of
   occurrences of each word to our distribution.  Does this help you determine
   set a reasonable value for this 'prior factor'?

3. For fun: also check out [Amazon's Statistically Improbable
   Phrases](http://en.wikipedia.org/wiki/Statistically_Improbable_Phrases).

*Implementation note:*
- The reference solution is not an aggressive filterer. Although there are
  definitely artifacts in the bigrams you'll find, many of the seemingly
  nonsensical words are actually somewhat meaningful.  Using smoothing
  parameters in the thousands or a high min_df might give you different
  results.
