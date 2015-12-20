import pdb
import variables
import requests
from lxml import html

def scrapper(url):

	x = robotcheck(url)
	variables.logging.info('ROBOT: %s  %s', x, url) 
	if not x:
		return

	page = requests.get(url)
	tree = html.fromstring(page.content)
	links = tree.xpath('//a/@href')

	for i, link in enumerate(links):
	    if not link.startswith('http'):
		links[i] = url + link
	    if not link.endswith('/'):
		links[i] = links[i] + '/' 

	for link in links:
	    if link not in variables.scrapped:
	        variables.queue.append(link)

	variables.scrapped.append(url)

# Check to see if url is allowed in robots.txt. Returns 1 if url not in robots.txt and 0 if url is in robots.txt or error has occured.
# Input url's must end in '/'
def robotcheck(url):

	# Convert url into robots.txt url
	split_url = url.split('/')
	domain_url = split_url[0] + '//' + split_url[2] 
	robot_url = domain_url + '/robots.txt'

	# Request url's robots.txt and save content into temp_array
	robot_txt = requests.get(robot_url).content.splitlines()

	# Declare variables needed in the processing of robot.txt
	forbidden_urls = []
	found_UserAgent = 0

	# Create array of forbidden urls from robot.txt 
	for line in robot_txt:
		
		# Check if found global user-agent or if come to end of global user-agent
		if line.lower().startswith('user-agent'):
			if line.split(' ')[1] != '*':
				found_UserAgent = 0
			elif line.split(' ')[1] == '*':	
				found_UserAgent = 1

		# Add all disallowed urls to forbidden_urls
		if found_UserAgent == 1 and line.lower().startswith('disallow:'):
			tmp_line = line.split(' ')
			if len(tmp_line) > 1:

				# Check there are no comments attached to url before adding to forbidden_urls 
				tmp_line = tmp_line[1].split('#')[0]

				# Add '/' on to end of line if needed
				if not tmp_line.endswith('/'):
					tmp_line = tmp_line + '/'

				# Add to forbidden urls
				forbidden_urls.append(tmp_line)

	# Convert url into robot.txt form
	url = '/' + '/'.join(split_url[3:len(split_url)]) #convert to lower case

	# Check if url is in forbidden list from robots.txt
	for line in forbidden_urls:

		# Check if url is forbidden
		if url == line:
			return 0
	
	# Check if forbidden_urls was successfully filled before returning TRUE
	if len(forbidden_urls):	
		return 1	
	else:
		variables.logging.info('Empty robots.txt for %s', robot_url)
		return 0	

def pop():
	
	if len(variables.queue) == 0:
		raise Exception('URL Queue Empty') 
		return

	url = variables.queue.popleft()
	base = url.split('/')[2] #improve hostname func e.g. ?x=y or www.x and just x: turn temp into IP address history

	if url in variables.scrapped:
		try:	
			return pop()
		except:
			raise
			return
	elif base in variables.temp:
		variables.queue.append(url)
		try:
			return pop()
		except:
			raise
			return
	variables.temp.popleft()
	variables.temp.append(base)
	return url

