'''
Created on Apr 29, 2013

@author: Suvodeep Pyne
'''
from recommender import Recommender

class GitBook():	
	recommender = Recommender()
	
	def __init__(self):
		self.recommender.build_project_features()
		print 'Launched GitBook instance'
		
	def get_languages(self):
		return self.recommender.get_languages()
		
	def get_areas_of_interest(self):
		return self.recommender.get_aoi()
		
	def recommend_projects(self, languages, area_interest, difficulty):
		return self.recommender.recommend_projects(self, languages, area_interest, difficulty) 
	
if __name__ == '__main__':
    obj = GitBook()
    print 'Languages:', obj.get_languages()
    print 'Areas of Interest:', obj.get_areas_of_interest()
    print 'Done.'    