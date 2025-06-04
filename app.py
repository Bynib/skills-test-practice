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
        flash("Successfully registered!")
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route('/dashboard')
def dashboard():
    user = session.get('user')
    registered_users = db.get_all_users()
    if user:
        return render_template('dashboard.html', user=user, registered_users=registered_users)
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method=="POST":
        user = session.get('user')
        search_query = request.form['search_query']
        users = db.search(search_query)
        return render_template('dashboard.html', registered_users=users, user=user, search_query=search_query)

# @app.route('/update-user', methods=["GET", "POST"])
# def update_user():
#     if request.method=="POST":
#         user_id = request.form['user_id']
#         user = db.get_one_user(user_id)
#         return render_template("update.html", user=user)

@app.route('/update',methods=["GET","POST"])
def update():
    if request.method =="POST":
        user_id = request.form['user_id']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user_to_update = db.get_one_user(user_id)
        original_email = user_to_update['email']
        original_username = user_to_update['username']

        users = db.get_all_users()

        user_emails = [user['email'] for user in users if user['email']!=original_email]
        user_usernames = [user['username'] for user in users if user['username']!=original_username]

        if not firstname or not lastname or not email or not username or not password:
            flash("All fields are required!")
            return render_template("update.html", user_id=user_id, firstname=firstname, lastname=lastname, email=email, username=username, password=password)
        
        if email in user_emails:
            flash("Email already exists!")
            return render_template("update.html", user_id=user_id, firstname=firstname, lastname=lastname, email=email, username=username, password=password)
        
        if username in user_usernames:
            flash("Username already taken!")
            return render_template("update.html", user_id=user_id, firstname=firstname, lastname=lastname, email=email, username=username, password=password)

        
        db.update_user(user_id, firstname, lastname, email, username, password)
        flash("User update successful!")
        return redirect(url_for('dashboard'))
    
    user_id = request.args.get('user_id')
    user = db.get_one_user(user_id)
    return render_template("update.html", user_id=user['user_id'], firstname=user['firstname'], lastname=user['lastname'], email=user['email'], username=user['username'], password=user['password'])

@app.route('/delete-user', methods=["GET","POST"])
def delete_user():
    if request.method == "POST":
        user_id =request.form['user_id']
        db.delete_user(user_id)
        return redirect(url_for('dashboard'))

    

if __name__ == "__main__":
    app.run(debug=True)