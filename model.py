from sklearn.metrics import r2_score

# Defines a model object for each individual linear regression model
class Model():
    def __init__(self, pct, ml, x_train, x_test, y_train, y_test, columns):
        self.pct = pct
        self.ml = ml
        self.x_train = x_train
        self.x_test = x_test
        self.y_train = y_train
        self.y_test = y_test
        self.columns = columns

    def accuracy(self):

        y_pred = self.ml.predict(self.x_test)

        # r2_score calculates the performance of model based on the total sum of error, and the sum of squares
        # of the residual errors

        # r2_score = 1 - (sum of squares of the residual errors)/(total sum of errors)

        # residual is the vertical distance between a data point and the regression line

        return r2_score(self.y_test, y_pred)
