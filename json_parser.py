'''
Created on Apr 11, 2013

@author: Suvodeep Pyne
'''
import pprint as pp
import json

json_data = open('sample_data.json')
data = json.load(json_data)
pp.pprint(data)