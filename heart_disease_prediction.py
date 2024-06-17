import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from joblib import dump, load

try:
    data = pd.read_csv("D:/XAMPP/htdocs/Flask_website/data/Heart_disease_data.csv")
    print("Data loaded successfully")
    print(data.head())  # Print the first few rows of the data frame
except Exception as e:
    print("Error loading data:", e)
    
data = pd.read_csv("D:/XAMPP/htdocs/Flask_website/data/Heart_disease_data.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

# Step 2: Model Training
model = LinearRegression()
model.fit(x, y)

# Step 3: Save the Trained Model
model_path = "D:/XAMPP/htdocs/Flask_website/data/model.joblib"
dump(model, model_path)

# Step 4: Load the Model
loaded_model = load(model_path)

# Step 5: Predict New Data
# Now, you can use the loaded model to predict a new patient's condition
age = int(input('Enter the patient age: '))
sex = int(input("Enter the sex: "))
cp = int(input('Enter the cp: '))
trestbps = int(input('Enter the trestbps: '))
chol = int(input('Enter the chol: '))
fbs = int(input('Enter the fbs: '))
restecg = int(input('Enter the restecg: '))
thalach = int(input('Enter the thalach: '))

new_data = loaded_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach]])

# Step 6: Predict Patient's Condition
if np.round(new_data) == 0:
    print("No heart disease")
else:
    print("Heart disease")
