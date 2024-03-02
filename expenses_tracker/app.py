import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
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
db = SQL("sqlite:///expenses.db")

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
    """Show summary of expenses"""
    user_id = session["user_id"]

    try:
        # Get total expenses for each category
        expenses = db.execute("SELECT category, SUM(amount) AS total_amount FROM expenses WHERE user_id = ? GROUP BY category", user_id)

        # Get the category with the highest total amount
        most_expensive_category = db.execute(
            "SELECT category FROM expenses WHERE user_id = ? GROUP BY category ORDER BY SUM(amount) DESC LIMIT 1",
            user_id
        )[0]["category"]

        total_expenses = sum(expense["total_amount"] for expense in expenses)
        cash_balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]["cash"]

        return render_template(
            "index.html",
            expenses=expenses,
            total_expenses=total_expenses,
            cash_balance=cash_balance,
            most_expensive_category=most_expensive_category,
            usd=usd
        )

    except Exception as e:
        return apology(f"An error occurred: {str(e)}")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("Username and password are required!")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("Invalid username and/or password")

        session["user_id"] = rows[0]["id"]

        flash("Login successful!")
        return redirect("/")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    session.clear()

    flash("Logout successful!")
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not confirmation:
            return apology("All fields are required!")

        if password != confirmation:
            return apology("Passwords do not match!")

        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            flash("Registration successful!")
            return redirect("/login")
        except Exception as e:
            return apology(f"Registration failed: {str(e)}")

    return render_template("register.html")

@app.route("/add_expense", methods=["GET", "POST"])
@login_required
def add_expense():
    """Add expense"""

    if request.method == "POST":

        category = request.form.get("category")  # Change from "name" to "category"
        amount = float(request.form.get("amount"))

        if not category or not amount or amount <= 0:
            return apology("Invalid category or amount")

        user_id = session["user_id"]

        try:
            db.execute("INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?)", user_id, category, amount)
            flash("Expense added successfully!")
            return redirect("/")
        except Exception as e:
            return apology(f"Failed to add expense: {str(e)}")

    # Fetch categories for the form
    try:
        categories = db.execute("SELECT DISTINCT name FROM categories")
    except Exception as e:
        return apology(f"An error occurred: {str(e)}")

    return render_template("add_expense.html", categories=categories)


@app.route("/expense_history")
@login_required
def expenses_history():
    """Show expenses history"""

    user_id = session["user_id"]

    try:
        expenses = db.execute("SELECT * FROM expenses WHERE user_id = ?", user_id)
        total_amount = db.execute("SELECT SUM(amount) AS total FROM expenses WHERE user_id = ?", user_id)[0]["total"]

        return render_template("expense_history.html", expenses=expenses, total_amount=total_amount, usd=usd)

    except Exception as e:
        return apology(f"An error occurred: {str(e)}")

@app.route("/expense_categories")
@login_required
def categories():
    """Show expense categories"""

    try:
        categories = db.execute("SELECT name FROM categories")
        return render_template("expense_categories.html", categories=categories)
    except Exception as e:
        return apology("sorry")

if __name__ == "__main__":
    app.run(debug=True)

