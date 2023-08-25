from flask_app import app
from flask import render_template, request, redirect, session, flash
import pprint
from flask_app.models.user_model import User
from flask_app.models.show_model import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#RENDER ADD SHOW PAGE
@app.route("/new")
def index_view():
    data = {"user_id":session['user_id']}
    user = User.get_user_by_id(data)
    return render_template("new.html",user=user)

#RENDER EDIT SHOW PAGE
@app.route("/edit/<int:id>")
def index_edit(id):
    show = Show.get_show_by_id(id)
    return render_template("edit.html", show=show)

#RENDER VIEW SHOWS PAGE
@app.route("/show/<int:id>")
def index_show(id):
    show=Show.get_show_by_id(id)
    return render_template("show.html", show=show)



#SAVE SHOW ROUTE
@app.route("/save/new", methods=['POST'])
def show_save():
    if not Show.validation(request.form):
        return redirect("/new")
    data = {
        "title":request.form['title'],
        "network":request.form['network'],
        "release_date":request.form['release_date'],
        "description":request.form['description'],
        "user_id": session['user_id']
    }
    Show.show_save(data)
    return redirect("/welcome")


#EDIT SHOW ROUTE
@app.route("/edit", methods=['POST'])
def edit():
    if not Show.validation(request.form):
        return redirect(f"/edit/{request.form['id']}")

    data = {
        "title":request.form['title'],
        "network":request.form['network'],
        "release_date":request.form['release_date'],
        "description":request.form['description'],
        "id": request.form['id']
    }
    Show.update_car(data)
    return redirect("/welcome")

#DELETE SHOW ROUTE
@app.route("/delete/<int:id>")
def delete(id):
    data={"id":id}
    Show.delete(data)
    return redirect("/welcome")