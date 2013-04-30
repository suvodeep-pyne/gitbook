'''
Created on Apr 29, 2013

@author: Suvodeep Pyne
'''

from flask import Flask, render_template, request, Response, redirect
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

@application.route('/results', methods = ['GET', 'POST'])
def results():
  try:
    request_data = request.args
    data = {}
    for key in request_data:
      data[key] = request_data.getlist(key)

    with open("app/project_contributors.p","rb") as fr: companies = pickle.load(fr)
    projects = gitbook.recommend_projects(data['languages'], data['area_of_interest'], data['difficulty'])
  except:
    return redirect('/index')
  
  output_companies = []
  for project in projects:
    if project['full_name'] in companies:
    	output_companies.append(companies[project['full_name']])
  
  output_companies = output_companies[:10]

  """
  		Project data keys : ['category', 'description', 'html_url', 'class_prob', 'full_name', 'prob']

  """
  return render_template('results.html', data=data, results=projects , results_size=len(projects), companies = output_companies)

@application.route('/layout')
def layout():
  return render_template('layout.html')


