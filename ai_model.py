import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

# Sample training data (service_type, customers in queue, avg_service_time)
data = np.array([
    [1, 10, 5],  # Service Type 1, 10 people, 5 min avg
    [2, 5, 8],   # Service Type 2, 5 people, 8 min avg
    [3, 7, 6],   # Service Type 3, 7 people, 6 min avg
])

df = pd.DataFrame(data, columns=['service_type', 'customers', 'avg_time'])
X = df[['service_type', 'customers']]
y = df['avg_time']

model = LinearRegression()
model.fit(X, y)

def predict_wait_time(service_type, num_people):
    return model.predict([[service_type, num_people]])[0]
