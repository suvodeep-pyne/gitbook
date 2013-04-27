'''
Created on Apr 26, 2013

@author: Suvodeep Pyne
'''
from read_data import DataRetriever

GITHUB_DATA = 'github_data'

class Recommender():
    
    projects = {}
    
    def __init__(self):
        directory_name = GITHUB_DATA
        self.data_retriever = DataRetriever(directory_name)
        self.project_data = self.data_retriever.parseProjectData()
        self.user_data = self.data_retriever.parseUserData()
    
    def get_recommended_projects(self, preferences):
        pass
    
    def build_projects_vector(self):
        for name, project in self.project_data.iteritems():
            self.projects[name] = {}
            
            
            
            
if __name__ == '__main__':
    obj = Recommender()
    print obj.get_recommended_projects(5)