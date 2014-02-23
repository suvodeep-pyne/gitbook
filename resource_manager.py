'''
Created on Feb 23, 2014

@author: Suvodeep Pyne
@Description: This class is responsible for handling all data files for the project.

Note: This class must be in the working directory.
'''
import os

class ResourceManager():
    DATA = 'data'

    def get_resource(self, id):
        return os.path.join(self.DATA, id)

