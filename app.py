import os
import sqlite3 # WIP: check other options

# WIP: we need to resolve the cs50 SQL problem
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session # WIP: tried getting rid of the flash import
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tickets.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    if request.method == "POST":
        return redirect("/sell")
    else:
        # Performing queries that show all the tickets, textbooks, and dorm items for sale (posted by you) on the index page
        tickets_f_s = db.execute("SELECT * FROM textbook_info WHERE type=? AND user_id=?", "ticket", session["user_id"])
        textbooks_f_s = db.execute("SELECT * FROM textbook_info WHERE type=? AND user_id=?", "textbook", session["user_id"])
        dorm_items_f_s = db.execute("SELECT * FROM textbook_info WHERE type=? AND user_id=?", "dorm item", session["user_id"])
        return render_template("index.html", tickets_f_s=tickets_f_s, textbooks_f_s=textbooks_f_s, dorm_items_f_s=dorm_items_f_s)

@app.route("/tickets", methods=["GET", "POST"])
@login_required
def tickets():
    # Getting summary ticket info for buy tickete page and all tickets for the pop up
    distinct_tickets = db.execute("SELECT opponent, date, MIN(asking_price) AS asking_price FROM textbook_info WHERE type = ? GROUP BY opponent", "ticket")
    ticket_details = db.execute("SELECT opponent, asking_price, name, phone_number FROM textbook_info WHERE type = ?", "ticket")

    return render_template("buy_tickets.html", distinct_tickets=distinct_tickets, ticket_details=ticket_details)

@app.route("/buy_textbooks", methods=["GET", "POST"])
@login_required
def buy_textbooks():
        # Getting all the information relevant to textbooks
        textbooks = db.execute("SELECT * FROM textbook_info WHERE type=?", "textbook")
        return render_template("buy_textbooks.html", textbooks=textbooks)

@app.route("/sell_textbooks", methods=["GET", "POST"])
@login_required
def sell_textbooks():
    if request.method == "POST":
        # Allowing for submission of new textbook for sale
        db.execute("INSERT INTO textbook_info (title, image_link, asking_price, name, netid, phone_number, user_id, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            request.form.get("title"), request.form.get("image link"), request.form.get("asking price"), request.form.get("name"), request.form.get("netID"), request.form.get("phone number"), session["user_id"], "textbook")
        return redirect("/")
    else:
        return render_template("sell_textbooks.html")

@app.route("/sell_dorm_items", methods=["GET", "POST"])
@login_required
def sell_dorm_items():
    if request.method == "POST":
        # Allowing for submission of new dorm item for sale
        db.execute("INSERT INTO textbook_info (item, image_link, asking_price, name, netid, phone_number, user_id, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            request.form.get("item"), request.form.get("image link"), request.form.get("asking price"), request.form.get("name"), request.form.get("netID"), request.form.get("phone number"), session["user_id"], "dorm item")
        return redirect("/")
    else:
        return render_template("sell_dorm_items.html")

@app.route("/buy_dorm_items", methods=["GET", "POST"])
@login_required
def buy_dorm_items():
        # Getting all relevant information relevant to dorm items
        dorm_items = db.execute("SELECT * FROM textbook_info WHERE type=?", "dorm item")
        return render_template("buy_dorm_items.html", dorm_items=dorm_items)

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

# Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        usernames = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # if the length returned is 0, no one has that username
        if len(usernames) != 0:
            return apology("username is taken", 400)

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure user provides password confirmation
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        # Password and confirmation must match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and password confirmation do not match", 400)

        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get("username"), generate_password_hash(request.form.get("password")))

        session["user_id"] = id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/delist", methods=["GET", "POST"])
@login_required
def delist():
    if request.method == "POST":
        # Updating the value of the good type to delisted so that it doesn't get posted onto any of the three pages that show listed goods
        db.execute("UPDATE textbook_info SET type=? WHERE good_id=? AND user_id=?", "delisted", request.form.get("good id"), session["user_id"])
        return redirect("/")
    else:
        return render_template("delist.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Allows redirection to sell page of relevant item
    if request.method == "post1":
        return redirect("/sell_tickets")
    elif request.method == "post2":
        return redirect("/sell_textbooks")
    elif request.method == "post3":
        return redirect("/sell_dorm_items")
    else:
        return render_template("sell.html")

@app.route("/sell_tickets", methods=["GET", "POST"])
@login_required
def sell_tickets():
    if request.method == "POST":
        # Allowing for submission of new ticket for sale
        db.execute("INSERT INTO textbook_info (user_id, asking_price, name, netid, phone_number, opponent, date, type) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
           session["user_id"] , request.form.get("asking price"), request.form.get("name"), request.form.get("netid"), request.form.get("phone number"), request.form.get("opponent"), request.form.get("date"), "ticket")
        return redirect("/")
    else:
        return render_template("sell_tickets.html")