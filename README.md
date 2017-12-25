# global-dance-culture

README: DANCEMAP

This file includes program information described by the following section headings: 
(1) ABOUT
(2) FILES REQUIRED
(3) PYTHON MODULES REQUIRED 
(4) HOW TO RUN THE PROGRAM
(5) REFERENCES AND RESOURCES
(6) PROGRAM OUTPUT

###############h

(1) ABOUT

On running the program, if you provide your New York Times, Flickr, and CartoDB information as instructed via the program prompt, the project will:

1. Find the most frequently mentioned non-United States country name in the first 100 articles returned from a NYT search for articles containing the keyword, “dance”;
2. Find the first 100 photos on Flickr returned from a Flickr search for photos tagged with the keywords “dance” and the most frequently mentioned non-United States country name from the NYT articles;
3. Generates a CSV file of information describing these photos;
4. Creates and / or updates and opens a map in your web browser with points representing each of these photos according to the photos’ geo-tagged coordinates.

The resulting map will allow you to see what people are “saying” (in photos) about dance and the non-United States country the New York Times has most frequently and recently published about.

###############

(2) FILES REQUIRED AND INCLUDED IN THIS SUBMISSION

Required files include:
dancemap.py
secret_data.py
countries.json

Please ensure that each of these resides in the same directory in order for the program to run.

###############

(3) PYTHON MODULES REQUIRED

json
requests
webbrowser
csv
GeoText
carto
time

###############

(4) HOW TO RUN THE PROGRAM

In order to run the code, please navigate to the directory that contains each of the necessary files outlined in section 2. Once in the appropriate directory, execute the following command in Terminal:

 python3 dancemap.py

On executing the above command, you will be prompted to enter your API keys for each of New York Times Article Search API, Flickr API, and CartoDB API. Please do so. This will automatically update the file ‘secret_data.py’ that the program requires to run.

Following entry of the requested API keys, the program will inform you in Terminal which tasks it is executing as it runs. 

The program will produce a CSV file in your working directory with information about the photos returned by the program. Once you have created a map as instructed in the comments in the program, it will also update and open a map in your web browser populated with the photo data returned by the program.

###############

(5) REFERENCES AND RESOURCES

‘geotext-python’ module documentation: https://pypi.python.org/pypi/geotext

New York Times Article Search API documentation: https://developer.nytimes.com/

Flickr API documentation:https://www.flickr.com/services/api/

CartoDB API and ‘carto’ module documentation:
https://carto.com/docs/
http://carto-python.readthedocs.io/en/latest/import_api.html
https://github.com/CartoDB/carto-python

‘countries.json’ file accessed via:
‘yshahak’’s comment on August 18th, 2017 at 8:42am, “Here, I used online converter, you can get my file: drive.google.com/file/d/0B52RjTfri3LPNDFuc0JHRDkxNE0/…". 
This comment references the online CSV file available at: https://developers.google.com/public-data/docs/canonical/countries_csv 
This comment is available at: https://stackoverflow.com/questions/2702309/need-a-list-of-all-countries-in-the-world-with-a-longitude-and-latitude-coordin

###############

(6) PROGRAM OUTPUT

This program generates a CSV file called ‘flickr_photo_analysis.csv’ of the photos returned from a search for ‘dance’ AND ‘most_frequent_country_for_flickr’ (this variable represents a list of country names). This CSV file will have 6 columns with the headers ‘photo_title', 'date_taken',  'country',  ‘latitude', 'longitude', and ‘photo_url’. The CSV file will have 100 rows per country keyword searched. If only one country is found to be most frequently mentioned, for example, the CSV file will have 100 rows. If four countries are tied for most frequently mentioned, for example, the CSV file will have 400 rows.

The program also updates a CartoDB map with points representing each of the photos described in the CSV file according to the photos’ geospatial coordinates. The program will only update the map with a maximum of 400 points (i.e. 400 photos). This map will open automatically in your web browser on the program’s completion. You may need to refresh the map a few times, as the map may take time populate with your new data.
