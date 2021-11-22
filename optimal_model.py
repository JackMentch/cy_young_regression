import numpy
from sklearn.linear_model import LinearRegression
from model import Model
from sklearn.model_selection import train_test_split
from filtering import filter

def optimal_model(df):

    # So first we shuffle the dataframe, so there is no bias
    df = df.sample(frac=1)

    list_of_models = []

    # we will test 10 different models, when pct is 0, that means we leave all the pitchers in the dataset that
    # received 0 votes. When pct is 1, we remove all pitchers that received 0 votes. We need to find for what pct
    # does our model perform the best?
    for pct in numpy.arange(0, 1, 0.1):
        pct = round(pct, 1)

        # filter function removes a percentage (pct) of rows where the pitcher received 0 votes
        df = filter(column_name='votes', filter_out=0, df=df, pct=pct)

        # drop the votes column in our table because that is our label
        # drop player_id
        x = df.drop(['votes', 'player_id'], axis=1).values

        # y will contain all the labels that match up to the x dataset
        y = df['votes'].values

        # split our dataset into training and testing.
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

        ml = LinearRegression()

        ml.fit(x_train, y_train)

        list_of_models.append(Model(ml=ml, pct=pct, x_train=x_train, x_test=x_test, y_train=y_train, y_test=y_test, columns=df.columns.values.tolist()))

    # We now have 10 model objects stored in our list_of_models, we need to find out which had the best performance
    # and use it to make estimations

    best_performing_model_accuracy = 0
    best_performing_model = None

    for model in list_of_models:

        model_accuracy = model.accuracy()

        if model_accuracy > best_performing_model_accuracy:
            best_performing_model = model
            best_performing_model_accuracy = model_accuracy

    return best_performing_model