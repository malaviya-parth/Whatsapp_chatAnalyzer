# -*- coding: utf-8 -*-
"""
Created on Thu May 18 18:59:34 2023

@author: malav
"""
import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[apm]{2}\s-\s'
    messages = re.split(pattern, data) [1:] #.split returns an array with first argument being the term which split the string and second being the data to be splitted
    dates = re.findall(pattern, data)
    dates = [date.replace("\u202f", " ") for date in dates]
    df = pd.DataFrame({'user-message': messages, 'message-date': dates})
    df['message-date'] = pd.to_datetime(df['message-date'], format='%d/%m/%y, %I:%M %p - ')
    
    df.rename(columns={'message-date': 'date'},inplace=True)

    users = []
    messages = []
    for message in df['user-message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('gorup_notification')
            messages.append(entry[0])
    
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user-message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
