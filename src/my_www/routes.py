from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user

from . import db

routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route("/login")
def login():
    return render_template("login.html")


@routes_blueprint.route("/login", methods=["POST"])
def login_form_submit():
    # login code goes here
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = db.User.query.filter_by(name=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(
            url_for("routes.login")
        )  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for("routes.index"))


@routes_blueprint.route("/signup")
def signup():
    return render_template("signup.html")


@routes_blueprint.route("/signup", methods=["POST"])
def signup_form_submit():
    # code to validate and add user to database goes here
    username = request.form.get("username")
    password = request.form.get("password")

    user = db.User.query.filter_by(
        name=username
    ).first()  # if this returns a user, then the email already exists in database

    if (
        user
    ):  # if a user is found, we want to redirect back to signup page so user can try again
        flash("Username address already exists")
        return redirect(url_for("routes.signup"))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = db.User(
        name=username,
        password=generate_password_hash(password, method="sha256"),
    )

    # add the new user to the database
    db.db.session.add(new_user)
    db.db.session.commit()
    flash("New user created, please login.")

    return redirect(url_for("routes.login"))


@routes_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.index"))


@routes_blueprint.route("/")
def index():
    if current_user and current_user.is_authenticated:
        out = render_template("profile.html", user=current_user)
    else:
        # no user logged in
        out = render_template("index.html")
    return out


## Item management
@routes_blueprint.route("/items/add", methods=["POST"])
@login_required
def add_item():
    item_name = request.form.get("item_name")
    item_price = request.form.get("item_price")
    current_user.items.append(
        db.Item(name=item_name, price=int(float(item_price) * 100))
    )
    db.db.session.commit()

    return redirect(url_for("routes.index"))


@routes_blueprint.route("/items/delete/<int:id>")
@login_required
def delete_item(id):
    item = db.Item.query.filter_by(id=id).first()

    if item:
        db.db.session.delete(item)
    db.db.session.commit()
    return redirect(url_for("routes.index"))


@routes_blueprint.route("/items/summary")
@login_required
def item_summary():
    return render_template(
        "items_summary.html",
        user=current_user,
        items_total=sum(item.price for item in current_user.items),
    )
