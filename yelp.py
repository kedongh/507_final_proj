import requests
import collections
import secrets
import json
import sqlite3

from bs4 import BeautifulSoup

API_KEY = secrets.API_KEY

headers = {
	"Authorization": "Bearer %s" % API_KEY
}

BASEURL = 'https://api.yelp.com/v3/businesses/search'

CACHE_DICT = {}
CACHE_FILENAME = 'search_cache.json'

DB_NAME = 'yelp.sqlite'

class Filter:

	def __init__(self):
		self.cities = []
		self.terms = []

	def add_city(self, city):
		if city not in self.cities:
			self.cities.append(city)

	def add_term(self, t):
		if t not in self.terms:
			self.terms.append(t)

	def show_city_list(self):
		return self.cities

	def show_term_list(self):
		return self.terms


class Business:

	def __init__(self, business):
		self.business_name = business.get('name', '')
		self.yelp_id = business.get('id', '')
		self.city = business.get('location', {}).get('city', '')
		self.phone_number = business.get('phone', '')
		self.review_count = business.get('review_count', -1)
		self.rating = business.get('rating', -1)
		self.price = business.get('price', '').count('$')
		self.url = business.get('url', '')
		self.address = business.get('location', {}).get('address1', '')

		if self.business_name == None: self.business_name = ''
		if self.yelp_id == None: self.yelp_id = ''
		if self.city == None: self.city = ''
		if self.phone_number == None: self.phone_number = ''
		if self.review_count == None: self.review_count = -1
		if self.rating == None: self.rating = -1
		if self.price == None: self.price = 0
		if self.url == None: self.url = ''
		if self.address == None: self.address = ''

		self.category = ['NULL'] * 3
		if 'categories' in business:
			for i in range(min(3, len(business['categories']))):
				self.category[i] = business['categories'][i]['title']

	def get_business_info(self):
		return [self.yelp_id, self.business_name, self.city, self.phone_number,
				self.review_count, self.rating, self.price, self.address, self.url]

	def get_category_info(self):
		return [self.yelp_id] + self.category
		

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Args:
    	None

    Returns:
    	cache_dict (dict): The opened cache.
    '''
    try:
    	cache_file = open(CACHE_FILENAME, 'r')
    	cache_contents = cache_file.read()
    	cache_dict = json.loads(cache_contents)
    	cache_file.close()
    except:
    	cache_dict = {}

    return cache_dict

def save_cache(cache_dict):
	''' Saves the current state of the cache to disk

	Args:
		cache_dict (dict): The dictionary to save.

	Returns:
		None
	'''
	dumped_json_cache = json.dumps(cache_dict)
	fw = open(CACHE_FILENAME, "w")
	fw.write(dumped_json_cache)
	fw.close()


def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and
    repeatably identify an API request by its baseurl and params

    Args:
    	baseurl (str): The URL for the API endpoint.
    	params (dict): A dictionary of param:value pairs.

    Returns:
    	unique_key (str): The unique key as a string.
    '''
    param_string = []
    connector = "_"

    for k in params.keys():
        param_string.append(f"{k}_{params[k]}")

    param_string.sort()
    unique_key = baseurl + connector + connector.join(param_string)

    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params

    Args;
    	baseurl (str): The URL for the API endpoint.
    	params (dict): A dictionary of param:value pairs.

    Returns:
    	results (dict): The JSON response from the request.
    '''
    response = requests.get(baseurl, params=params, headers=headers)
    results = response.json()
    return results


def make_request_with_cache(baseurl, term='', location='', count=50):
	''' Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    Args:
    	baseurl (str): The URL for the API endpoint
    	term (str): The search term passes to the API.
    	location (str): The search location passes to the API.
    	count (int): The number of business results to return.

    Return:
    	results (dict): The JSON response from the request.
	'''
	params = {
		'term': term.lower().replace(" ", "+"),
		'location': location.lower().replace(" ", "+"),
		'limit': count
	}
	request_key = construct_unique_key(baseurl=baseurl, params=params)

	if request_key in CACHE_DICT:
		# The data has been fetched before and stored in the cache
		return CACHE_DICT[request_key]
	else:
		results = make_request(baseurl=baseurl, params=params)
		CACHE_DICT[request_key] = results
		save_cache(cache_dict=CACHE_DICT)
		return results


def write_to_business_single(info):
	''' Write a row into business_info table

	Args:
		info (list): A list of business information.

	Returns:
		None
	'''
	insert_instructors = '''
		INSERT OR REPLACE INTO business_info
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
	'''
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()
	cursor.execute(insert_instructors, info)
	connection.commit()
	connection.close()

def write_to_category_single(info):
	''' Write a row into category_info table.
	
	Args:
		info (list): A list of category info of one business.

	Returns:
		None
	'''
	insert_instructors = '''
		INSERT OR REPLACE INTO category_info
		VALUES (?, ?, ?, ?)
	'''
	connection = sqlite3.connect(DB_NAME)
	cursor = connection.cursor()
	cursor.execute(insert_instructors, info)
	connection.commit()
	connection.close()

def write_to_business(list):
	''' Write multiple rows into business_info table.

	Args:
		list (list): A list of business objects.

	Returns:
		None
	'''
	for busi_obj in list:
		write_to_business_single(busi_obj.get_business_info())

def write_to_category(list):
	''' Write multiple rows into category_info table.

	Args:
		list (list): A list of business objects.
	
	Returns:
		None
	'''
	for busi_obj in list:
		write_to_category_single(busi_obj.get_category_info())

def get_business_list(term='', location='', count=50):
	''' Fetch the data throught API and process the JSON
	response into two lists.

	Args:
		term (str): The search term passed into API.
		location (str): The search location passed into API.
		count (int): The number of business results to return.

	Returns:
		business_list (list): A list of business objects.
	'''
	results = make_request_with_cache(baseurl=BASEURL,
									term=term, location=location, count=count)
	business_info = results['businesses']

	business_list = []
	for business in business_info:
		business_list.append(
			Business(business)
			)

	return business_list



if __name__ == '__main__':
	# term = 'barbecue'
	# city = 'New York'
	# busi_list = get_business_list(term=term, location=city, count=50)
	# write_to_business_single(busi_list[31].get_business_info())

	f = Filter()

	f.add_term('Chinese restaurants')
	f.add_term('Japanese restaurants')
	f.add_term('Indian restaurants')
	f.add_term('Mediterranean restaurants')
	f.add_term('breakfast')
	f.add_term('barbecue')
	f.add_term('coffee')
	f.add_term('noodles')
	f.add_term('food')
	f.add_term('hamburger')
	f.add_term('sandwich')
	f.add_term('bubble tea')
	f.add_term('taco')
	f.add_term('dumplings')
	f.add_term('Korean')
	f.add_term('sushi')
	f.add_term('ramen')
	f.add_term('curry')
	f.add_term('cocktail')
	f.add_term('bar')
	f.add_term('seafood')
	f.add_term('hot pot')
	f.add_term('steak')
	f.add_term('Vegetarian')

	f.add_city('San Francisco')
	f.add_city('Seattle')
	f.add_city('New York')
	f.add_city('Ann Arbor')
	f.add_city('San Jose')
	f.add_city('Boston')
	f.add_city('Los Angeles')
	f.add_city('Las Vegas')
	f.add_city('Chicago')
	f.add_city('Washington')
	f.add_city('Detroit')

	for term in f.show_term_list():
		for city in f.show_city_list():
			print(term, city)
			busi_list = get_business_list(term=term, location=city, count=50)
			write_to_business(busi_list)
			write_to_category(busi_list)














