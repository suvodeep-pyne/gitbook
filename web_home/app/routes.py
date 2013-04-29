from flask import Flask, render_template
 
app = Flask(__name__)      
 
@app.route('/')
@app.route('/index')
def home():
	languages = ['C++', 'Ruby']
	aoi = ['machine-learning', 'artificial-intelligence']
	return render_template('index.html', languages = languages, areas_of_interest = aoi)

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/results')
def results():
  results = { 'project1' : {'projectName': 'login' , 'owner':'ownername'} , 'project2' : {'projectName': 'login' , 'owner':'ownername'}}
  results1 = { 'project1': { u'html_url': u'https://github.com/ezmobius',u'login': u'ezmobius',u'organizations_url': u'https://api.github.com/users/ezmobius/orgs', u'repos_url': u'https://api.github.com/users/ezmobius/repos',u'url': u'https://api.github.com/repos/ezmobius/nanite', u'watchers_count': 770}}
  aoi = ['machine-learning', 'artificial-intelligence']
  return render_template('results.html' , areas_of_interest=aoi, results=results1)

@app.route('/layout')
def layout():
  return render_template('layout.html')

if __name__ == '__main__':
  app.run(debug=True)
