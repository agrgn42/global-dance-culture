import json
import requests
import webbrowser
import csv
from secret_data import FLICKR_KEY, NYT_KEY, CARTO_USERNAME, CARTO_KEY
from geotext import GeoText
from carto.auth import APIKeyAuthClient
from carto.datasets import DatasetManager
from carto.maps import NamedMapManager, NamedMap
from carto.sql import BatchSQLClient
import time

CACHE_FNAME = 'dancemap.json'

try:
	cache_file = open(CACHE_FNAME, 'r')
	cache_contents_str = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents_str)
	cache_file.close()
except: 
    CACHE_DICTION = {}

fcountries = "countries.json"
fcountries_obj = open(fcountries, "r")
fcountries_contents = fcountries_obj.read()
COUNTRIES_DICT = json.loads(fcountries_contents)
fcountries_obj.close()


######################################################-----NEW YORK TIMES -----###############################################################

def params_unique_combination(baseurl, params_d):
	alphabetized_keys = sorted(params_d.keys())
	results_keys=[]
	for k in alphabetized_keys:
		results_keys.append("{}-{}".format(k, params_d[k]))
	return baseurl + "_".join(results_keys)

def get_nyt_data(search_term, page=0):
	baseurl = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
	params_diction = {}	
	params_diction['api-key'] = NYT_KEY
	params_diction['q'] = search_term
	params_diction['fl'] = "web_url", "snippet", "lead_paragraph", "abstract", "print_page", "source", "headline", "keywords", "pub_date", "byline","_id", "word_count"
	params_diction['hl'] = True
	params_diction['page'] = page
	unique_identifier = params_unique_combination(baseurl,params_diction)
	if unique_identifier in CACHE_DICTION:	
		print('Getting cached data...')
		return CACHE_DICTION[unique_identifier]
	else:
		print('Making request for new data...')
		nyt_resp = requests.get(baseurl, params_diction)
		nyt_text = json.loads(nyt_resp.text)
		if nyt_text == {'message': 'Invalid authentication credentials'}:
		 	print("\nSorry, it appears the way you input your New York Times Article Search API key may be incorrect. Please try pasting it in again.\n")
		CACHE_DICTION[unique_identifier] = json.loads(nyt_resp.text)
		dumped_json_cache = json.dumps(CACHE_DICTION)
		filew = open(CACHE_FNAME, "w")
		filew.write(dumped_json_cache)
		filew.close()
		return CACHE_DICTION[unique_identifier]

print("\nThe program will now request the most recent 100 articles from the New York Times API that include the keyword 'dance'.\n")
dance_request = get_nyt_data("dance")
dance_request1 = get_nyt_data("dance", 1)
dance_request2 = get_nyt_data("dance", 2)
dance_request3 = get_nyt_data("dance", 3)
dance_request4 = get_nyt_data("dance", 4)
dance_request5 = get_nyt_data("dance", 5)
dance_request6 = get_nyt_data("dance", 6)
dance_request7 = get_nyt_data("dance", 7)
dance_request8 = get_nyt_data("dance", 8)
dance_request9 = get_nyt_data("dance", 9)

class Article(object):
	def __init__(self, post_dict={}):
		self.title = post_dict["headline"]["main"]
		for elem in post_dict["keywords"]:
			self.keywords = elem["value"]
		self.abstract = post_dict["snippet"]
		if "pub_date" in post_dict:
			self.date_published = post_dict["pub_date"]
		else:
			self.date_published = ""
		self.article_url = post_dict["web_url"]
	
	def places_mentioned(self):
		places = GeoText(self.abstract)
		countries_mentioned_dict = places.country_mentions
		self.countries_mentioned = countries_mentioned_dict
		return self.countries_mentioned

	def __str__(self):
		return '{}\n{}\n{}\n{}\n'.format(self.title, self.abstract, self.date_published, self.article_url)

article_instances = []
for k,v in CACHE_DICTION.items():
	if 'nytimes' in k:
		if "response" in v:
			for diction in (v["response"]["docs"]):
				article_instances.append(Article(diction))

