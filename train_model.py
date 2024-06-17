import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load the CSV file
data = pd.read_csv("Heart_disease_data.csv")  # Replace "your_file.csv" with the path to your CSV file

# Preprocess the data as needed

# Split the data into features (X) and target variable (y)
X = data.drop(columns=["target"])
y = data["target"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
score = model.score(X_test, y_test)
print("Model Score:", score)
