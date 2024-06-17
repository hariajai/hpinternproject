from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, median_absolute_error, explained_variance_score, r2_score
from joblib import load

app = Flask(__name__)
app.secret_key = "b'\xa7P\xc59k\xc6\x84:\x03\x82\x03\xa6\x0b\xefl\r\xb9\x8b\xbe\xec\x89pz\x86'"

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'hphar'
app.config['MYSQL_PASSWORD'] = 'hari'
app.config['MYSQL_DB'] = 'flask_app'

mysql = MySQL(app)

# Load model and calculate metrics once
model = load('model.joblib')

# Load data to calculate accuracy metrics
data = pd.read_csv("Heart_disease_data.csv")
x = data.iloc[:, :-1].values
y = data.iloc[:, -1].values
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Calculate predictions for test data
y_predict = model.predict(x_test)

# Calculate metrics
metrics = {
    "mae": round(mean_absolute_error(y_test, y_predict)*2, 2),
    "mse": round(mean_squared_error(y_test, y_predict)*2, 2),
    "median_ae": round(median_absolute_error(y_test, y_predict)*2, 2),
    "evs": round(explained_variance_score(y_test, y_predict)*2, 2),
    "r2": round(r2_score(y_test, y_predict)*2,2)
}

@app.route('/show_accuracy', methods=['POST'])
def show_accuracy():
    flash('Accuracy metrics displayed!', 'success')
    return render_template('prediction_result.html', condition=session['condition'], metrics=metrics)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        # Check if the user already exists
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Email address already registered', 'error')
            cursor.close()
            return redirect(url_for('register'))

        cursor.execute("INSERT INTO user (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, password))
        mysql.connection.commit()
        cursor.close()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user'] = user[1]  # Assuming username is the second field in the user table
            flash('Login successful!', 'success')
            return redirect(url_for('patient_details'))
        else:
            flash('Invalid email or password', 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout',methods=["GET","POST"])
def logout():
    if request.method=="POST":
        return render_template('home.html')

@app.route('/learn_more')
def learn_more():
    return render_template('learn_more.html')

@app.route('/get_started')
def get_started():
    return render_template('get_started.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

@app.route('/patient_details', methods=['GET', 'POST'])
def patient_details():
    if request.method == 'POST':
        age = request.form['age']
        sex = request.form['sex']
        cp = request.form['cp']
        trestbps = request.form['trestbps']
        chol = request.form['chol']
        fbs = request.form['fbs']
        restecg = request.form['restecg']
        thalach = request.form['thalach']

        new_data = model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach]])

        if np.round(new_data) == 0:
            condition = "No Heart Disease"
        else:
            condition = "Heart Disease"

        session['condition'] = condition

        flash('Predicted successfully!', 'success')
        return render_template('prediction_result.html', condition=condition, metrics=metrics)

    if 'user' in session:
        return render_template('patient_details.html')
    else:
        return redirect(url_for('login'))

@app.route('/prediction_result', methods=['POST'])
def prediction_result():
    if request.method == 'POST':
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        cp = int(request.form['cp'])
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = int(request.form['fbs'])
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])

        new_data = model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach]])

        if np.round(new_data) == 0:
            condition = "No Heart Disease"
        else:
            condition = "Heart Disease"

        session['condition'] = condition

        
        return render_template('prediction_result.html', condition=condition, metrics=metrics)

    return redirect(url_for('home'))  # Redirect if not a POST request

if __name__ == '__main__':
    app.run(debug=True)
