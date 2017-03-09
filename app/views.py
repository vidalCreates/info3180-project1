"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from app import db
from app.models import UserProfile
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

import time
import uuid
import os

###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Project 1")


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/profile', methods=['POST','GET'])
def profile():
    if request.method == 'POST':
        #handling the random unique id
        userid = str(uuid.uuid4().fields[-1])[:8]

        #handling general form data
        f_name = request.form['fname']
        l_name = request.form['lname']
        user_name = request.form['username']
        biography = request.form['bio']
        age = request.form['age']
        gender = request.form['gender']

        #handleing the file upload
        profile_image = request.files['file']
        file_folder = app.config['UPLOAD_FOLDER']
        filename = secure_filename(profile_image.filename)
        profile_image.save(os.path.join(file_folder, filename))

        #handling the time created
        created_on = time.strftime("%Y/%b/%d")

        #creating user object and inserting into database
        user = UserProfile(userid=userid,first_name=f_name,last_name=l_name,username=user_name,biography=biography,age=age,gender=gender,created_on=created_on,profile_image=profile_image.filename)
        db.session.add(user)
        db.session.commit()
        #quit()
        flash("Profile added")
        return redirect(url_for('home'))
    return render_template('profile.html')

@app.route('/profiles', methods=['GET'])
def profiles():
    return render_template('profiles.html')

@app.route('/profile/<userid>', methods=['GET'])
def userprofile():
    return

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")