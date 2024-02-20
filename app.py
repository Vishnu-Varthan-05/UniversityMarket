from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'vishnu',
    'password': 'vishnu',
    'database': 'university_market',
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# def create_tables():
#     connection = get_db_connection()
#     cursor = connection.cursor()
#     with app.open_resource('university_market.sql', mode='r') as f:
#         cursor.execute(f.read())
#     connection.commit()
#     cursor.close()
#     connection.close()

# create_tables()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home', methods=['POST'])
def login_post():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        username = request.form['username']
        password = request.form['password']
        
        query = "SELECT * FROM login WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            return render_template('welcome.html')
        else:
            return render_template('login.html', message="Invalid username or password")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            
            query = "SELECT * FROM login WHERE username = %s"
            cursor.execute(query, (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                return render_template('signup.html', message="Username already exists, please choose another one.")
            
            query = "INSERT INTO master_user (name, phone_number, email, status) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, phone, email, '1'))
            user_id = cursor.lastrowid
            
            query = "INSERT INTO login (id, username, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (user_id, username, password))
            
            connection.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
