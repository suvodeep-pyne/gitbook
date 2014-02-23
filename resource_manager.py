'''
Created on Feb 23, 2014

@author: Suvodeep Pyne
@Description: This class is responsible for handling all data files for the project.

Note: This class must be in the working directory.
'''
import os

class ResourceManager():
    DATA = 'data'

    def __init__(self):
        self.TRAINDATA = os.path.join(self.DATA, "train_data")
        self.PROJECTCONTRIBUTORS = os.path.join(self.DATA, "project_contributors.p")
        self.TRAINDATA_VOCAB = os.path.join(self.TRAINDATA, "vocabulary")
        self.TRAINDATA_DATASET = os.path.join(self.TRAINDATA, "dataset")

    def get_resource(self, id):
        return os.path.join(self.DATA, id)

