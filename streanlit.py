import pandas as pd
import streamlit as st
import snscrape.modules.twitter as sntwitter
import datetime as dt
import time
import pymongo
from PIL import Image
import json

# Main method contains whole navigation system, based on the user input it will redirect to specific

def main():



    # here user can select the type of scraper thet he want and we are storing the value in the radio variable

    radio = st.sidebar.selectbox("Select the Type of scraper", ["Select", "Username", "Hashtag", "Keyword"], index=0)

    # Based on the condition the data will be displayed accordingly

    if radio == "Username":
        query = 'from:'
        st.markdown("<h1 style='text-align: center; color: blue;'>Username Scraper</h1>", unsafe_allow_html=True)
        username = st.text_input("Username :-")

        # check weather the username contains the @ symbol or not

        if '@' in username:
            st.error("Write username without @")

        # dividing the row into two columns to take inputs from the user

        startDate, endDate = st.columns([2, 2])
        sdate = startDate.date_input("Enter the starting date:")
        edate = endDate.date_input("Enter the ending date:")

        # converting the date format to the format needed to the TwitterSearchScraper method

        sdate = str(sdate)
        edate = str(edate)
        sdate = sdate.replace("/", "-")
        edate = edate.replace("/", "-")
        limit = st.number_input("Limit :-", min_value=10, value=100, max_value=1000, step=10)

        # after taking all required inputs creating the string which is needed for the TwitterSearchScraper method

        query = query + username + ' since:' + sdate + ' until:' + edate

        # After clicking the button it will call the retrieve_and_display function and get the result and stored inside df and printing that result

        if st.button('Retrieve Tweets', type="primary", use_container_width=True):
            df = retrieve_and_display(query, limit)
            st.dataframe(df, width=700, height=300)

        # After clicking the button it will call the upload_into_mongo function and get the result as object and stored inside obj and based on that result we are printing the message

        if st.button('Upload to Database', type="secondary", use_container_width=True):
            obj = upload_into_mongo(query, limit,username)
            if obj:
                st.success("Uploaded Successfully")
            else:
                st.error("Error occurred while uploading")

        # retrieving the data from retrieve_and_display and converting into jason and csv files and providing them the buttons to download

        df = retrieve_and_display(query, limit)
        # for json
        twtjs = df.to_json(default_handler=str).encode('utf-8')
        # Create Python object from JSON string data
        obj = json.loads(twtjs)
        js = json.dumps(obj, indent=4)
        st.download_button(
            label="Download data as JSON",
            data=js,
            file_name='Scraped_data.json',
            mime='text/js',
            use_container_width=True
        )

        #for csv
        def convert_df(data):
            # Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Scraped_data.csv',
            mime='text/csv',
            use_container_width=True
        )


    elif radio == "Hashtag":
        query = '#'
        st.markdown("<h1 style='text-align: center; color: blue;'>Hashtag Scraper</h1>", unsafe_allow_html=True)
        Hashtag = st.text_input("Hashtag :-")

        # check weather the username contains the @ symbol or not

        if '#' in Hashtag:
            st.error("Write Hashtag without #")

        # dividing the row into two columns to take inputs from the user

        startDate, endDate = st.columns([2, 2])
        sdate = startDate.date_input("Enter the starting date:")
        edate = endDate.date_input("Enter the ending date:")

        # converting the date format to the format needed to the TwitterSearchScraper method

        sdate = str(sdate)
        edate = str(edate)
        sdate = sdate.replace("/", "-")
        edate = edate.replace("/", "-")
        limit = st.number_input("Limit :-", min_value=10, value=100, max_value=1000, step=10)

        # after taking all required inputs creating the string which is needed for the TwitterSearchScraper method

        query = query + Hashtag + ' since:' + sdate + ' until:' + edate

        # After clicking the button it will call the retrieve_and_display function and get the result and stored inside df and printing that result

        if st.button('Retrieve Tweets', type="primary", use_container_width=True):
            df = retrieve_and_display(query, limit)
            st.dataframe(df, width=700, height=300)

        # After clicking the button it will call the upload_into_mongo function and get the result as object and stored inside obj and based on that result we are printing the message

        if st.button('Upload to Database', type="secondary", use_container_width=True):
            obj = upload_into_mongo(query, limit,Hashtag)
            if obj:
                st.success("Uploaded Successfully")
            else:
                st.error("Error occurred while uploading")

        # retrieving the data from retrieve_and_display and converting into jason and csv files and providing them the buttons to download

        df = retrieve_and_display(query, limit)
        # for json
        twtjs = df.to_json(default_handler=str).encode('utf-8')
        # Create Python object from JSON string data
        obj = json.loads(twtjs)
        js = json.dumps(obj, indent=4)
        st.download_button(
            label="Download data as JSON",
            data=js,
            file_name='Scraped_data.json',
            mime='text/js',
            use_container_width=True
        )

        # for csv
        def convert_df(data):
            # Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Scraped_data.csv',
            mime='text/csv',
            use_container_width=True
        )

    elif radio == "Keyword":
        query = ''
        st.markdown("<h1 style='text-align: center; color: blue;'>Keyword Scraper</h1>", unsafe_allow_html=True)
        Keyword = st.text_input("Keyword :-")

        # dividing the row into two columns to take inputs from the user

        startDate, endDate = st.columns([2, 2])
        sdate = startDate.date_input("Enter the starting date:")
        edate = endDate.date_input("Enter the ending date:")

        # converting the date format to the format needed to the TwitterSearchScraper method

        sdate = str(sdate)
        edate = str(edate)
        sdate = sdate.replace("/", "-")
        edate = edate.replace("/", "-")
        limit = st.number_input("Limit :-", min_value=10, value=100, max_value=1000, step=10)

        # after taking all required inputs creating the string which is needed for the TwitterSearchScraper method

        query = query + Keyword + ' since:' + sdate + ' until:' + edate

        # After clicking the button it will call the retrieve_and_display function and get the result and stored inside df and printing that result

        if st.button('Retrieve Tweets', type="primary", use_container_width=True):
            df = retrieve_and_display(query, limit)
            st.dataframe(df,width=700,height=300)

        # After clicking the button it will call the upload_into_mongo function and get the result as object and stored inside obj and based on that result we are printing the message

        if st.button('Upload to Database', type="secondary", use_container_width=True):
            obj = upload_into_mongo(query, limit,Keyword)
            if obj:
                st.success("Uploaded Successfully")
            else:
                st.error("Error occurred while uploading")

        # retrieving the data from retrieve_and_display and converting into jason and csv files and providing them the buttons to download

        df = retrieve_and_display(query, limit)
        # for json
        twtjs = df.to_json(default_handler=str).encode('utf-8')
        # Create Python object from JSON string data
        obj = json.loads(twtjs)
        js = json.dumps(obj, indent=4)
        st.download_button(
            label="Download data as JSON",
            data=js,
            file_name='Scraped_data.json',
            mime='text/js',
            use_container_width=True
        )

        # for csv
        def convert_df(data):
            # Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Scraped_data.csv',
            mime='text/csv',
            use_container_width=True
        )
    else:
        image = Image.open('Twitter-scraping.jpg')
        st.image(image, width=700)
        st.markdown("<h1 style='text-align: center; color: blue;'>Welcome to Twitter Scraper</h1>",
                    unsafe_allow_html=True)

