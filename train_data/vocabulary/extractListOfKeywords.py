import re
from bs4 import BeautifulSoup
html_doc = open("List_of_programming_and_computer_science_terms.htm", 'r')
html_content = html_doc.read()
soup = BeautifulSoup(html_content)
allTags =  soup.find_all(id="mw-content-text")
allTagsContents = allTags[0].contents
item = allTags[0]
lists = item.find_all('ul')
fw = open('allTerms.txt', 'w')
for itlist in lists:
  KeywordList = itlist.find_all('li')
  for item in KeywordList:
    try:
      textRaw = item.contents[0].contents[0].encode('utf8')
      textRaw = re.sub('-','',textRaw)
      text = re.split('[\W]+',textRaw,flags=re.UNICODE)
      for word in text:
        fw.write(word)
        fw.write(' ')
      #print text
    except AttributeError:
      print "******************************************************************************"
fw.close()
html_doc.close()





