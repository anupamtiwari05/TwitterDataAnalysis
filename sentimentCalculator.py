# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 20:45:47 2017

@author: Rachit & Nitesh
"""

class tweetsSenti:

    def __init__(self, **kwargs):
        return super().__init__(**kwargs)

    def searchTweets(self, q):
        import numpy as np
        import pandas as pd
        import re
        from twitter import Twitter, OAuth, TwitterHTTPError
        from pandas.io.json import json_normalize
        
        ACCESS_TOKEN = '136600388-9iihe7SFq8nZUOL5GjxoZlPbxW2MYcScWlZ6sD3a'
        ACCESS_SECRET = 'ScmAR4iYHCxuPHhYMifirTK0h2Jhdqt1p10uoz9lHTshT'
        consumer_key = 'bto0MsRvjjfkrl4QpndjaUneg'
        consumer_secret = '5zr7Xr9y4AbKgUCuWRmQGaMvizwg48HpVeyjbSZC4j350rIYPF'
    
        oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, consumer_key, consumer_secret)
        twitterObj = Twitter(auth=oauth)
        #q = 'modi'
        count = 100
        try:
            search_results = twitterObj.search.tweets(q=q,count = count)
        except TwitterHTTPError:
            return 'twitter server error'
        Original_status_df = json_normalize(search_results,['statuses'])
        Original_status_df = pd.DataFrame(Original_status_df)
        min_id = min(Original_status_df['id'])
        max_id = max(Original_status_df['id'])

        while len(Original_status_df) < 300:
            try:
                search_results = twitterObj.search.tweets(q=q,count=count,max_id = min_id)
                results = json_normalize(search_results,['statuses'])
                Original_status_df = Original_status_df.append(results)
                min_id = min(results['id'])
                max_id = max(results['id'])
            except TwitterHTTPError:
                return 'twitter server error'
        

        Original_status_df = Original_status_df.reset_index()
        cleansed_tweets_df = clean_Tweets(Original_status_df)
        countries = ['Argentina','Austria','Australia','Brasil','Brazil','Bangladesh','Cameroon','Canada','Cyprus',
                    'Deutschland','Dubai','Ecuador','Egypt',
                    'England','Kenya','Nigeria','Hong Kong','Holand','Finland','Prague','USA','Greece',
                    'Kazakhstan','Thailand','Italy','Italia','India','Israel','Ireland','Pakistan','Polska','Poland',
                    'United States','Germany','Spain','France','Fiji','China','Mexico','Netherlands',
                    'New Zealand','North Korea','Japan','Jordan',
                    'Oman','Palestine','United Arab Emirates','UAE','Portugal','Scotland','Slovakia',
                    'South Africa','Switzerland','Sweden',
                    'Turkey','Peru','Puerto Rico','Russia','Singapore','Chile','United Kingdom','Indonesia','Philippines',
                    'Ukraine','UK','Venezuela','Yemen']

        Cleansed_Country_df = Country_of_tweet(cleansed_tweets_df,countries)

        us_city_state_filter =['Albuquerque','Asheville','Atlanta','Austin','Baltimore','Boston','Columbia','Dallas','Detroit','Denver',
                       'Las Vegas','Georgia','Miami','Honolulu','Los Angeles','Pensacola','Richmond','Kansas',
                       'Pheonix City','Washington, DC','NYC',
                       'San Jose','Seattle','Orlando','Pittsburgh','San Diego','Chicago',    
                       'New York','Phoenix','Mount Prospect',
                       'Alabama','Alaska','Arkansas','Arizona',
                       'California','Colorado','Connecticut','Delaware','Florida','Hawaii','Indiana','Iowa','Idaho','Illinois',
                       'Indiana','Louisiana','Oregon',       
                       'Maryland','Michigan','Minnesota','Maine','Massachusetts','Missouri','Mississippi','Montana',
                       'Nebraska','New Jersey','New Hampshire','North Carolina','Kentucky','Ohio','Oklahoma',
                       'New Mexico','Nevada','North Dakota','South Dakota','Pennsylvania','San Francisco',
                       'Tennessee','Utah','Rhode Island','South Carolina','Washington','West Virginia','Wisconsin','Wyoming',
                       'Texas','Vermont','Virginia','LA','SF',
                       'AZ','AL','CA','CO','CT','DE','FL','GA','IA','ID','IL','IN','KY','MA',
                       'MI','MO','MD','MT','MN','MS','NC','ND','NJ','NH','NY','NV',
                       'OH','OR','PA','RI','SD','TX','TN','UT','VA','VT','WA','WI','WY','WV']
        
        US_States_df = US_State_of_User(Cleansed_Country_df,us_city_state_filter)
        Updated_country_df = Updated_country_of_tweet(US_States_df,'USA')

        only_country_df =   Updated_country_df[Updated_country_df['Country_User']!=''].reset_index(drop=True)
        tweet_df_live_sentiments_df = calculate_sentiment(only_country_df)

        country_tweets_count  = countryTweetsCount(tweet_df_live_sentiments_df)
        usa_tweets_count    = usaTweetsCount(country_tweets_count)

        mean_sentiments_country_df = meanSentimentsCountry(usa_tweets_count)
        mean_sentiments_UsState_df = meanSentimentsUsState(mean_sentiments_country_df)

        world_map_df  = mean_sentiments_UsState_df[['Country_User','Mean_Polarity_Country','Weighted_Mean_Polarity_Country','Total_Tweets_Country']]
        world_map =  world_map_df.groupby('Country_User').mean()
  
        UsState_map_df  = mean_sentiments_UsState_df[['USA_State_User','Mean_Polarity_USA_State','Weighted_Mean_Polarity_USA_State','Total_Tweets_USA_State']]
        UsState_map =  UsState_map_df.groupby('USA_State_User').mean()
       
        world_map_string = worldMap(world_map['Weighted_Mean_Polarity_Country'], world_map.index)
        return 'Success'

def clean_Tweets(Original_status_df):
    import re
    status_row = []
    location=[]
    tweet_df = Original_status_df[['user','text']]
    for i in range(len(tweet_df)):
        status_ = tweet_df.iloc[i,:]['text'].lower()
        status_ = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',status_)
        status_ = re.sub('@[^\s]+','',status_)
        status_ = re.sub('[^A-Za-z0-9 ]+', '', status_)
        status_ = status_.replace('rt','')
        status_row.append(status_)
        
        try:
            location_ = tweet_df.iloc[i,:]['user']['location']
            location.append(location_)
        except IndexError:
            location.append("")

    tweet_df['text'] = status_row
    tweet_df['Location_User'] = location
   
    return tweet_df


def Country_of_tweet(dataframe,countries_filter):
    import re
    list3 =[]
    country_names_updated = {'Prague' : 'Czechia','United States':'USA','United Arab Emirates':'UAE',
                             'Deutschland':'Germany','UK':'United Kingdom','Italia':'Italy','Polska':'Poland',
                             'Holand':'Netherlands','Brasil':'Brazil'}
    for i in range(len(dataframe)):
        setblank =0
        location = dataframe.iloc[i,:]['Location_User']
        if(isinstance(location,str)):
            location_split = re.split(r'[-,.\s]',location)
            for country in countries_filter:
                if('United Arab Emirates' in country or 'United States' in country or 'United Kingdom' in country 
                   or 'New Zealand' in country or 'North Korea' in country):
                    if(re.search(country,location) or re.search(country.lower(),location.lower()) or re.search(country.upper(),location.upper())):
                        country_updated = country_names_updated.get(country,country)
                        list3.append(country_updated) 
                        setblank = 1
                        break 
                elif(country in location_split or country.lower() in location_split or country.upper() in location_split):
                    country_updated = country_names_updated.get(country,country)
                    list3.append(country_updated)
                    setblank = 1
                    break
            if(setblank == 0):
                list3.append("")
        else:
            list3.append("")
        
    dataframe['Country_User'] = list3
    return dataframe


def US_State_of_User(dataframe,us_city_state):
    import re
    dummylist =[]
    count = 0
    city_to_state_names_updated = {'Albuquerque':'New Mexico',
                                   'Atlanta':'Georgia',
                                   'Austin':'Texas',
                                   'Baltimore':'Maryland',
                                   'Boston':'Massachusetts',
                                   'Columbia':'South Carolina',
                                   'Diego':'California',
                                   'Denver':'Colorado',
                                   'Detroit':'Michigan',
                                   'Honolulu':'Hawaii',
                                   'Las Vegas' : 'Nevada',
                                   'Vegas':'Nevada',
                                   'Indianapolis':'Indiana',
                                   'Dallas': 'Texas',
                                   'Seattle': 'Washington',
                                   'NYC':'New York',
                                   'Los Angeles' : 'California',
                                   'Orlando': 'Florida',
                                   'San Diego' : 'California',
                                   'San Jose':'California',
                                   'San Francisco':'California',
                                   'LA':'California',
                                   'SF':'California',
                                   'Pittsburgh':'Pennsylvania',
                                   'Pensacola':'Florida',
                                   'Chicago':'Illinois','Phoenix':'Arizona','Pheonix City':'Albama','Richmond':'Virginia',
                                   'Mount Prospect':'Illinois','Washington  DC':'Maryland','washington, DC':'Maryland',                             
                                   'Miami':'Florida', 'Asheville':'North Carolina','Washington DC':'Maryland',
                                   'AZ':'Arizona','AL':'Alabama','CA':'California','CT':'Connecticut','CO':'Colorado',
                                   'DE':'Delaware','FL':'Florida','GA':'Georgia','ID':'Idaho','IA':'Iowa','IL':'Illinois',
                                   'IN':'Indiana','KY':'Kentucky','MA':'Massachusetts','MD':'Maryland','MI':'Michigan',
                                   'MN':'Minnesota','MS':'Mississippi','MT':'Montana','MO':'Missouri','NC':'North Carolina',
                                   'ND':'North Dakota','NE':'Nebraska','NH':'New Hampshire','NY':'New York',
                                   'NJ':'New Jersey','NV':'Nevada','OH':'Ohio','OR':'Oregon','PA':'Pennsylvania',
                                   'RI':'Rhode Island','TX':'Texas','TN':'Tennessee','SD':'South Dakota','UT':'Utah',
                                   'VA':'Virginia','VT':'Vermont','WA':'Washington','WI':'Wisconsin','WY':'Wyoming',
                                   'WV':'West Virginia'}
    
    for i in range(len(dataframe)):
        setblank =0
        location_string =  dataframe.iloc[i,:]['Location_User']
        if(isinstance(location_string,str)):
            location_string_split= re.split(r'[,\s]', location_string)
            for city_state in us_city_state:
                if('New York' in city_state or 'Las Vegas' in city_state or 'Los Angeles' in city_state 
                   or 'North Carolina' in city_state or 'San Francisco' in city_state or 'New Mexico' in city_state 
                   or 'North Dakota' in city_state or 'South Dakota' in city_state or 'Rhode Island' in city_state 
                   or 'Washington, DC' in city_state or 'New Jersey' in city_state or 'Washington DC' in city_state
                   or 'Washington  DC' in city_state or 'New Hampshire' in city_state or 'West Virginia' in city_state):
                    if(re.search(city_state,location_string) or re.search(city_state.lower(),location_string.lower()) 
                       or re.search(city_state.upper(),location_string.upper())):
                        state_updated = city_to_state_names_updated.get(city_state,city_state)
                        dummylist.append(state_updated) 
                        setblank = 1
                        break
                elif(city_state in location_string_split or city_state.lower() in location_string_split or city_state.upper() in location_string_split):
                    state_updated = city_to_state_names_updated.get(city_state,city_state)
                    dummylist.append(state_updated) 
                    setblank = 1
                    break
                    
            if(setblank == 0):
                dummylist.append('')
        else:
            list3.append('')
        
    dataframe['USA_State_User'] = dummylist
    
    return dataframe

def Updated_country_of_tweet(dataframe,country):
    countrylist = []
    for i in range(len(dataframe)):
        if(dataframe.iloc[i,:]['USA_State_User']!=""):
            countrylist.append(country)
        else:
            countrylist.append(dataframe.iloc[i,:]['Country_User'])
                          
    dataframe['Country_User'] = countrylist
    return  dataframe 

def calculate_sentiment(tweet_df):
    from textblob import TextBlob
    polarity = []
    subjectivity = []
    reputation = []
    for i in range(len(tweet_df)):
        wiki = TextBlob(tweet_df.iloc[i,:]['text'])
        polarity.append(wiki.sentiment.polarity)
        subjectivity.append(wiki.sentiment.subjectivity)
        try:
            reputation.append(int(tweet_df.iloc[i,:]['user']['followers_count'])/(int(tweet_df.iloc[i,:]['user']['followers_count'])
            + int(tweet_df.iloc[i,:]['user']['friends_count'])))
        except ValueError:
            reputation.append(0)
        except ZeroDivisionError:
            reputation.append(0)
    tweet_df['Polarity'] = polarity
    tweet_df['Subjectivity']= subjectivity
    tweet_df['Reputation'] = reputation
    tweet_df['Reputation'] = round(tweet_df['Reputation'],1)
    return tweet_df

def countryTweetsCount(dataframe):
    dataframe['Total_Tweets_Country']=int()
    for country in dataframe.Country_User.unique():
        if(country == ''):
            dataframe.loc[dataframe.Country_User==country,'Total_Tweets_Country']= np.nan
        else:
            dataframe.loc[dataframe.Country_User==country,'Total_Tweets_Country'] = (dataframe[dataframe.Country_User==country].count().values[3])

    return dataframe

def usaTweetsCount(dataframe):
    import numpy as np
    dataframe['Total_Tweets_USA_State']=int()
    for state in dataframe.USA_State_User.unique():
        if(state == ''):
            dataframe.loc[dataframe.USA_State_User==state,'Total_Tweets_USA_State']= np.nan
        else:
            dataframe.loc[dataframe.USA_State_User==state,'Total_Tweets_USA_State'] = (dataframe[dataframe.USA_State_User==state].count().values[4])

    return dataframe

def meanSentimentsCountry(dataframe):
    dataframe['Mean_Polarity_Country']=float()
    dataframe['Mean_Subjectivity_Country']=float()
    dataframe['Mean_Reputation_Country']=float()
    dataframe['Weighted_Mean_Polarity_Country']=float()

    for country in dataframe.Country_User.unique():
        if(country == ''):
            dataframe.loc[dataframe.Country_User==country,'Mean_Polarity_Country'] = ''
            dataframe.loc[dataframe.Country_User==country,'Mean_Subjectivity_Country'] = ''
            dataframe.loc[dataframe.Country_User==country,'Mean_Reputation_Country'] = ''
        else:
            dataframe.loc[dataframe.Country_User==country,'Mean_Polarity_Country'] =100 * dataframe[dataframe.Country_User==country].Polarity.mean()
            dataframe.loc[dataframe.Country_User==country,'Weighted_Mean_Polarity_Country'] =(1000000 * dataframe[dataframe.Country_User==country].Polarity.mean() * dataframe[dataframe.Country_User==country].Total_Tweets_Country.mean())/dataframe['Total_Tweets_Country'].sum()     
            dataframe.loc[dataframe.Country_User==country,'Mean_Subjectivity_Country'] =100 * dataframe[dataframe.Country_User==country].Subjectivity.mean()
            dataframe.loc[dataframe.Country_User==country,'Mean_Reputation_Country'] =100 * dataframe[dataframe.Country_User==country].Reputation.mean()

    return dataframe

def meanSentimentsUsState(dataframe):
    dataframe['Mean_Polarity_USA_State']=float()
    dataframe['Mean_Subjectivity_USA_State']=float()
    dataframe['Mean_Reputation_USA_State']=float()
    dataframe['Weighted_Mean_Polarity_USA_State']=float()

    for us_state in dataframe.USA_State_User.unique():
        if(us_state == ''):
            dataframe.loc[dataframe.USA_State_User==us_state,'Mean_Polarity_USA_State'] = ''
            dataframe.loc[dataframe.USA_State_User==us_state,'Mean_Subjectivity_USA_State'] = ''
            dataframe.loc[dataframe.USA_State_User==us_state,'Mean_Reputation_USA_State'] = ''
        else:
            dataframe.loc[dataframe.USA_State_User==us_state,'Mean_Polarity_USA_State'] =100 * dataframe[dataframe.USA_State_User==us_state].Polarity.mean()
            dataframe.loc[dataframe.USA_State_User==us_state,'Weighted_Mean_Polarity_USA_State'] =(1000000 * dataframe[dataframe.USA_State_User==us_state].Polarity.mean() * dataframe[dataframe.USA_State_User==us_state].Total_Tweets_USA_State.mean())/dataframe['Total_Tweets_USA_State'].sum() 
            dataframe.loc[dataframe.USA_State_User==us_state,'Mean_Subjectivity_USA_State'] =100 * dataframe[dataframe.USA_State_User==us_state].Subjectivity.mean()
            dataframe.loc[dataframe.USA_State_User==us_state,'Mean_Reputation_USA_State'] =100 * dataframe[dataframe.USA_State_User==us_state].Reputation.mean()

    return dataframe

def worldMap(polarity,country_code):
     #from plotly import plotly
     from json import json
#==============================================================================
#     scl = [[0.0, 'rgb(242,240,247)'],[0.2, 'rgb(218,218,235)'],[0.4, 'rgb(188,189,220)'],\
#             [0.6, 'rgb(158,154,200)'],[0.8, 'rgb(117,107,177)'],[1.0, 'rgb(84,39,143)']]
#==============================================================================
    graphs = [dict(data = [dict(
                        type = 'choropleth',
                        locations = country_code,
                        z = polarity,
                        text = country_code,
                        colorscale = [[-1,"rgb(5, 10, 172)"],[-0.5,"rgb(40, 60, 190)"],[0.0,"rgb(70, 100, 245)"],\
                            [0.3,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"]],
                        autocolorscale = False,
                        reversescale = True,
                        marker = dict(
                            line = dict (
                                color = 'rgb(180,180,180)',
                                width = 0.5
                            ) ),
                        colorbar = dict(
                            autotick = False,
                            title = 'Polarity'),
                      )
                    ],
            layout = dict(
            title = 'World Map Plot',
            geo = dict(
                showframe = False,
                showcoastlines = True,
                projection = dict(
                    type = 'Mercator'
                )
                )   
            )
        )
    ]
    world_map_id = ['World_Map']
    #data =json.dumps(world_map_id)
    #cls=plotly.plotly.utils.PlotlyJSONEncoder
    #world_map_json = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)
    #return cls, world_map_id
    return 'success'
