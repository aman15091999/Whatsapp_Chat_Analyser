import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatspp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue() # site pr jo file upload ho rhi hai vo byte data ka stream hai usko hame 'string' mai convert krna pdega.

     # byte data to string.
     data = bytes_data.decode('utf-8')
     # st.text(data) # show text in screen

     df = preprocessor.preprocess(data)

     # st.dataframe(df)# Display data frame.

     # Fetch No. of unique users
     user_list = df['user'].unique().tolist()
     user_list.remove('group_notification')
     user_list.sort()


     # Show user Name in
     user_list.insert(0, 'Overall')
     selected_user = st.sidebar.selectbox('Show Anaysis w.r.t', user_list)

     # Click user Button the anaysis start.
     if st.sidebar.button('Show Anaysis'):
          #Create Columns

          num_of_messages, words, num_media_files, num_links = helper.fetch_stats(selected_user, df)
          # Heading
          st.title('Top Statistics')
          col1, col2, col3, col4 = st.columns(4)



          with col1:
               st.header('Total Messages')
               st.title(num_of_messages)
          with col2:
               st.header('Total Words')
               st.title(words)
          with col3:
               st.header('Total Media Files')
               st.title(num_media_files)
          with col4:
               st.header('Total Link')
               st.title(num_links)




          # Time Based Analysis

          # monthly timeline
          timeline = helper.monthly_timeline(selected_user, df)
          fig, ax = plt.subplots()
          ax.plot(timeline['time'], timeline['message'])
          plt.xticks(rotation='vertical')
          st.title('Monthly Chat Timeline')
          st.pyplot(fig)




          # daily timeline
          daily_timeline = helper.daily_timeline(selected_user,df)
          # plt.figure(figsize=(10, 10))
          fig, ax = plt.subplots(figsize=(10, 10))
          ax.plot(daily_timeline['only_date'], daily_timeline['message'])
          plt.xticks(rotation='vertical')
          st.title('Daily Chat Timeline')
          st.pyplot(fig)




          st.title('Activity Map')
          col1,col2 = st.columns(2)

          with col1:
               st.header('Most Busy Day')
               busy_day = helper.weekly_active(selected_user,df)
               fig,ax = plt.subplots()
               ax.bar(busy_day.index, busy_day.values)
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          with col2:
               st.header('Most Busy Month')
               busy_month = helper.monthly_active(selected_user,df)
               fig,ax = plt.subplots()
               ax.bar(busy_month.index, busy_month.values, color='orange')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)


          # Heatmap
          st.title('Weekly Activity Map')
          user_heatmap = helper.activity_headmap(selected_user,df)
          fig,ax = plt.subplots()
          ax = sns.heatmap(user_heatmap)
          plt.yticks(rotation='horizontal')
          st.pyplot(fig)




          # finding the busiest users in the group (group level)
          if selected_user == 'Overall':
               st.title('Most Busy Users')
               x, per_df = helper.most_busy_users(df)
               fig, ax = plt.subplots()

               col1, col2 = st.columns(2)

               with col1:
                    ax.bar(x.index, x.values, color='red')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(per_df)





          # Word-Cloud(1:12:00) # used of create a random text images.
          st.title('Word Cloud')
          df_wc = helper.create_wordcloud(selected_user,df)
          fig, ax = plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)






          # most_common_words (Extra - WordCloud mai bhi hum word ki filtering kr skte hai)
          words_df = helper.most_common_words(selected_user, df)
          # st.dataframe(words_df) # Convert to bar graph
          fig, ax = plt.subplots()
          ax.barh(words_df[0], words_df[1])
          plt.xticks(rotation='vertical')
          st.title('Most Common Words')
          st.pyplot(fig)
          

          # Emoji Analysis
          emojis_df = helper.most_common_emojis(selected_user,df)
          st.title("Emoji Analyser")

          col1,col2 = st.columns(2)

          with col1:
               st.dataframe(emojis_df)
          # # do after some time
          # while col2:
          #      fig, ax = plt.subplots()
          #      ax.pie(emojis_df[1].head(), labels=emojis_df[0].head(), autopct='%0.2f')
          #      st.pyplot(fig)