# retrieve_and_display function takes query and limit as the arguments and use TwitterSearchScraper method to scrape the tweets and getting those tweets into list and converting that into dataframe and return that dataframe

def retrieve_and_display(query,limit):
    query1 = query
    limit1 = limit
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query1).get_items():
        if len(tweets) == limit1:
            break
        else:
            tweets.append([tweet.date, tweet.id, tweet.url, tweet.user.username, tweet.rawContent, tweet.retweetCount,
                           tweet.replyCount, tweet.lang, tweet.source, tweet.likeCount])
    df = pd.DataFrame(tweets, columns=['Date', 'ID', 'Url', 'Username', 'Tweet_Content', 'RetweetCount', 'replyCount',
                                       'Language', 'source', 'likeCount'])
    return df

# upload_into_mongo takes query,limit and word as the argument return obj(created after inserting into the database)

def upload_into_mongo(query,limit,word):
    name = word
    query1 = query
    limit1 = limit
    df = retrieve_and_display(query1,limit1)

    # converting the dataframe to dictionary

    dict1 = df.to_dict(orient='list')

    #getting todays date

    tdate = dt.date.today()
    d1 = tdate.strftime("%d-%m-%Y")

    # creating the format in which we need to insert into database

    record = {"Scraped_Keyword": name, "Scraped_Date": d1, "Scraped_Data": dict1}

    # creating connection to database and creating the database and its collection to store above record

    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    Pscraper = client['PythonScraper']
    scraperinfo =Pscraper.Scraperinformation
    obj = scraperinfo.insert_one(record)
    return obj



if __name__ == '__main__':
   main()