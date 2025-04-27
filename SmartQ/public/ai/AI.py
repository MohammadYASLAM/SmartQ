import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np
from sklearn.linear_model import LinearRegression

# Initialize Firebase
cred = credentials.Certificate('path/to/your/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()

def calculate_wait_time(queue_id):
    queue_ref = db.collection('queues').document(queue_id)
    queue_data = queue_ref.get().to_dict()
    
    if queue_data:
        wait_times = queue_data['waitTimes']
        
        if len(wait_times) > 1:
            # Use the last few wait times to predict
            X = np.array(range(len(wait_times))).reshape(-1, 1)
            y = np.array(wait_times)
            
            model = LinearRegression()
            model.fit(X, y)
            
            predicted_wait_time = model.predict([[len(wait_times) + 1]])  # Predict for next position
            return predicted_wait_time[0]
    
    return 0  # Default if no data

def update_estimated_wait_time(queue_id):
    predicted_time = calculate_wait_time(queue_id)
    db.collection('queues').document(queue_id).update({
        'estimatedWaitTime': predicted_time
    })
    print(f"Updated estimated wait time for {queue_id}: {predicted_time} minutes")
