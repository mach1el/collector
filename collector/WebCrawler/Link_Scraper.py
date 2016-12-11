#! -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup


url = 'https://pornhub.com'

my_request  = requests.get(url)
web_page    = my_request.content
html_parser = BeautifulSoup(web_page,'html.parser')

links       = []

print html_parser.title.string

for link in html_parser.find_all('a'):
	links.append(link.get('href'))

for link in links:
	if link != None and link.startswith('/'):
		pass