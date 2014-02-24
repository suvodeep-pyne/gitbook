'''
Created on Feb 23, 2014

@author: Suvodeep Pyne
@Description: This class is responsible for handling all links to files.

Note: This class must be in the working directory.
'''
import os

join = os.path.join

class ResourceManager():
    DATA = 'data'
    CACHE = join(DATA, 'cache')
    CRAWL = join(DATA, 'crawl')

    TRAINDATA = join(DATA, 'train_data')
    TRAINDATA_VOCAB = join(TRAINDATA, 'vocabulary')
    TRAINDATA_DATASET = join(TRAINDATA, 'dataset')

    PROJECTDATA = join(CRAWL, 'projects')
    USERDATA = join(CRAWL, 'users')

    NB_PROB = join(CACHE, 'nb_prob')
    LOC = join(DATA, 'proj_loc')

    def __init__(self):
        self.PROJECTCONTRIBUTORS = os.path.join(self.DATA, "project_contributors.p")

    def get_resource(self, id):
        return join(self.DATA, id)


if __name__ == '__main__':
    print 'Resource Manager Test'
    rm = ResourceManager()
    print rm.TRAINDATA_VOCAB
    print rm.NB_PROB
    print rm.get_resource('sample_data.json')
