import re
import pandas as pd

def preprocess(data):
    pattern = '(?<=- ).*'
    messages = re.findall(pattern, data)

    date = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w\w'
    dates = re.findall(date, data)

    x = len(dates)
    y = len(messages)
    del messages[x:y]

    # create DataFrame
    df = pd.DataFrame({'user_message': messages, 'messages_date': dates})
    # convert message_date type
    df['messages_date'] = pd.to_datetime(df['messages_date'], format='%m/%d/%y, %I:%M %p')
    df.rename(columns={'messages_date': 'date'}, inplace=True)



    # Now, split user_name from user_message.[separate users and messages]
    users = []
    message = []
    for msg in df['user_message']:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:  # user_name
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append('group_notification')
            message.append(entry[0])
    df['user'] = users
    df['message'] = message
    df.drop(columns=['user_message'], inplace=True)

    # Create New Columns in Which has Splits in dd-mm-yy hh-mm-ss
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour < 9:
            period.append(str('0') + str(hour) + '-' + str('0') + str(hour + 1))
        elif hour == 9:
            period.append(str('0') + str(hour) + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period

    return df