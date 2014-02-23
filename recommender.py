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
from resource_manager import ResourceManager

rm = ResourceManager()

class ProjectVectorBuilder():
    
    projects = {}
    
    def __init__(self, project_data):
        self.project_data = project_data
        
        self.nb = NaiveBayesClassifier(rm.TRAINDATA_VOCAB, rm.TRAINDATA_DATASET)
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
        directory_name = rm.CACHE
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
        return self.categories
    
    """Get different scores for each project"""
    def build_project_features(self):
        try:    
            with open(rm.NB_PROB, 'rb') as f:
                print "Reading probabilities from:", rm.NB_PROB
                self.project_vector = pickle.load(f)
                self.categories = pickle.load(f)

                print 'done.'
                print '#Projects:', len(self.project_vector)
                print '#Categories:', len(self.categories)
        except:
            print "Generating a new Naive Base classifier"
            self.project_vector_builder = ProjectVectorBuilder(self.project_data)
            self.project_vector = self.project_vector_builder.build_projects_vector()
            self.categories = list(self.project_vector_builder.nb.clf.classes_)
            with open(rm.NB_PROB, 'wb') as f:
                pickle.dump(self.project_vector, f)
            with open(rm.NB_PROB, 'ab') as f:
                pickle.dump(self.categories, f)

        self.user_ranking = pagerank(self.user_data)
        with open(os.path.join(rm.CACHE, 'lang_to_projects.p'), 'rb') as f:
          self.language_proj = pickle.load(f)
        
        with open(os.path.join(rm.CACHE, 'new_LOC.p'),'rb') as f:
          self.difficulty_score = pickle.load(f)
                 
    def recommend_projects(self, languages, area_interest, difficulty): 
        print "Calling recommender"
        projects = set()
        #Filter based on languages
        for language in languages:
            projects = projects.union(self.language_proj[language]) 
        
        similar_projects = []
        for project in projects:
            if project not in self.project_vector:   continue

            if self.project_vector[project]['category'] in area_interest:
                project_desc = self.project_vector[project]
                project_desc['html_url'] = self.project_data[project]['html_url']
                project_desc['full_name'] = self.project_data[project]['full_name']
                similar_projects.append(project_desc)
        
        sorted_similar_projects = sorted(similar_projects, key=lambda k: k['prob'], reverse=True) 
        #pp.pprint(sorted_similar_projects)
        zipped = map(list, zip(*self.user_ranking))
        userLists = zipped[0]
        PRs = zipped[1]
        sortedProjsLength = len(sorted_similar_projects)
        for i in range(0,len(sorted_similar_projects)):
          proj = sorted_similar_projects[i]
          project = self.project_data[proj[u'full_name']]
          owner = project[u'owner']
          if owner[u'login'] in userLists:
            userIndex = userLists.index(owner[u'login'])
            sorted_similar_projects[i]['page_rank_of_owner'] = PRs[userIndex]
            sorted_similar_projects[i]['owner'] = owner[u'login']
            #sorted_similar_projects[i]['contributors'] = self.project_data[proj['full_name']]['contributors'][0]['login']
            if len(self.project_data[proj['full_name']]['contributors']) >=1:
              sorted_similar_projects[i]['contributors'] = self.project_data[proj['full_name']]['contributors'][0]['login']
              sorted_similar_projects[i]['contributors_url'] = self.project_data[proj['full_name']]['contributors'][0]['html_url']
            else:
              sorted_similar_projects[i]['contributors'] = ''
              sorted_similar_projects[i]['contributors_url'] ='' 
          else:
            sorted_similar_projects[i]['page_rank_of_owner'] = 0
            sorted_similar_projects[i]['owner'] = owner[u'login']
            if len(self.project_data[proj['full_name']]['contributors']) >=1:
              sorted_similar_projects[i]['contributors'] = self.project_data[proj['full_name']]['contributors'][0]['login']
              sorted_similar_projects[i]['contributors_url'] = self.project_data[proj['full_name']]['contributors'][0]['html_url']
            else:
              sorted_similar_projects[i]['contributors'] = ''
              sorted_similar_projects[i]['contributors_url'] = ''

        # sort the sorted_similar_projects based on the key 'page_rank_of_owner' value
        # have the contributors tag with the first contributor for the server side handling


        #"""
        if len(sorted_similar_projects) > 10:
          firstListToSort = sorted_similar_projects[0:sortedProjsLength/2]
          secListToSort = sorted_similar_projects[sortedProjsLength/2 + 1 : sortedProjsLength*4/5 ]
          thirListToSort = sorted_similar_projects[sortedProjsLength*4/5 + 1 : ]
          #"""
         
          sorted1 =  sorted(firstListToSort, key=lambda k: k['page_rank_of_owner'], reverse=True) 
          sorted2 =  sorted(secListToSort, key=lambda k: k['page_rank_of_owner'], reverse=True) 
          sorted3 =  sorted(thirListToSort, key=lambda k: k['page_rank_of_owner'], reverse=True) 
         
          #print len(sorted1)
          #print len(sorted2)
          #print len(sorted3)
         
          sorted1.extend(sorted2)
          sorted3.extend(sorted1)
          #pp.pprint(sorted3)
         
          #print 'lenght after merging all: ',len(sorted3)

          return sorted3

        return sorted_similar_projects

class CommandLineInterface(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.obj = Recommender()
        self.obj.build_project_features()
        self.name = "garima"
        print self.obj.get_aoi()
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
