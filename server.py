from flask import Flask, request, redirect, render_template, session, flash
import datetime
import re
from mysqlconnection import MySQLConnector
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'freelunch'
mysql = MySQLConnector(app,'email_val')

@app.route('/')
def index():
    query = "SELECT * FROM users"                           # define your query
    users = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_users=users) # pass data to our template

@app.route('/success')
def success():
    flash(str("The email address you entered " + session['new_email'] + " is a valid address! Thank You!"))
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM users;"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': id}
    # Run query with inserted data.
    users = mysql.query_db(query)
    return render_template('success.html', all_users=users)

@app.route('/delete/<id>')
def delete(id):
    query = "DELETE FROM users WHERE id = :id"
    data = {'id': int(id)}
    # Run query with inserted data.
    mysql.query_db(query,data)
    return redirect('/success')

@app.route('/users', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO users (email, created_at, updated_at) VALUES (:email, NOW(), NOW());"
    query_val = "SELECT email FROM users WHERE email = :email;"
    session['new_email'] = request.form['email']
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'email': request.form['email'],
           }
    check = mysql.query_db(query_val, data)

    # Validates email address for proper format.
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        return redirect('/')
    elif len(check) != 0:
        flash("Duplicate address, enter another one!")
        return redirect('/')
    
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/success')


app.run(debug=True)