
from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User

from forms import SignUpForm,LoginForm

app=Flask(__name__)
app.config ["SQLALCHEMY_DATABASE_URI"] = "sqlite:////home/hedley/Documents/learning-flask/learning-flask.db"

db.init_app(app)
app.secret_key = "super-Secret"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup", methods=['GET',"POST"])
def signup():
    form=SignUpForm()
    if request.method == "POST":
        if not form.validate():
            
            return render_template("signup.html", form=form)
        else:
            newuser=User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
            db.session.add(newuser)
            db.session.commit()
            session["email"]=newuser.email
            return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("signup.html", form=form)

@app.route("/login", methods=['GET',"POST"])
def login():
    form=LoginForm()
    if request.method == "POST":
        if not form.validate():
            return render_template("login.html", form=form)
        else:
            email = form.email.data
            passw = form.password.data
            user = User.query.filter_by(email=email).first()
            print passw
            print email
            if user is not None and user.check_password(passw):
                return redirect(url_for("home"))
            else:
                return redirect(url_for("login"))
               
    elif request.method == "GET":
        return render_template("login.html", form=form)
@app.route("/logout")
def logout():
    session.pop("email",None)
    return redirect(url_for("index"))

@app.route("/home")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
