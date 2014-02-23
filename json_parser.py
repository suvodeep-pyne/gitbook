'''
Created on Apr 11, 2013

@author: Suvodeep Pyne
'''
import pprint as pp
import json
from resource_manager import ResourceManager

rm = ResourceManager()

json_data = open(rm.get_resource('sample_data.json'))
data = json.load(json_data)
pp.pprint(data)