print('\n{}\n{}\n'.format("Here's an example of what your request for articles containing 'dance' returned:", article_instances[0]))


######################################################-----FLICKR-----###############################################################


def get_photo_keywords(article_instances_lst):
	country_frequency_mentions = {}						#this determines frequency of country mentions
	for article in article_instances:
		for k,v in article.places_mentioned().items():	#this is a dictionary of items
			if k not in country_frequency_mentions:
				country_frequency_mentions[k] = v
			else:
				country_frequency_mentions[k] += v
	print('{}\n{}\n'.format("The countries mentioned and the frequency of their mentions in the New York Times article abstracts are:", country_frequency_mentions))
	sorted_country_frequency_mentions = sorted(country_frequency_mentions.items(), key=lambda x: x[1], reverse=True)
	most_frequent_country = []							#this determines most frequent country
	base_count = 0
	for each in sorted_country_frequency_mentions:		#this is a dictionary of items
		if 'US' not in each:
			if each[1] > base_count:								
				base_count = each[1]
				most_frequent_country.append(each[0])				#this is a now a list of the keys of the countries 
			elif each[1] == base_count:
				most_frequent_country.append(each[0])
	most_frequent_country_for_flickr = []					#this formats frequncy of country output for csv
	for country_code in most_frequent_country:
		for diction in COUNTRIES_DICT:
			if country_code in diction["country"]:
				most_frequent_country_for_flickr.append({"country_name": diction["name"], "geo_lat": diction["latitude"], "geo_long": diction["longitude"]})
	print('{}\n{}\n'.format("The most frequently mentioned non-United States countries in the New York Times article abstracts are:", most_frequent_country_for_flickr))
	return most_frequent_country_for_flickr

def get_flickr_data(tag_search, num_photos=100):
    baseurl = "https://api.flickr.com/services/rest/"
    params_d = {}
    params_d['tags'] = tag_search
    params_d['per_page'] = num_photos
    params_d['api_key'] = FLICKR_KEY
    params_d['method'] = "flickr.photos.search"
    params_d['has_geo'] = True
    params_d['tag_mode'] = "all"
    params_d['format'] = "json"
    unique_identifier = params_unique_combination(baseurl, params_d)
    if unique_identifier in CACHE_DICTION:
        print('Getting cached Flickr data...')
        return CACHE_DICTION[unique_identifier]
    else:
        print('Making request for new Flickr data...')
        flickr_resp = requests.get(baseurl, params=params_d)
        flickr_text = flickr_resp.text
        if flickr_text == 'jsonFlickrApi({"stat":"fail","code":100,"message":"Invalid API Key (Key has invalid format)"})':
        	print("\nSorry, it appears the way you input your New York Times Article Search API key may be incorrect. Please try pasting it in again.\n")
        flickr_text_adjusted = flickr_text[14:-1]
        flickr_resp_python = json.loads(flickr_text_adjusted)
        CACHE_DICTION[unique_identifier] = flickr_resp_python
        entire_diction_json_string_to_cache = json.dumps(CACHE_DICTION)
        fwrite = open(CACHE_FNAME,'w')
        fwrite.write(entire_diction_json_string_to_cache)
        fwrite.close()
        return CACHE_DICTION[unique_identifier]

print("\nThe program will now find the most frequently mentioned country(ies) in the returned New York Times articles' abstracts, and will make a request to Flickr for the first 100 photos taged with the keywords 'dance' AND 'most_frequent_country'.\n")
photo_ids = []
for each in get_photo_keywords(article_instances):
	flickr_dance_request = get_flickr_data(tag_search = '{},{}'.format("dance", each["country_name"]))
	for diction in flickr_dance_request["photos"]["photo"]:
		photo_ids.append(diction["id"])

