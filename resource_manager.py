'''
Created on Feb 23, 2014

@author: Suvodeep Pyne
@Description: This class is responsible for handling all links to files.

Note: This class must be in the working directory.
'''
import os

class ResourceManager():
    join = os.path.join

    DATA = 'data'
    CACHE = join(DATA, 'cache')

    TRAINDATA = join(DATA, 'train_data')
    TRAINDATA_VOCAB = join(TRAINDATA, 'vocabulary')
    TRAINDATA_DATASET = join(TRAINDATA, 'dataset')

    NB_PROB = join(CACHE, 'nb_prob')

    def __init__(self):
        self.PROJECTCONTRIBUTORS = os.path.join(self.DATA, "project_contributors.p")

    def get_resource(self, id):
        return os.path.join(self.DATA, id)


if __name__ == '__main__':
    print 'Resource Manager Test'
    rm = ResourceManager()
    print rm.TRAINDATA_VOCAB
    print rm.NB_PROB
