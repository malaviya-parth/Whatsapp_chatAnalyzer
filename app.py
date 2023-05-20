# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:57:14 2023

@author: Parth
"""

import streamlit as st #web app
import pandas as pd #data manipulation
import preprocessor as p  #preprocessor.py
import re   #regular expression
import helper as h #helper.py
import matplotlib.pyplot as plt #plotting
import wordcloud
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    # Convert to UTF-8
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = p.preprocess(data)

    # st.dataframe(df)

    user_list = df.user.unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Show Analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4 = st.columns(4)

        total_messages, words, total_media, urls = h.fetch_stats(selected_user,df)
        
        col1.header("Total Messages")
        col1.success(total_messages)

        col2.header("Total Words")
        col2.success(len(words))

        col3.header("Total Media")
        col3.success(total_media)

        col4.header("Total Links")
        col4.success(len(urls))

        # Monthly_timeline
        timeline = h.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['message'])
        plt.xticks(rotation=90)
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = h.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
    
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = h.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = h.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values, color='orange')
            st.pyplot(fig)
        
        user_heatmap = h.activity_heatMap(selected_user, df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == "Overall":
            st.title("Most Busy Users")
            result, new_df = h.most_busy_users(df)
            fig, ax = plt.subplots()
            

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(result.index, result.values.flatten(), color='green')
                plt.xticks(rotation=90)
                plt.xlabel("Users")
                plt.ylabel("Number of Messages")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)
        else:
            pass    

        st.title("WordCloud")
        wc = h.plot_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(wc)
        # ax.axis("off")
        st.pyplot(fig)

        most_common_df = h.most_common_words(selected_user, df)
        st.title("Most Common Words")
        fig, ax = plt.subplots()
        ax.bar(most_common_df["word"], most_common_df["count"], color='green')
        plt.xticks(rotation=90)
        plt.xlabel("Words")
        plt.ylabel("Count")
        st.pyplot(fig)

        # emoji analysis
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        emoji_df = h.emoji_helper(selected_user,df)
        with col1:
            st.title("Tablular")
            st.dataframe(emoji_df)
        with col2:
            st.title("Graphical")
            fig, ax = plt.subplots()
            ax.pie(emoji_df["count"].head(), labels=emoji_df["emoji"].head(), autopct="%1.1f%%")
            plt.xlabel("Emoji")
            plt.ylabel("Count")
            st.pyplot(fig)
            






    # Split into lines
    # lines = data.split("\n")
    # # Convert to pandas dataframe
    # df = pd.DataFrame(lines)
    # # Split each line into columns
    # df = df[0].str.split(" - ", n=1, expand=True)
    # # Rename columns
    # df.columns = ["Date", "Message"]
    # # Convert date column to datetime
    # df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y, %I:%M %p")
    # # Drop missing values from messages
    # df = df.dropna()
    # # Drop if message is media message
    # df = df[df["Message"] != "<Media omitted>"]
    # # Extract hours and minutes
    # df["Hour"] = df["Date"].apply(lambda x: x.hour)
    # df["Minute"] = df["Date"].apply(lambda x: x.minute)
    # # Extract date
    # df["Date"] = df["Date"].apply(lambda x: x.date())
    # # Extract day of week
    # df["Day"] = df["Date"].apply(lambda x: x.day_name())
    # # Extract month
    # df["Month"] = df["Date"].apply(lambda x: x.month_name())
    # # Extract year
    # df["Year"] = df["Date"].apply(lambda x: x.year)
    # # Extract number of words
    # df["Word_Count"] = df["Message"].apply(lambda x: len(x.split()))
    # # Extract number of letters
    # df["Letter_Count"] = df["Message"].apply(lambda x: len(x))
    # # Extract number of links
    # df["Link_Count"] = df["Message"].apply(lambda x: x.count("http"))
    # # Extract number of emojis
    # df["Emoji_Count"] = df["Message"].apply(lambda x: sum([char in emoji.UNICODE_EMOJI for char in x]))
    # # Extract number of photos
    # df["Photo_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>"))
    # # Extract number of videos
    # df["Video_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "video omitted" in x else 0)
    # # Extract number of gifs
    # df["GIF_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "GIF omitted" in x else 0)
    # # Extract number of audio files
    # df["Audio_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "audio omitted" in x else 0)
    # # Extract number of documents
    # df["Document_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "document omitted" in x else 0)
    # # Extract number of contacts
    # df["Contact_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "contact card omitted" in x else 0)
    # # Extract number of locations
    # df["Location_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "location omitted" in x else 0)
    # # Extract number of stickers
    # df["Sticker_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "sticker omitted" in x else 0)
    # # Extract number of polls
    # df["Poll_Count"] = df["Message"].apply(lambda x: x.count("<Media omitted>") if "poll omitted" in x else 0)
