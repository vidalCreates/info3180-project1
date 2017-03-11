'''
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
'''

import time
import uuid
import os

from app import app
from app import db
from app.models import UserProfile
from flask import render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename



###
# Routing for your application.
###


@app.route('/')
def home():
    '''Render website's home page.'''
    return render_template('home.html')


@app.route('/about/')
def about():
    '''Render the website's about page.'''
    return render_template('about.html', name='Project 1')


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/profile', methods=['POST', 'GET'])
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
        if profile_image:
            file_folder = app.config['UPLOAD_FOLDER']
            filename = secure_filename(profile_image.filename)
            profile_image.save(os.path.join(file_folder, filename))

        #handling the time created
        created_on = time.strftime('%Y/%b/%d')

        #creating user object and inserting into database
        user = UserProfile(userid=userid,
                           first_name=f_name,
                           last_name=l_name,
                           username=user_name,
                           biography=biography,
                           age=age,
                           gender=gender,
                           created_on=created_on,
                           profile_image=profile_image.filename)
        db.session.add(user)
        db.session.commit()
        #quit()
        return redirect(url_for('home'))
    return render_template('profile.html')


@app.route('/profiles', methods=['GET', 'POST'])
def profiles():
    userlist=[]

    #get all profiles from database
    users = UserProfile.query.filter_by().all()

    if request.method == 'POST':
        #create list of profiles in json format
        for user in users:
            userlist += [{'username':user.username, 'userid':user.userid}]

        return jsonify(users=userlist)
    elif request.method == 'GET':
        return render_template('profiles.html', profiles=users)

    return redirect(url_for('home'))


@app.route('/profile/<userid>', methods=['GET', 'POST'])
def userprofile(userid):
    userjson={}
    #get specific profile from database
    user = UserProfile.query.filter_by(userid=userid).first()
    if request.method == 'POST':
        #create json formatted data
        userjson={'userid':user.userid, 'username':user.username, 'profile_image':user.profile_image, 'gender':user.gender, 'age':user.age, 'created_on':user.created_on}
        return jsonify(userjson)

    elif request.method == 'GET' and user:
        return render_template('profile-individual.html', profile=user)

    return render_template('profile.html')


@app.after_request
def add_header(response):
    '''
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    '''
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    '''Custom 404 page.'''
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='8080')