import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

data = pd.read_csv('../../data.csv')
X = data.drop('Power', axis = 1)
X = X.drop('Time', axis = 1)
data = data.drop('Time', axis = 1)
lm = LinearRegression()
lm.fit(X, data.Power)
print("coefficients: ")
print(lm.coef_)
print("intercept:")
print(lm.intercept_)
mse = np.mean((data.Power - lm.predict(X))**2)
print("Mse:")
print(mse)
print("rsquared:")
print(lm.score(X, data.Power))
