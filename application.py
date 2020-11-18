from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# initialize the application
app = Flask(__name__)

# showing debug messages
app.config["DEBUG"] = True

# initialize the SQL DATABASE connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# User Model
class User( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    bio = db.Column(db.Text())
    username = db.Column(db.String(10))
    password = db.Column(db.String(20))
    # relationships
    cars = db.relationship( "Car", backref="user" )
    bids = db.relationship( "Bid", backref="user" )
    auctions = db.relationship( "Auction", backref="user" )

    def __init__(self, fname, lname, bio, username, password):
        self.fname = fname
        self.lname = lname
        self.bio = bio
        self.username = username
        self.password = password

# Car Model
class Car( db.Model ):
    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String(100))
    make = db.Column(db.String(100))
    model = db.Column(db.String(100))
    color = db.Column(db.String(10))
    year = db.Column(db.Integer)
    mileage = db.Column(db.Integer)
    doors = db.Column(db.Integer)
    engine = db.Column(db.String(100))
    # relationships
    parts = db.relationship( "Part", backref="car" )
    auction = db.relationship( "Auction", backref="car" )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, picture, make, model, color, year, mileage, doors, engine, user):
        self.picture = picture
        self.make = make
        self.model = model
        self.color = color
        self.year = year
        self.mileage = mileage
        self.doors = doors
        self.engine = engine
        self.user = user


@app.route("/")
def home():
    return render_template("index.html")


# CRUDI - Users Controller

@app.route("/users")
def all_users():
    allUsers = User.query.all()
    return render_template("users.html", users = allUsers)

@app.route("/users/create", methods=["POST"])
def create_user():
    fname = request.form.get('fname', "")
    lname = request.form.get('lname', "")
    bio = request.form.get('bio', "")
    username = request.form.get('username', "")
    password = request.form.get('password', "")

    newUser = User(fname, lname, bio, username, password)
    db.session.add(newUser)
    db.session.commit()

    return redirect("/users/")

@app.route("/users/<id>")
def get_user(id):
    user = User.query.get( int(id) )
    return render_template("user.html", user = user)

@app.route("/users/<id>/edit", methods=["GET", "POST"])
def edit_user(id):
    user = User.query.get( int(id) )

    if request == "Post":
        user.fname = request.form.get('fname', "")
        user.lname = request.form.get('lname', "")
        user.bio = request.form.get('bio', "")
        user.password = request.form.get('password', "")
        db.session.commit()
        return render_template("user.html", user = user)
    else:
        return render_template("edit_user.html", user = user)

@app.route("/users/<id>/delete", methods=["POST"])
def delete_user(id):
    user = User.query.get( int(id) )
    db.session.delete(user)
    db.session.commit()
    return redirect("users")


if __name__ == "__main__":
    app.run()
