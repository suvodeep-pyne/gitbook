
#from recommender import Recommender

class GitBook():
	#recommender = Recommender()
	
	def __init__(self):
		print 'Launched GitBook instance'
		
	def get_languages(self):
		languages = ['RUby']
		return languages
		
	def get_areas_of_interest(self):
		aoi = ['machine-learning', 'artificial-intelligence']
		return aoi
	
if __name__ == '__main__':
    obj = GitBook()
    print 'Done.'    