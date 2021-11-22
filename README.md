# Predicting 2021 Cy Young Awards

<h3 align="left">Goals:</h3>

__Non-technical:__ What pitching statistics are the best predictors
for who wins the Cy Young.

__Technical:__ Given a dataset (such as the one below), 
what combination of features generates a Linear Regression model with the highest accuracy (in terms of R2 Score).

<img src="images/dataset.png" width="400" class="center"/>

----

<h3 align="left">Tasks to accomplish goals:</h3>

* Generate a dataset
* Generate a subset of the dataset
* Fit each subset to a linear regression model
* Calculate accuracy (R2 Score) of each model
* Choose the model with the highest score

<h3 align="left">The issue we face:</h3>

Let's say our dataset has __15__ variables, and we want to generate all combinations of __8__

<img src="images/combinations.png" width="300"/>

This means we will have __6,435__ subsets of the dataset. This will require
extensive runtime to compute.

----

<img src="images/speedup.png" width="650"/>

----

<img src="images/breakdown1.png" width="750"/>
<img src="images/breakdown2.png" width="750"/>

## Getting Started:

To run the program locally, execute the following lines into terminal:

```sh
$ git clone https://github.com/JackMentch/cy_young_regression.git
$ cd cy_young_regression
$ python -m venv cy_young_regression
$ pip install -r requirements.txt
```

Once the program is ready you can then run
```sh
$ python main.py
```

## Future Work to Improve Model:
- Normalize the dataset that we feed to the algorithm
  

- Cy Young votes are based on what league you play in. 
  In theory, a pitcher could be in the 90th percentile
  in MLB but be in the 99th percentile of the National/American League.
  Votes are dependent on a pitcher's respective league competition. The model should account for this.
  

- Regression Splines - Since the model is linear, players in the bottom percentile can receive negative
Cy Young votes. Regression spline can ensure more accurate estimations for players in any percentile.


## Credits:
- Baseball-Reference.com for generating the dataset
- Sklearn for the linear regression toolkit