def get_flickr_photos_data(lst_ids):
    baseurl = "https://api.flickr.com/services/rest/"
    params_d = {}
    params_d['photo_id'] = each_id
    params_d['api_key'] = FLICKR_KEY
    params_d['method'] = "flickr.photos.getInfo"
    params_d['format'] = "json"
    unique_identifier = params_unique_combination(baseurl, params_d)
    if unique_identifier in CACHE_DICTION:
        print('Getting cached Flickr photo data...')
        return CACHE_DICTION[unique_identifier]
    else:
	    print('Making request for new Flickr photo data...')
	    flickr_resp = requests.get(baseurl, params=params_d)
	    flickr_text = flickr_resp.text
	    flickr_text_adjusted = flickr_text[14:-1]
	    flickr_resp_python = json.loads(flickr_text_adjusted)
	    CACHE_DICTION[unique_identifier] = flickr_resp_python
	    entire_diction_json_string_to_cache = json.dumps(CACHE_DICTION)
	    fwrite = open(CACHE_FNAME,'w')
	    fwrite.write(entire_diction_json_string_to_cache)
	    fwrite.close()
	    return CACHE_DICTION[unique_identifier]

class Photo(object):
    def __init__(self, photo_dict):
    	self.title = photo_dict["photo"]["title"]["_content"]
    	self.date_taken = photo_dict["photo"]["dates"]["taken"]
    	if "country" in photo_dict["photo"]["location"]:
    		self.country = photo_dict["photo"]["location"]["country"]["_content"]
    	else:
    		self.country = ""
    	self.latitude = photo_dict["photo"]["location"]["latitude"]
    	self.longitude = photo_dict["photo"]["location"]["longitude"]
    	for each in photo_dict["photo"]["urls"]["url"]:
    		self.url = each["_content"]

    def photo_geo_info(self):
    	return self.country, self.latitude, self.longitude

    def __str__(self):
        return "{}\n{}\n{}\n{}\n".format(self.title, self.date_taken, self.url, self.photo_geo_info())

for each_id in photo_ids:
	flickr_photos_request = get_flickr_photos_data(each_id)

photo_instances = []
for k,v in CACHE_DICTION.items():
	for each in photo_ids:
		if each in k:
			photo_instances.append(Photo(v))

print('\n{}\n{}\n'.format("Here's an example of what your request for photos returned:", photo_instances[0]))

print("\nThe program will now generate a .csv file with the returned Filckr photos' information.\n")
photo_csv = open("flickr_photo_analysis.csv", 'w', newline='')
photo_writer = csv.writer(photo_csv)
photo_writer.writerow(['photo_title','date_taken', 'country', 'latitude', 'longitude', 'photo_url'])
for photo in photo_instances:
	photo_writer.writerow([photo.title, photo.date_taken, photo.country, photo.latitude, photo.longitude, photo.url])
photo_csv.close()


######################################################-----CARTODB-----###############################################################
	
CARTO_USR_BASE_URL = "https://{user}.carto.com/".format(user=CARTO_USERNAME)

auth_client = APIKeyAuthClient(api_key=CARTO_KEY, base_url=CARTO_USR_BASE_URL)

LOCAL_FILEreader = csv.reader(open("flickr_photo_analysis.csv"), delimiter=",")

line_list = []
for line in LOCAL_FILEreader:
	line_list.append(line)

# If you have not yet uploaded a dataset to CartoDB...
# 	1. Upload your dataset to CartoDB using the block of code called "New Map".
# 	2. Publish a map based on this uploaded dataset directly in the CartoDB user interface. 
# 	3. Copy your newly published map URL into the appropriate "webbrowser" module invocation below. 
# 	4. Once the three steps above are complete, comment out the "New Map" code block.
# If you have already uploaded a dataset to CartoDB and created a map...
# 	1. Update the New York Times and Flickr data supporting your map by uncommenting and  using the the "Map Update" 
# 		code block.

## This block of code is called "New Map".
dataset_manager = DatasetManager(auth_client)
dataset = dataset_manager.create(LOCAL_FILEreader)


