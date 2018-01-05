from flask import Flask, redirect, render_template, request, session, flash
import re
app = Flask(__name__)
app.secret_key = "inner ear hallows"

emailRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-z]+$')

@app.route('/')
def index():
    if not session.has_key('errors'):
        session['errors'] =[]
    elif session.has_key('errors'):
        session['errors'] = []
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    #check each field for some value, adds error if any return empty
    error = False
    for key in request.form:
        if len(request.form[key]) < 1:
            error = True

    if error:
        session['errors'].append('Please Complete All Fields!')

    #check that password is appropriate length(8)
    if len(request.form['password']) < 8:
        session['errors'].append('Password Must Be At Least 8 Characters!')

    #check that password lengths match
    if len(request.form['password']) !=len(request.form['confirm_password']):
        session['errors'].append("Password and Confirmation Must Be The Same Length!")
    
    #check that the pasword values match
    if request.form['password'] != request.form['confirm_password']:
        session['errors'].append('Passwords Do Not Match!')

    #check for invalid characters in email
    if not emailRegex.match(request.form['email']):
        session['errors'].append('Invalid Email!')

    #check that first name and last name do not include numbers
    if not request.form['first_name'].isalpha() or not request.form['last_name'].isalpha():
        session['errors'].append('Your Name(s) May Only Include Letters!')

    print session['errors']
    if len(session['errors'])>0 :
        for string in session['errors']:
            flash(string)
    else:
        flash('Thank You For Registering!')
    return redirect('/')

app.run(debug=True)