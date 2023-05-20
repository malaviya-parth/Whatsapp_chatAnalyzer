import re
from urlextract import URLExtract
import wordcloud #wordcloud
import pandas as pd #data manipulation
from collections import Counter #counter
import emoji #emoji

def fetch_stats(selected_user,df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    total_messages = df.shape[0]

    words = []
    for message in df['message']:
        words.extend(message.split())
    
    # total_media = df[df['message'] == "<Media omitted>\n"].shape[0]
    total_media = [msg for msg in df['message'] if not msg.startswith('<Media omitted>')].__len__()

    # links = df[df['message'].str.contains("http")].shape[0]

    links = []
    for message in df['message']:
        links.extend(re.findall("(?P<url>https?://[^\s]+)", message))


    # links = []
    # for message in df['message']:
    #     extractor = URLExtract()
    #     links.extend(extractor.find_urls(message))

    
    return total_messages, words, total_media, links

def most_busy_users(df):
    x = df['user'].value_counts().head(10)
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index()
    return x, df

def plot_wordcloud(selected_user,df): 
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    df_wc = wordcloud.WordCloud(width=500, height=500,min_font_size=10,background_color='white').generate(df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('stopwords_hinglish.txt', "r") # read stopwords
    stop_words = f.read() # convert to list

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    temp = df[df['user'] != "group_notification"] # remove group notifications
    temp = [msg for msg in temp['message'] if not msg.startswith('<Media omitted>')] # remove media
    temp = [msg for msg in temp if not msg.startswith('http')] # remove links
    temp = pd.DataFrame(temp, columns=['message']) # convert to dataframe

    words = []

    for msg in temp['message']:
        for word in msg.lower().split(): # convert to lowercase
            if word not in stop_words: 
                words.append(word) 

    most_common_df =pd.DataFrame(Counter(words).most_common(20), columns=['word','count'])

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        # ([c for c in message if c in emoji.emoji_list(message)])
        # emojis.append(emoji.emoji_list(message))
        if (emoji.emoji_list(message)):
            for ans in emoji.emoji_list(message):
                emojis.append(ans)
       
    # print(len(emojis))
    # print(emojis[0]["emoji"])
    emoji_count = []
    for e in emojis:
        emoji_count.extend(emojis[0]["emoji"])

    # emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df = pd.DataFrame(Counter(emoji_count).most_common(len(Counter(emoji_count))), columns=['emoji','count'])

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index() 

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    
    timeline['time'] = time
    
    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatMap(selected_user,df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap