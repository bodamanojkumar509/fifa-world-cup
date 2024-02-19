#!/usr/bin/env python
# coding: utf-8

# In[5]:


import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import numpy as np
import pandas as pd
import plotly.express as px


# In[6]:


get_ipython().system('pip install wordcloud')


# In[8]:


get_ipython().system('pip install pandas-profiling')


# In[25]:


fifa_df = pd.read_csv("C:/Users/KADAVATH LATHA/Downloads/Fifa_WC_2022_Match_data.csv", encoding='latin1')


# In[26]:


player_stat_df = pd.read_csv("C:/Users/KADAVATH LATHA/Downloads/player_stats.csv", encoding='latin1')


# In[27]:


fifa_df.head(2)


# In[28]:


fifa_df.info()


# In[29]:


fifa_df.isnull().sum()


# In[30]:


print(fifa_df.columns)


# In[31]:


print(fifa_df.head())


# In[33]:


# add 1_goals and 2_goals, create a new col with name total_match_goals 
# and store the added value in that
fifa_df['total_match_goals'] = fifa_df['1_goals'] + fifa_df['2_goals']


# In[34]:


# Show the specific col  i.e 1_goals and 2_goals and total_match_goals
fifa_df.loc[:,['1_goals', '2_goals', 'total_match_goals']].head(10)


# In[35]:


# Highest scoring match
fifa_df[fifa_df['total_match_goals'] == fifa_df['total_match_goals'].max()]


# In[36]:


# Match with highest Attendence
fifa_df[fifa_df['attendance'] == fifa_df['attendance'].max()]


# In[37]:


# Argetina matches
fifa_df[(fifa_df['1'] == 'ARGENTINA') | (fifa_df['2'] == 'ARGENTINA')] 


# In[38]:


# FRANCE matches
fifa_df[(fifa_df['1'] == 'FRANCE') | (fifa_df['2'] == 'FRANCE')] 


# In[39]:


# No. Matches Played on respective venues till QF
fifa_df['venue'].value_counts()


# In[40]:


# Bar graph Venue v/s No of Matches Played at Venue (using plotly)
x = fifa_df['venue'].value_counts().index
y = fifa_df['venue'].value_counts().values

df = pd.DataFrame({'Venue':x,
                  'Matches':fifa_df['venue'].value_counts().values })

fig = px.bar(df, 
             x='Venue', 
             y='Matches',
             color='Venue',
             title='Venue v/s No of Matches Played at Venue'
            )
fig.show()


# In[41]:


# Total Attendance in all the venue of all matches played
fifa_df.groupby('venue').sum()['attendance'].sort_values(ascending=False)


# In[42]:


# Bar graph Venue v/s attendance at Venue (using seaborn) 
x = fifa_df.groupby('venue').sum()['attendance'].index
y = fifa_df.groupby('venue').sum()['attendance'].values
labels = [s.strip('Stadium') for s in x]
df = pd.DataFrame({'venue': labels, 'attendance': y})
plt.figure(figsize=(15, 8))
splot=sns.barplot(x="venue",y="attendance",data=df)
plt.xlabel("Venue", size=16)
plt.ylabel("Attendance", size=16)
plt.title('Venue v/s Total Attendance of all matches played')
plt.bar_label(splot.containers[0],size=16)
plt.show()


# In[43]:


# Bar graph venue v/s attendance at Venue (using plotly)
x = fifa_df.groupby('venue').sum()['attendance'].sort_index().index
y = fifa_df.groupby('venue').sum()['attendance'].sort_index().values

df_1 = pd.DataFrame({'venue': x, 'attendance': y})

fig = px.bar(df_1, x='venue', y='attendance',color='attendance',title='Venue v/s Total Attendance of all matches played')
fig.update_layout(title_text='Venue v/s Total Attendance of all matches played',template='plotly_dark')
fig.show()


# In[44]:


# Venue with max attendance of total matches played 
venue_df = pd.DataFrame({'venue':fifa_df.groupby(['venue'])['attendance'].sum().sort_values(ascending=False).index,
                   'total_attendance': fifa_df.groupby(['venue'])['attendance'].sum().sort_values(ascending=False).values})
venue_df[venue_df['total_attendance'] == venue_df['total_attendance'].max()]


# In[47]:


get_ipython().system('pip install wordcloud')


# In[48]:


from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Your code for creating and displaying the WordCloud


# In[45]:


# Plotiing the wordcloud for the teams
plt.subplots(figsize=(25,15))
wordcloud = WordCloud(
                          background_color='white',
                          width=1920,
                          height=1080
                         ).generate(" ".join(fifa_df['1']))
plt.imshow(wordcloud)
plt.axis('off')
#plt.savefig('teams.png')
plt.show()


# In[49]:


#All Teams
" ".join(fifa_df['1'].sort_values().value_counts().index)


# In[50]:


# Total games played and goals scored by the teams

