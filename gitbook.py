'''
Created on Apr 29, 2013

@author: Suvodeep Pyne
'''
from recommender import Recommender
from resource_manager import ResourceManager

class GitBook():    
    
    def init(self):
        self.recommender = Recommender()
        self.rm = ResourceManager()
        self.recommender.build_project_features()
        print 'Launched GitBook instance'
        
    def get_languages(self):
        return self.recommender.get_languages()
        
    def get_areas_of_interest(self):
        return self.recommender.get_aoi()
        
    def recommend_projects(self, languages, area_interest, difficulty):
        return self.recommender.recommend_projects(languages, area_interest, difficulty) 
    
if __name__ == '__main__':
    print "GitBook class Test Module"
    gitbook = GitBook()

    print "calling gitbook.init()"
    gitbook.init()
    print 'Languages:', gitbook.get_languages()
    print 'Areas of Interest:', gitbook.get_areas_of_interest()

    print
    print '#Languages', len(gitbook.get_languages()), 'Expected: 53'
    print '#Areas of Interest:', len(gitbook.get_areas_of_interest()), 'Expected 7'

    print
    print 'Test #1'
    languages = [ u'Python' ]
    aoi = ['Information Retrieval', 'Machine Learning']
    print '#Results:', len(gitbook.recommend_projects(languages, aoi, 'any')), 'Expected: 7'

    print 'Done.'    
