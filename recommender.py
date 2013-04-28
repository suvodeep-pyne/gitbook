'''
Created on Apr 26, 2013

@author: Suvodeep Pyne
Edited by Garima Agarwal
'''

import operator
import pprint as pp

from read_data import DataRetriever
from nb_classifier import NaiveBayesClassifier
from page_rank import pagerank

GITHUB_DATA = 'github_data'
TRAIN_DATA = 'train_data'

class ProjectVectorBuilder():
    
    projects = {}
    
    def __init__(self, project_data):
        self.project_data = project_data
        
        self.nb = NaiveBayesClassifier('train_data/vocabulary', 'train_data/dataset')
        self.nb.train()
    
    
    def build_projects_vector(self):
        print "In build projects"
        for name, project in self.project_data.iteritems():
            self.projects[name] = {}
            #readme = project['readme']
            
            # Bad case: When readme is not found. It returns empty lists.
            #if isinstance(readme, list): continue
            #readme = unicode(readme, 'utf-8', errors = 'ignore')
            if project["description"] != None:
                readme = project["description"]
            else:
                continue

            prob_data = self.nb.classify(readme)[0]
            self.projects[name]['class_prob'] = prob_data
            self.projects[name]['description'] = readme
            if len(prob_data) > 0:
                self.projects[name]['category'] = max(prob_data.iteritems(), key=operator.itemgetter(1))[0]
        print "Printing maps"
        pp.pprint(self.projects)
        return self.projects
    
            
class Recommender():
    """Initialize the recommender"""
    def __init__(self):
        directory_name = GITHUB_DATA
        self.data_retriever = DataRetriever(directory_name)
        self.project_data = self.data_retriever.parseProjectData()
        self.user_data, self.user_follower_map = self.data_retriever.parseUserFollowers()
        self.project_vector_builder = ProjectVectorBuilder(self.project_data)
   
    """Get different scores for each project"""
    def build_project_features(self):
        self.project_vector = self.project_vector_builder.build_projects_vector()
        self.user_ranking = pagerank(self.user_data, self.user_follower_map) 
                 

if __name__ == '__main__':
    obj = Recommender()
    obj.build_project_features()
    
    print 'Printing projects Data Structure'
    #pp.pprint(obj.project_vector)
    #pp.pprint(obj.user_ranking[0:10])
    
