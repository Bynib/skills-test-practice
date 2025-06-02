from flask import Flask, render_template,redirect, url_for, request, session, flash
import db

app = Flask(__name__)
app.secret_key = "asdfghjkl"

db.create_table_user()
db.create_table_event()
db.create_table_user_event()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == "POST":

        users = db.get_all_users()
        user_emails = [user['email'] for user in users]
        user_usernames = [user['username'] for user in users]

        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        if not firstname or not lastname or not email or not username or not password:
            flash("All fields are required!")
            return render_template('register.html', firstname=firstname, lastname=lastname, email=email, username=username, password=password)

        if email in user_emails:
            flash("Email already exists!")
            return render_template('register.html', firstname=firstname, lastname=lastname, email=email, username=username, password=password)
        
        if username in user_usernames:
            flash("Username already taken!")
            return render_template('register.html', firstname=firstname, lastname=lastname, email=email, username=username, password=password)


        db.add_user(firstname, lastname, email, username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash("All fields are required!")
            return render_template("login.html", username=username, password=password)
        user = db.login(username, password)
        if user:
            user = dict(user)
            session['user'] = user
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    if user:
        return render_template('dashboard.html', user=user)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)