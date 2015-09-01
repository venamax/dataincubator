The city of New York does restaurant inspections and assigns a grade.
Inspections data the last 4 years are available
[here](https://s3.amazonaws.com/thedataincubator/coursedata/nyc_inspection_data.zip).

The file `RI_Webextract_BigApps_Latest.xls` contains a description of each of
the datafiles.  Take a look and then load the csv formatted `*.txt` files into
Postgresql into five tables:
1. `actions`
2. `cuisines`
3. `violations`
4. `grades` (from `WebExtract.txt`)
5. `boroughs` (from `RI_Webextract_BigApps_Latest.xls`)

# Hints
1. It is recommended to use sqlite3 for this project. Postgresql can work but
   will be more difficult to set up properly on Digital Ocean. If you do use
   sqlite, in order to do mathematical calculations like square root, you will
   need to compile and install the extension described on the
   [wiki](https://sites.google.com/a/thedataincubator.com/the-data-incubator-wiki/course-information-and-logistics/getting-started/setup).
2. Sqlite3 has a convenient .import function which can create tables from .csv .
   You may want to set up your databases using the sqlite shell, then use Python
   just to run the SELECT queries.

   Postgresql has an equivalent [`\copy`
   command](http://www.postgresql.org/docs/9.2/static/app-psql.html#APP-PSQL-META-COMMANDS-COPY)
   that can both save and load files in various formats.  It is a convenience
   wrapper for the [`copy`
   command](http://www.postgresql.org/docs/9.2/static/sql-copy.html) but
   behaves better (e.g. relative paths).
3. The files may contain malformatted text.  Unfortunately, this is all too
   common.  As a stop gap, remember that `iconv` is a unix utility that can
   convert files between different text encodings.
4. For more sophisticated needs, a good strategy is to write simple python
   scripts that will reparse files.  For example, commas (',') within a single
   field will trick many csv parsers into breaking up the field.  Write a
   python script that converts these 'inadvertent' delimiters into semicolons
   (';').

# Questions

## score_by_zipcode
Return a list of tuples of the form:
```
    (zipcode, mean grade, standard error, number of inspections)
```
for each of the 184 zipcodes in the city with over 100 inspections. Sort the
list in ascending order by mean grade. You can read more about standard error
on [wikipedia](http://en.wikipedia.org/wiki/Standard_error).

**Checkpoint**
Total entries in valid zipcodes: 531,126

## score_by_map
The above are not terribly enlightening.  Use [CartoDB](http://cartodb.com/)
to produce a map of average scores by zip code.  You can sign up for a free
trial.

You will have to use their wizard to plot the data by
[zipcode](http://docs.cartodb.com/cartodb-editor.html#geocoding-data).  Then
use the "share" button to return a link to a short URL beginning with
"http://cdb.io/".

**For fun:** How do JFK, Brighton Beach, Liberty Island (home of the Statue of
Liberty), Financial District, Chinatown, and Coney Island fare?

## score_by_borough
Return a list of tuples of the form:
    ```
    (borough, mean grade, stderr, number of inspections)
    ```
for each of the city's five boroughs. Sort the list in ascending order by grade.

**Hint**: you will have to perform a join with the `boroughs` table.

**Checkpoint**
Total entries in valid boroughs: 531,832

## score_by_cuisine
Return a list of the 75 tuples of the form
    ```
    (cuisine, mean grade, stderr, number of inspections)
    ```
for each of the 75 cuisine types with at least 100 inspections. Sort the list 
in ascending order by score. Are the least sanitary and most sanitary cuisine
types surprising?

**Checkpoint**
Total entries from valid cuisines: 531,529

## violation_by_cuisine
Which cuisines tend to have a disproportionate number of what which violations?
Answering this question isn't easy becuase you have to think carefully about
normalizations.

1. More popular cuisine categories will tend to have more violations just
   becuase they represent more restaurants.
2. Similarly, some violations are more common.  For example, knowing that
   "Equipment not easily movable or sealed to floor" is a common violation for
   Chinese restuarants is not particularly helpful when it is a common
   violation for all restaurants.

The right quantity is to look at is the conditional probability of a specific
type of violation given a specific cuisine type and divide it by the
unconditional probability of the violation for the entire population. Taking
this ratio gives the right answer.  Return the 20 highest ratios of the form:
    ```
        ((cuisine, violation), ratio, count)
    ```

**Hint**:
1. You might want to check out this [Stackoverflow
   post](http://stackoverflow.com/questions/972877/calculate-frequency-using-sql).
2. The definition of a violation changes with time.  For example, 10A can mean
   two different things "Toilet facility not maintained ..." or "Vermin or
   other live animal present ..." when things were prior to 2003. To deal with
   this, you should limit your analysis to violations with end date after Jan 1,
   2014.
3. The ratios don't mean much when the number of violations of a given type and
   for a specific category are not large (why not?).  Be sure to filter these
   out.  We chose 100 as our cutoff.

**Checkpoint**:
Top 20 ratios mean: 1.95724597861122
