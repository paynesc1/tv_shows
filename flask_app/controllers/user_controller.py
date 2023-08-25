from flask_app import app
from flask import render_template, request, redirect, session, flash
import pprint
from flask_app.models.user_model import User
from flask_app.models.show_model import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#render page
@app.route("/")
def index():
    return render_template("user.html")

@app.route("/welcome")
def welcome():
    if 'user_id' not in session:
        return redirect("/")
    user = User.get_user_by_id(session['user_id'])
    shows = Show.get_all_shows()
    return render_template("welcome.html", user=user, shows=shows)


#SAVE ROUTE
@app.route("/user/save", methods=['POST'])
def user_save():
    if not User.validation(request.form):
        return redirect("/")
    #create hash
    if len(request.form['password']) < 8:
        flash("Password must be at least 8 characters.", "registration_error")
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name" : request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password" : pw_hash
    }
    #classmethod to save user to database
    new_user = User.user_save(data)
    session['user_id'] = new_user
    return redirect("/welcome")

#LOGIN ROUTE
@app.route("/user/login", methods=['POST'])
def user_login():
    #see if username/email exists in db
    data = { "email" : request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid email address", "login_error")
        return redirect("/")
    if len(request.form['password']) < 8:
        flash("Invalid password.", "login_error")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password", "login_error")
        return redirect("/")
    session['user_id'] = user_in_db.id
    return redirect("/welcome")
    
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
