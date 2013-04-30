'''
Created on Apr 26, 2013

@author: Suvodeep Pyne
Edited by Garima Agarwal
'''

import os
import cmd
import pickle
import pickle
import marshal
import operator
import pprint as pp

from page_rank import pagerank
from collections import defaultdict
from read_data import DataRetriever
from nb_classifier import NaiveBayesClassifier

GITHUB_DATA = 'github_data'
TRAIN_DATA = 'train_data'
naive_prob_file = os.path.join(GITHUB_DATA, 'prob')
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
                self.projects[name]['prob'] = max(prob_data.iteritems(), key=operator.itemgetter(1))[1]
        return self.projects
    
            
class Recommender():
    """Initialize the recommender"""
    def __init__(self):
        print 'Initializing Recommender..'
        directory_name = GITHUB_DATA
        self.data_retriever = DataRetriever(directory_name)
        self.project_data = self.data_retriever.parseProjectData()
        self.user_data, self.user_follower_map = self.data_retriever.parseUserFollowers()
        self.language_proj = defaultdict()   

    def get_languages(self):
        lang_dict = {}
        
        for lang in self.language_proj.keys():
            _lang = lang.replace(' ','$')
            lang_dict[_lang] = lang
        return lang_dict        

    def get_aoi(self):
        return self.project_vector_builder.nb.clf.classes_
    
    """Get different scores for each project"""
    def build_project_features(self):
        try:    
            with open(naive_prob_file, 'rb') as f:
                print "Reading probabilities from the file"
                self.project_vector = marshal.load(f)
        except:
            print "Generating a new Naive Base classifier"
            self.project_vector_builder = ProjectVectorBuilder(self.project_data)
            self.project_vector = self.project_vector_builder.build_projects_vector()
            with open(naive_prob_file, 'wb') as f:
                marshal.dump(self.project_vector, f)

        #self.user_ranking = pagerank(self.user_data, self.user_follower_map)
        with open(os.path.join(GITHUB_DATA, 'lang_to_projects.p'), 'rb') as f:
          self.language_proj = pickle.load(f)
        
        with open(os.path.join(GITHUB_DATA, 'new_LOC.p'),'rb') as f:
          self.difficulty_score = pickle.load(f)
                 
    def recommend_projects(self, languages, area_interest, difficulty): 
        print "Calling recommender"
        projects = set()
        print languages
        print area_interest
        print difficulty
        #Filter based on languages
        for language in languages:
            projects = projects.union(self.language_proj[language]) 
        
        similar_projects = []
        for project in projects:
            if project not in self.project_vector:   continue

            if self.project_vector[project]['category'] in area_interest:
                project_desc = self.project_vector[project]
                project_desc['html_url'] = self.project_data['html_url']
                project_desc['full_name'] = self.project_data['full_name']
                similar_projects.append(project_desc)
        
        sorted_similar_projects = sorted(similar_projects, key=lambda k: k['prob'], reverse=True) 
        return sorted_similar_projects

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
    
