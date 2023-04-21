from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from openpyxl import load_workbook
import os

app = Flask(__name__)
app.secret_key = "mysecretkey"


def get_users_by_email(email):
    # Check if the users file exists
    if not os.path.exists('users.xlsx'):
        return []

    # Load user data from file into a pandas DataFrame
    user_data = pd.read_excel('users.xlsx', header=None, names=[
                              'username', 'email', 'password', 'contact'])

    # Check if the email exists in the DataFrame
    matches = user_data[user_data['email'] == email]
    if not matches.empty:
        # If there is a match, return the rows as a list of dictionaries
        return matches.to_dict('records')
    else:
        # If there is no match, return an empty list
        return []


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        # Check if email and password are correct
        email = request.form["email"]
        password = request.form["password"]
        users = get_users_by_email(email)
        if not users:
            # Display error message
            error = "Invalid email or password"
            return render_template("signin.html", error=error)
        elif len(users) == 1:
            # If there is only one user with the given email, check the password
            user = users[0]
            if user["password"] == password:
                # Set session variables
                session["username"] = user["username"]
                # Redirect to dashboard
                return render_template("dashboard.html")
            else:
                # Display error message
                error = "Invalid email or password"
                return render_template("signin.html", error=error)
        else:
            # If there are multiple users with the given email, prompt for username
            return render_template("signin.html", users=users)
    else:
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get user details from form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact = request.form['contact']

        # Load existing user data from file into a pandas DataFrame
        if os.path.exists('users.xlsx'):
            user_data = pd.read_excel('users.xlsx', header=None, names=[
                'username', 'email', 'password', 'contact'])
        else:
            user_data = pd.DataFrame(
                columns=['username', 'email', 'password', 'contact'])

        # Check if email is already registered
        if email in user_data['email'].values:
            error = 'Email is already registered. Please sign in or use a different email.'
            return render_template('signup.html', error=error)

        # Add new user data to the existing DataFrame
        new_user = pd.DataFrame({
            'username': [username],
            'email': [email],
            'password': [password],
            'contact': [contact]
        })
        user_data = pd.concat([user_data, new_user], ignore_index=True)

        # Save user data to file
        user_data.to_excel('users.xlsx', index=False, header=False)

        # Redirect to sign in page
        return render_template('signin.html')
    else:
        return render_template('signup.html')


@app.route("/dashboard")
def dashboard():
    # Check if user is logged in
    if "username" in session:
        # Get username from session
        username = session["username"]
        # Render dashboard template with username
        return render_template("dashboard.html", username=username)
    else:
        # Redirect to sign in page
        return render_template("signin.html")


@app.route("/logout")
def logout():
    # Clear session variables
    session.pop("username", None)
    # Redirect to sign in page
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
