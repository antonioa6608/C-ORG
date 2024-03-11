from flask import Flask, render_template, request, redirect, url_for, session
import hashlib

app = Flask(__name__)
app.secret_key = 'thisasecretkey'

users = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest()
    },
    "user": {
        "password": hashlib.sha256("user123".encode()).hexdigest()
    }
}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password.')
    
    return render_template('login.html', error=None)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/process_zip', methods=['POST'])
def process_zip():
    if 'username' in session:
        zip_code = request.form['zip_code']
        return f"Zip code {zip_code} submitted successfully!"
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
