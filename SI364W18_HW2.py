## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError, validators
from wtforms.validators import Required
import requests
import json
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################
class albumform(Form):
	album = TextField("Name Of album:",validators=[Required() ])
	albumrating= RadioField('Please rate this album from 1 star to 3 stars:',validators=[Required() ], choices = [('1','1'),('2','2'),('3','3')])
	submit = SubmitField("Submit")

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def artistform():
	return render_template("artistform.html")

@app.route('/artistinfo', methods=['GET', 'POST'])
def artistinfo():
	if request.method== 'POST':
		search= "term=" +request.form['artist']
		r=requests.get('https://itunes.apple.com/search?' +search)
		dicto=json.loads(r.text)
	return render_template('artist_info.html', objects=dicto['results'])
	

@app.route('/specific/song/<artist_name>')
def specificartist(artist_name):
	search= "term=" +artist_name
	request=requests.get('https://itunes.apple.com/search?' +search)
	dictionary=json.loads(request.text)
	return render_template('specific_artist.html', results = dictionary['results'])

@app.route('/artistlinks')
def artistlinks():
	return render_template('artist_links.html')

@app.route('/album_entry',methods = ['GET', 'POST'])
def albumentry():
	form=albumform()
	#if request.method == 'GET':
	return render_template('album_entry.html', form = form)
@app.route('/album_result', methods = ['GET', 'POST'])
def albumresult():
	form=albumform(request.form)
	if request.method=='POST' and form.validate_on_submit():
		album=form.album.data
		albumrating=form.albumrating.data
		return render_template('album_data.html', name=album, albumrating=albumrating)
	flash('All fields are required!')
	return redirect(url_for('albumentry'))
if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