team_df = pd.DataFrame({'teams':fifa_df['1'].value_counts().sort_index().index,
                        'total_matches':fifa_df['1'].value_counts().sort_index().values + fifa_df['2'].value_counts().sort_index().values,
                        'total_goals': fifa_df.groupby(['1'])['1_goals'].sum().sort_index().values + fifa_df.groupby(['2'])['2_goals'].sum().sort_index().values, 
                         })
team_df.sort_values(by='total_goals', ascending=False)


#team_df.loc[:, ['teams','total_matches','total_goals' ]].sort_values(by='total_goals


# In[51]:


# Bar graph Team v/s Goals Scored (using plotly)

fig = px.bar(team_df, x='teams', y='total_goals',color='total_matches',title='Teams v/s Goals Scored')
fig.update_layout(title_text='Teams v/s Goals Scored',template='plotly_white', width=1000)
fig.show()


# In[52]:


# Highest Goals Scoring Team
team_df[team_df['total_goals'] == team_df['total_goals'].max()]


# In[53]:


# Top 3 highest Goal Scoring Teams
team_df.sort_values(by='total_goals', ascending=False).head(3)


# In[54]:


#lowest Goal Scoring Teams
team_df[team_df['total_goals'] == team_df['total_goals'].min()]


# In[57]:


# no of matches played and passes completed by teams

team_df['total_pass_completed'] = fifa_df.groupby(['1'])['1_passes_compeletd'].sum().sort_index().values + fifa_df.groupby(['2'])['2_passes_compeletd'].sum().sort_index().values

#sort on total_pass_completed
team_df.loc[:,['teams', 'total_matches', 'total_pass_completed']].sort_values(by='total_pass_completed', ascending=False)


# In[58]:


# Bar graph Team v/s pass completed (method 1 using plotly)

fig = px.bar(team_df, x='teams', y='total_pass_completed',color='total_matches',title='Teams v/s Pass Completed')
fig.update_layout(title_text='Teams v/s Pass Completed',template='plotly', width=800)
fig.show()


# In[61]:


print(team_df.columns)


# In[64]:


team_df.loc[team_df['total_pass_completed'] == team_df['total_pass_completed'].max(), ['teams', 'total_matches', 'total_pass_completed']]


# In[66]:


# Top 3 teams w.r.t. the avg_possession
team_df.loc[:,['teams', 'total_matches', 'total_pass_completed']].sort_values(by='total_pass_completed', ascending=False).head(3)


# In[67]:


# Lowest avg_possession by team
team_df.loc[team_df['total_pass_completed'] == team_df['total_pass_completed'].min(), ['teams', 'total_matches', 'total_pass_completed']]


# In[68]:


# Exected Goals(xG) by teams

team_df['avg_xg'] = round((fifa_df.groupby(['1'])['1_xg'].sum().sort_index().values + fifa_df.groupby(['2'])['2_xg'].sum().sort_index().values)/team_df['total_matches'], 2)

#sort on avg_xg
team_df.loc[:,['teams', 'total_matches', 'avg_xg']].sort_values(by='avg_xg', ascending=False)


# In[69]:


# Bar graph Teams v/s Exected Goals(xG) 

fig = px.bar(team_df, x='teams', y='avg_xg',color='total_matches',title='Teams v/s Exected Goals(xG) ')
fig.update_layout(title_text='Teams v/s Exected Goals(xG)  ',template='seaborn')
fig.show()


# In[70]:


# Highest Exected Goals(xG) by teams
team_df.loc[team_df['avg_xg'] == team_df['avg_xg'].max(), ['teams', 'total_matches', 'avg_xg']]


# In[71]:


# Top 3 teams w.r.t. the Exected Goals(xG)
team_df.loc[:,['teams', 'total_matches', 'avg_xg']].sort_values(by='avg_xg', ascending=False).head(3)


# In[72]:


# Lowest Exected Goals(xG) by team
team_df.loc[team_df['avg_xg'] == team_df['avg_xg'].min(), ['teams', 'total_matches', 'avg_xg']]


# In[73]:


# This is how team_df looks like after the above iterations 
# sorted in alphabetical order
team_df.head(32)


# In[74]:


# Yellow Cards by teams 

team_df['total_yellow_cards'] = (fifa_df.groupby(['1'])['1_yellow_cards'].sum().sort_index().values + fifa_df.groupby(['2'])['2_yellow_cards'].sum().sort_index().values)

#sort on total_yellow_cards
team_df.loc[:, ['teams', 'total_matches', 'total_yellow_cards']].sort_values(by='total_yellow_cards', ascending=False)


# In[75]:


# Bar graph Teams v/s Yellow Cards

fig = px.bar(team_df, x='teams', y='total_yellow_cards',color='total_matches',title='Teams v/s Yellow Cards ')
fig.update_layout(title_text='Teams v/s Yellow Cards  ',template='simple_white')
fig.show()


