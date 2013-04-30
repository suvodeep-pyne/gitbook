from flask import Flask, render_template
import pickle
 
from app import application

# folder/gitbook folder/ gitbook module/ --. get the damn class !
from app.gitbook.gitbook import GitBook

gitbook = GitBook()

@application.route('/')
@application.route('/index')
def home():
	languages = gitbook.get_languages()
	aoi = gitbook.get_areas_of_interest()
	return render_template('index.html', languages = languages, areas_of_interest = aoi)

@application.route('/about')
def about():
  print "this is printed whenever the about page is called!!!!!!!!!!!!!!!!!!!!!!!"
  return render_template('about.html')

@application.route('/results')
def results():
  """
  Compute the reccomendation for the user using his preferences and assign it to the variable results.
  Call the Reccomender class here... integrate it with all!!
  
  This is where you will have to dump the Reccomender's code
  """
  
  
  #results = [{'projectName': 'login' , 'owner':'ownername'} , {'projectName': 'login' , 'owner':'ownername'}]
  with open("app/tmpProjs.p","rb") as fr: results = pickle.load(fr)
  with open("app/project_contributors.p","rb") as fr: companies = pickle.load(fr)
  
  aoi = ['machine-learning', 'artificial-intelligence']
  
  return render_template('results.html' , areas_of_interest=aoi, results=results , companies = companies)

@application.route('/layout')
def layout():
  return render_template('layout.html')


