from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

BASE_CRAIGLIST_URL = 'https://bhubaneswar.craigslist.org/search/?query={}'
# Create your views here.
def home(request):
	return render(request, 'base.html')

def new_search(request):
	search = request.POST.get('search')
	models.Search.objects.create(search=search)
	final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
	response = requests.get(final_url)
	data=response.text
	#print(data)
	soup = BeautifulSoup(data, features='html.parser')

	post_listings = soup.find_all('li', {'class':'result-row'})

	post_title = post_listings[0].find(class_='result-title hdrlnk').text
	post_url = post_listings[0].find('a').get('href')
	
	final_postings = []

	for post in post_listings:
		post_title = post.find(class_='result-title hdrlnk').text
		post_url = post.find('a').get('href')

		final_postings.append((post_title, post_url))


	frontend_stuff = {
		'search' : search,
		'final_postings' :final_postings
	}
	return render(request, 'dhundo/new_search.html', frontend_stuff)