# In[76]:


# Highest Yellow Cards by teams
team_df.loc[team_df['total_yellow_cards'] == team_df['total_yellow_cards'].max(), ['teams', 'total_matches', 'total_yellow_cards']]


# In[77]:


# Top 3 teams w.r.t. the Yellow Cards
team_df.loc[:,['teams', 'total_matches', 'total_yellow_cards']].sort_values(by='total_yellow_cards', ascending=False).head(3)


# In[78]:


# Lowest Yellow Cards by teams
team_df.loc[team_df['total_yellow_cards'] == team_df['total_yellow_cards'].min(), ['teams', 'total_matches', 'total_yellow_cards']]


# In[79]:


# Teams with Red Cards

team_df['total_red_cards'] = (fifa_df.groupby(['1'])['1_red_cards'].sum().sort_index().values + fifa_df.groupby(['2'])['2_red_cards'].sum().sort_index().values)
team_df.loc[team_df['total_red_cards'] != 0, ['teams', 'total_matches', 'total_red_cards']].sort_values(by='total_red_cards', ascending=False)


# In[80]:


# Total games played and goals conceded by the teams  

team_df['total_goals_conceded'] = (fifa_df.groupby(['1'])['1_conceded'].sum().sort_index().values + fifa_df.groupby(['2'])['2_conceded'].sum().sort_index().values)

#sort on goals conceded
team_df.loc[:, ['teams', 'total_matches', 'total_goals_conceded']].sort_values(by='total_goals_conceded', ascending=False)


# In[81]:


# Bar graph Teams v/s Total Goals Conceded

fig = px.bar(team_df, x='teams', y='total_goals_conceded',color='total_matches',title='Teams v/s Total Goals Conceded ')
fig.update_layout(title_text='Teams v/s Total Goals Conceded  ',template='none')
fig.show()


# In[82]:


# Team with Highest Goal Conceded
team_df.loc[team_df['total_goals_conceded'] == team_df['total_goals_conceded'].max(), ['teams', 'total_matches', 'total_goals_conceded']]


# In[83]:


# Team with Lowest Goal Conceded
team_df.loc[team_df['total_goals_conceded'] == team_df['total_goals_conceded'].min(), ['teams', 'total_matches', 'total_goals_conceded']]


# In[84]:


# Top 3 teams w.r.t. the Goal Conceded
team_df.loc[:,['teams', 'total_matches', 'total_goals_conceded']].sort_values(by='total_goals_conceded', ascending=False).head(3)


# In[85]:


# Teams with own goals  

team_df['total_own_goals'] = (fifa_df.groupby(['1'])['1_own_goal'].sum().sort_index().values + fifa_df.groupby(['2'])['2_own_goal'].sum().sort_index().values)

#sort on total_own_goals
team_df.loc[team_df['total_own_goals'] != 0, ['teams', 'total_matches', 'total_own_goals']].sort_values(by='total_own_goals', ascending=False)


# In[86]:


# Total games played and goals conceded by the teams excluding own goals  

team_df['goals_by_opponent'] = team_df['total_goals_conceded'] - team_df['total_own_goals']

#sort on goals_by_opponent
team_df.loc[:, ['teams','total_matches','total_goals_conceded','total_own_goals', 'goals_by_opponent']].sort_values(by='goals_by_opponent', ascending=False)


# In[87]:


# Bar graph Teams v/s Total Goals Conceded(excluding Own Goal)

fig = px.bar(team_df, x='teams', y='goals_by_opponent',color='total_matches',title='Teams v/s Total Goals Conceded(excluding Own Goal) ')
fig.update_layout(title_text='Teams v/s Total Goals Conceded(excluding Own Goal)  ',template='plotly_white')
fig.show()


# In[88]:


player_stat_df.head()


# In[89]:


player_stat_df.info()


# In[90]:


# Top Goal Scorer of WC 2022 | Golden Boot Award
#player_stat_df[player_stat_df['goals'] == player_stat_df['goals'].max()]
player_stat_df.loc[player_stat_df['goals'] == player_stat_df['goals'].max(), ['player', 'team','birth_year', 'club','games', 'assists','goals' ] ]


# In[91]:


# Top 5 Goal Scorer of WC 2022
player_stat_df.loc[:, ['player', 'team','birth_year', 'club','games', 'assists','goals' ] ].sort_values(by='goals', ascending=False).head(5)


# In[92]:


player_stat_df[player_stat_df['xg'] == player_stat_df['xg'].max()]


# In[93]:


# Top Goal Assist of WC 2022 
player_stat_df.loc[player_stat_df['assists'] == player_stat_df['assists'].max(), ['player', 'team','birth_year', 'club','games', 'assists','goals' ] ].sort_values(by='goals', ascending=False)


# In[94]:


profile = ProfileReport(team_df)
profile


# In[ ]:




