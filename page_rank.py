'''
Author: Garima Agarwal
Created on April 26, 2013
'''
import math
import time
import sys
import pprint as pp
import operator

from read_data import *

ALPHA = 0.9
ERROR_BOUND = 0.0000001

user_followers = {}
pr_graph = {}
pr = {}
unique_user = set()

def init(graph):
    pr_graph.clear()
    build_pr_graph(graph)
    
    pr.clear()
    pr0 = (float)(1.0) / len(unique_user)
    
    for uid in unique_user: pr[uid] = pr0
    
    for uid in unique_user:
        if uid not in user_followers:
            user_followers[uid] = 1
 
def build_pr_graph(user_graph):
    for user in user_graph:
        mentions = user_graph[user]
        unique_user.add(user)
        if len(mentions) > 0:
            if user not in pr_graph: pr_graph[user] = set()
            for out_user in mentions:
                if out_user not in pr_graph: pr_graph[out_user] = set()
                unique_user.add(out_user)
                pr_graph[out_user].add(user)

def compute(user_graph):
    print 'Computing pagerank on users...'
    print 'Using Damping factor(ALPHA):', ALPHA
    print 'Using Root Mean Squared Error bound:', ERROR_BOUND
    print
    
    iter_count = 1
    global pr
    
    init(user_graph)
    tlprt_val = (1.0 - ALPHA) / len(user_followers)
    iters = 1
    while True:
        # Initialize the new pagerank structure
        new_pr = {}
        
        # Obtain contributions from the in links
        err = 0
        total_pr = 0 # required for normalization
        for user in pr_graph:
            inlink_sum = 0
            for in_user in pr_graph[user]:
                inlink_sum += pr[in_user] / len(user_graph[in_user])
            new_pr[user] = ALPHA * inlink_sum + tlprt_val
            total_pr += new_pr[user]
            err += (new_pr[user] - pr[user]) ** 2
                
        err = math.sqrt(err)
        print 'Iteration: %d Error: %.7f' % (iter_count, err)
        
        #has_converged = err <= ERROR_BOUND
        pr = new_pr
        has_converged = err <= ERROR_BOUND
        
        if has_converged: 
            # Scaling pagerank value to 0.0 to 1.0 scale
            for user in pr:
                pr[user] /= total_pr
            print 'Pagerank Converged. Scaling to [0,1]'
            break
        iter_count += 1

def pagerank(user):
    """
    if len(user_graph) == 0:
        sys.stderr.write('Error: No user graph created.\n')
        sys.stderr.write('Please run the index command first!\n')
        return
    """
    t0 = time.clock()
    
    user_map = user
    compute(user_map)
        
    # transfer your data into a more usable format
    #results = [(pr[userid], cr.uid_name_map[userid]) for userid in pr]
    
    # sort on descending score
    ranked_users = sorted(pr.iteritems(), key=operator.itemgetter(1), reverse=True)
    
    name, scale_value = ranked_users[0]
    ranked_users[0] = (name, 1)
    users_ranking = map(lambda x: (x[0], x[1] / scale_value), ranked_users[1:])
    users_ranking = [ranked_users[0]] + users_ranking
    #normalize the scores
    return users_ranking
   
    """ 
    print
    print '#Users in pr_graph:', len(pr_graph)
    print 'Page rank convergence: %3f sec' % (t1 - t0)        
    print
    """

if __name__ == '__main__':
    from resource_manager import ResourceManager
    rm = ResourceManager()
    directory_name = rm.CACHE

    data_retriever = DataRetriever(directory_name)
    user_data, user_follower_map = data_retriever.parseUserFollowers()
    # print user_data
    # print user_follower_map

    user_ranking = pagerank(user_data)
    # user_ranking = pagerank(user_data, user_follower_map)
