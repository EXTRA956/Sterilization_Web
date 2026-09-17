import os
import re

from dotenv import load_dotenv, dotenv_values
from flask import Flask, session, redirect, render_template, request
from functools import wraps

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

def login_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/")
        return view_function(*args, **kwargs)
    return wrapper

@app.route("/", methods=["GET", "POST"]) # Only redirect here if not logged in / on logout
def login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("password")

        if (re.match(r"^ID_\d{3}$", user_id)) or (password != os.getenv("ADMIN_PASSWORD")): # Temporary to get the page working, (Profiles with hash passwords will be added later)
            return render_template("login.html", error="Invalid ID format or incorrect password")

        session["user_id"] = user_id
        
        return redirect("/home")

    session.clear()
    return render_template("login.html")

@app.route("/home")
@login_required
def home():
    return f"Logged in as {session["user_id"]}"

@app.route("/logout")
def logout():
    session.clear()
    return "Logged out"

if __name__ == "__main__":
    app.run(debug=True)