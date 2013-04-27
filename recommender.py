'''
Created on Apr 26, 2013

@author: Suvodeep Pyne
'''

import pprint as pp

from read_data import DataRetriever
from nb_classifier import NaiveBayesClassifier

GITHUB_DATA = 'github_data'

class Recommender():
    
    projects = {}
    
    def __init__(self):
        directory_name = GITHUB_DATA
        self.data_retriever = DataRetriever(directory_name)
        self.project_data = self.data_retriever.parseProjectData()
        self.user_data = self.data_retriever.parseUserData()
        
        self.nb = NaiveBayesClassifier('train_data\\vocabulary', 'train_data\\dataset')
        self.nb.train()
    
    def get_recommended_projects(self, preferences):
        pass
    
    def build_projects_vector(self):
        for name, project in self.project_data.iteritems():
            self.projects[name] = {}
            readme = project['readme']
            
            # Bad case: When readme is not found. It returns empty lists.
            if isinstance(readme, list): continue
            try:
                readme = readme.encode('utf8', 'ignore')
                self.projects[name]['class_prob'] = self.nb.classify(readme)
            except:
                pass
            
            
if __name__ == '__main__':
    obj = Recommender()
    print obj.build_projects_vector()
    print obj.get_recommended_projects(5)
    
    print 'Printing projects Data Structure'
    pp.pprint(obj.projects)
    print 'Size of Project_data:', len(obj.project_data)
    print 'Size of projects:', len(obj.projects)
    