'''
Created on Apr 26, 2013

@author: Suvodeep Pyne
Edited by Garima Agarwal
'''

import operator
import pickle
import pickle
import cmd
import pprint as pp

from page_rank import pagerank
from collections import defaultdict
from read_data import DataRetriever
from nb_classifier import NaiveBayesClassifier

GITHUB_DATA = 'data_ash'
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
            readme = project['readme']
            
            # Bad case: When readme is not found. It returns empty lists.
            if isinstance(readme, list): 
                readme = ""
            else:
                readme = unicode(readme, 'utf-8', errors = 'ignore')

            if project['description'] != None:
                readme += project['description']
            
            if readme == "":    continue

            self.projects[name] = {}
            prob_data = self.nb.classify(readme)[0]
            self.projects[name]['class_prob'] = prob_data
            self.projects[name]['description'] = project['description']
            if len(prob_data) > 0:
                self.projects[name]['category'] = max(prob_data.iteritems(), key=operator.itemgetter(1))[0]
        return self.projects
    
            
class Recommender():
    """Initialize the recommender"""
    def __init__(self):
        directory_name = GITHUB_DATA
        print "Reading data..........."
        self.data_retriever = DataRetriever(directory_name)
        print "Done reading data"
        self.project_data = self.data_retriever.parseProjectData()
        self.user_data, self.user_follower_map = self.data_retriever.parseUserFollowers()
        print "Training Naive's Bayes classifier"
        self.project_vector_builder = ProjectVectorBuilder(self.project_data)
        print "Trained!!!"
        self.language_proj = defaultdict()   

    def get_languages(self):
        lang_dict = {}
        
        for lang in language_proj.keys():
            _lang = lang.replace(' ','$')
            lang_dict[_lang] = lang
        return lang_dict        

    def get_aoi(self):
        return self.project_vector_builder.nb.clf.classes_
    
    """Get different scores for each project"""
    def build_project_features(self):
        self.project_vector = self.project_vector_builder.build_projects_vector()
        #self.user_ranking = pagerank(self.user_data, self.user_follower_map)
        with open('lang_to_projects.p') as f:
          self.language_proj = pickle.load(f)
        
        with open('new_LOC.p','rb') as f:
          self.difficulty_score = pickle.load(f)
                 
    def recommend_projects(self, languages, area_interest, difficulty): 
        print "Calling recommender"
        projects = set()
        print languages
        print area_interest
        print difficulty
        for language in languages:
            projects = projects.union(self.language_proj[language]) 
        
        similar_projects = []
        for project in projects:
            if project not in self.project_vector:   continue

            if self.project_vector[project]['category'] in area_interest:
                similar_projects.append(self.project_vector[project])
            
        pp.pprint(similar_projects)

class CommandLineInterface(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.obj = Recommender()
        self.obj.build_project_features()
        self.name = "garima"
        self.prompt = ">> "
    
    def do_recommend_projects(self, args):
        languages, aoi, level = args.split("\" \"")
        languages = languages.replace("\"", "")
        level = level.replace("\"", "")
        self.obj.recommend_projects(languages.split(), [aoi], level)
    
    def do_EOF(self, args):
        return self.do_exit(args)
 
    def do_exit(self, args):
        """Exit"""
        return -1  
    
    def do_help(self, args):
        cmd.Cmd.do_help(self, args)

if __name__ == '__main__':
    cmi = CommandLineInterface()
    cmi.cmdloop()
    #print obj.get_languages()
    #print obj.get_aoi()
    print "Getting recommended projects"
    print 'Printing projects Data Structure'
    #pp.pprint(obj.projects)
    #pp.pprint(obj.project_vector)
    #pp.pprint(obj.user_ranking[0:10])
    
