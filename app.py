from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    if username == 'admin' and password == 'p':
        return render_template('welcome.html')
    else:
        return render_template('login.html', message="Invalid username or password")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        
        print(f"New user signed up with name: {name}, phone: {phone}, email: {email}, username: {username}, password: {password}")
        return redirect(url_for('login'))
    
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
