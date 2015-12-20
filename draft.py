import pdb

from collections import deque
from lxml import html
import requests 

TEMP_ARRAY = 10

queue = deque(['https://pymotw.com/2/pdb','http://www.stackoverflow.com'])
scrapped = []
temp = deque([])
for x in range(0,TEMP_ARRAY):
	temp.append(None)

def scrapper(url):
	global scrapped, queue, temp

	page = requests.get(url)
	tree = html.fromstring(page.content)
	links = tree.xpath('//a/@href')

	for i, link in enumerate(links):
	    if not link.startswith('http'):
		links[i] = url + link
	    if link.endswith('/'):
		links[i] = links[i][:-1] 

	for link in links:
	    if link not in scrapped:
	        queue.append(link)

	scrapped.append(url)

def robotcheck(url):
	url = url.split('/')
	robot_url = url[0] + '//' + url[2] + '/robots.txt'
	robot = requests.get(url)
	return robot.content.splitlines()

def pop():
	global scrapped, queue, temp	
	
	if len(queue) == 0:
		raise Exception('URL Queue Empty') 
		return

	url = queue.popleft()
	base = url.split('/')[2]

	if url in scrapped:
		try:	
			return pop()
		except:
			raise
			return
	elif base in temp:
		queue.append(url)
		try:
			return pop()
		except:
			raise
			return
	temp.popleft()
	temp.append(base)
	return url

for x in range(0,2):		
	try:
		print 'x = ',x
		url = pop()
		scrapper(url)
	except Exception as err:
		print err

########TESTING###########
#print 'temp = ', temp
#print 'queue = ', queue
print 'Length of queue = ', len(queue)
print 'temp = ', temp

tmp = []
for i, url in enumerate(queue):
	tmp += url.split('/')[2]
print 'Different hostnames in queue = ', len(set(tmp))

print robotcheck('http://www.stackoverflow.com')

	