## This block of code is called "Map Update".
# def carto_update(lst_csv_lines):
# 	print("The program and will now update CartoDB's mapping interface with the information contained in the Flickr photo .csv. Please note that if the list of countries most frequently mentioned in the New York Times article abstracts exceeds 4 items, the program will only post information about the first 4 to CartoDB's mapping interface.\n")
# 	LIST_OF_SQL_QUERIES1 = ['delete from flickr_photo_analysis']
# 	LIST_OF_SQL_QUERIES2 = []
# 	LIST_OF_SQL_QUERIES3 = []
# 	LIST_OF_SQL_QUERIES4 = []
# 	LIST_OF_SQL_QUERIES5 = []
# 	LIST_OF_SQL_QUERIES6 = []
# 	LIST_OF_SQL_QUERIES7 = []
# 	for line in line_list[1:50]:
# 		LIST_OF_SQL_QUERIES1.append("{}{}'{}','{}','{}',{},{},'{}'{}".format('insert into flickr_photo_analysis(photo_title, date_taken, country, latitude, longitude, photo_url)',' values(', line[0], line[1], line[2], line[3], line[4], line[5], ')'))
# 	for line in line_list[50:100]:
# 		LIST_OF_SQL_QUERIES2.append("{}{}'{}','{}','{}',{},{},'{}'{}".format('insert into flickr_photo_analysis(photo_title, date_taken, country, latitude, longitude, photo_url)',' values(', line[0], line[1], line[2], line[3], line[4], line[5], ')'))
# 	for line in line_list[100:150]:
# 	 	LIST_OF_SQL_QUERIES3.append("{}{}'{}','{}','{}',{},{},'{}'{}".format('insert into flickr_photo_analysis(photo_title, date_taken, country, latitude, longitude, photo_url)',' values(', line[0], line[1], line[2], line[3], line[4], line[5], ')'))
# 	for line in line_list[150:200]:
# 	 	LIST_OF_SQL_QUERIES4.append("{}{}'{}','{}','{}',{},{},'{}'{}".format('insert into flickr_photo_analysis(photo_title, date_taken, country, latitude, longitude, photo_url)',' values(', line[0], line[1], line[2], line[3], line[4], line[5], ')'))
# 	for line in line_list[200:250]:
# 	 	LIST_OF_SQL_QUERIES5.append("{}{}'{}','{}','{}',{},{},'{}'{}".format('insert into flickr_photo_analysis(photo_title, date_taken, country, latitude, longitude, photo_url)',' values(', line[0], line[1], line[2], line[3], line[4], line[5], ')'))
# 	for line in line_list[250:300]:
# 	 	LIST_OF_SQL_QUERIES6.append("{}{}'{}','{}','{}',{},{},'{}'{}".format('insert into flickr_photo_analysis(photo_title, date_taken, country, latitude, longitude, photo_url)',' values(', line[0], line[1], line[2], line[3], line[4], line[5], ')'))
# 	for line in line_list[350:400]:
# 	 	LIST_OF_SQL_QUERIES7.append("{}{}'{}','{}','{}',{},{},'{}'{}".format('insert into flickr_photo_analysis(photo_title, date_taken, country, latitude, longitude, photo_url)',' values(', line[0], line[1], line[2], line[3], line[4], line[5], ')'))
# 	sql_instance = BatchSQLClient(auth_client)
# 	createJob1 = sql_instance.create(LIST_OF_SQL_QUERIES1)
# 	createJob2 = sql_instance.create(LIST_OF_SQL_QUERIES2)
# 	createJob3 = sql_instance.create(LIST_OF_SQL_QUERIES3)
# 	createJob4 = sql_instance.create(LIST_OF_SQL_QUERIES4)
# 	createJob5 = sql_instance.create(LIST_OF_SQL_QUERIES5)
# 	createJob6 = sql_instance.create(LIST_OF_SQL_QUERIES6)
# 	createJob7 = sql_instance.create(LIST_OF_SQL_QUERIES7)
# 	createJob8 = sql_instance.create(['update flickr_photo_analysis set the_geom = CDB_LatLng(latitude, longitude)'])

# carto_update(line_list)

# print("\nPlease wait for 30 seconds while your map is updated with your new photo data. When the map loads, if you do not immediately see your datapoints represented, please continue refreshing the page. In the event that multiple photos have the same geo-tag, you will only see one point representing this cluster. This is an issue the programmer is aware of and is working on! Thank you for your patience.\n")
# time.sleep(30)

## Enter your CartoDB published map URL here. This will allow the program to open your updated map in your web browser.
# webbrowser.open('ENTER URL HERE')
















