import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from filtering import filter
import numpy
import matplotlib.pyplot as plt
from players import *

class Model():
    def __init__(self, pct, ml, x_train, x_test, y_train, y_test):
        self.pct = pct
        self.ml = ml
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test

    def accuracy(self):

        y_pred = self.ml.predict(self.x_test)

        # r2_score calculates the performance of model based on the total sum of error, and the sum of squares
        # of the residual errors

        # r2_score = 1 - (sum of squares of the residual errors)/(total sum of errors)

        # residual is the vertical distance between a data point and the regression line

        return r2_score(self.y_test, y_pred)


df = pd.read_csv('data.csv')

# Before filtering the dataset, there are 1671 rows in the dataframe
# 1383 of these rows recieved 0 votes for the CY Young, this is heavily biasing the data

# So first we shuffle the dataframe, so there is no bias
df = df.sample(frac=1)

list_of_models = []

# we will test 10 different models, when pct is 0, that means we leave all the pitchers in the dataset that
# received 0 votes. When pct is 1, we remove all pitchers that received 0 votes. We need to find for what pct
# does our model perform the best?
for pct in numpy.arange(0,1,0.1):

    pct = round(pct,1)

    # filter function removes a percentage (pct) of rows where the pitcher received 0 votes
    df = filter(column_name='votes', filter_out=0, df=df, pct=pct)

    # drop the votes column in our table because that is our label
    # drop player_id
    x = df.drop(['votes', 'player_id'],axis=1).values

    # y will contain all the labels that match up to the x dataset
    y = df['votes'].values

    # split our dataset into training and testing.
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3, random_state=0)

    ml = LinearRegression()

    ml.fit(x_train, y_train)

    list_of_models.append(Model(ml=ml, pct=pct, x_train= x_train, x_test= x_test, y_train= y_train, y_test= y_test))


plt.title('Filtering vs Performance')
plt.xlabel('% of Players w/ 0 votes removed from dataset')
plt.ylabel('Model Performance')


# We now have 10 model objects stored in our list_of_models, we need to find out which had the best performance
# and use it to make estimations

best_performing_model_accuracy = 0
best_performing_model = None

for model in list_of_models:

    model_accuracy = model.accuracy()

    plt.scatter(model.pct,  model_accuracy, s=40)

    if model_accuracy > best_performing_model_accuracy:
        best_performing_model = model
        best_performing_model_accuracy = model_accuracy

print(f"Optimal Model Accuracy: {best_performing_model.accuracy()}\n")

# With the best performing model, we will estimate how many votes each player will get
gerrit_cole = list(gerrit_cole.values())
zack_wheeler = list(zack_wheeler.values())
jake_arrieta = list(jake_arrieta.values())
lance_lynn = list(lance_lynn.values())
corbin_burnes = list(corbin_burnes.values())
aaron_nola = list(aaron_nola.values())
max_scherzer = list(max_scherzer.values())
robbie_ray = list(robbie_ray.values())

print(f"2021 Expected Gerrit Cole CY Young Votes: {int(best_performing_model.ml.predict([gerrit_cole])[0])}")
print(f"2021 Expected Zack Wheeler CY Young Votes: {int(best_performing_model.ml.predict([zack_wheeler])[0])}")
print(f"2021 Expected Jake Arrieta CY Young Votes: {int(best_performing_model.ml.predict([jake_arrieta])[0])}")
print(f"2021 Expected Lance Lynn CY Young Votes: {int(best_performing_model.ml.predict([lance_lynn])[0])}")
print(f"2021 Expected Corbin Burnes CY Young Votes: {int(best_performing_model.ml.predict([corbin_burnes])[0])}")
print(f"2021 Expected Aaron Nola CY Young Votes: {int(best_performing_model.ml.predict([aaron_nola])[0])}")
print(f"2021 Expected Max Scherzer CY Young Votes: {int(best_performing_model.ml.predict([max_scherzer])[0])}")
print(f"2021 Expected Robbie Ray CY Young Votes: {int(best_performing_model.ml.predict([robbie_ray])[0])}")


coefficients = zip(list(df.drop(['votes', 'player_id'],axis=1).columns), best_performing_model.ml.coef_)

# Print out the coefficient of each variable to see which variable hold the most weight
print(f"\nCoeff: {list(coefficients)}")

plt.show()



