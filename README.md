# PythonProject
Twitter Scraper

===  python libraries required ===
pandas,streamlit,datetime,time,pymongo,snscrape,image,json 
These libraries are used in this project and install with latest version available 

=== Description ===

This is simple python project where a user can scrape the based on his wish to select keyword or hashtag or username, one can able to see the data in the form of dataframe when he click on the button,One can upload those scraped tweets into database and download them as csv and json format files

=== Development ===

streamlit :-
->Using streamlit sidebar selection box navigator created pages and where user can provide the type of scraper, based on the input it will display accordingly where user can provide some more data to scrape the tweets
->after collecting information user will click on the retrieve button to scrape the data and to display it in the form of table
->other buttons created to upload the data into mongodb by calling respective function and download the data by st.download_button

pandas :-
-> retrieve_and_display function invoked when you called or clicked on the retrieve button and takes query(user information concatenated to string) and limt(no of tweets to be scraped) and return the dataframe to the main function. Here we are converting the list of tweets into dataframe

snscrape :-
->from snscrape we use TwitterSearchScraper method and take the query as argument and scrape the tweets accordingly, here we stored those tweets in the list, vars function is used to get the keynames for the dataframe columns

pymongo :-
->upload_into_database function called when user click on the upload to database button, it will create connection to the mongodb compas server and create database and collection where user can push the record(data scraped) to the server using insert_one query
