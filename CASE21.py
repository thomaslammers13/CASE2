#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json


# #### Create olympic games dataframe from csv

# In[2]:


df=pd.read_csv('athlete_events.csv')


# #### Drop the winter olympics

# In[3]:


df.drop(df[df['Season'] == 'Winter'].index, inplace = True)


# #### Create a list of unique values of 'City'

# In[4]:


st.title('Data merge')
st.markdown('**Before the data analysis, the unique summer cities are being defined, see dataframe below:**')

st.text('df.drop(df[df["Season"] == "Winter"].index, inplace = True)')
unique_cities = pd.unique(df['City'])
unique_cities


# #### Use the unique_cities to gather data from the Country API made by API Ninjas
# Note: some of the cities have missing data which is no problem for use.

# In[5]:


response_list = []
for country in unique_cities:
    print(country)
    
    api_url = 'https://api.api-ninjas.com/v1/country?name={}'.format(country)
    response1 = requests.get(api_url, headers={'X-Api-Key': '0eJ24h1oAq0DwwYAz67D3Q==EaKYACEsoPSFRO2M'})
   
    response1 = response1.text[1:-1]
    print(response1)
    
    if response1 !='': 
        response1 = json.loads(response1) #json.loads() is used to transform the string dictionaries to pandas dictionaries.
    if response1 != '': 
        response_list.append(response1) #If the response1 is not empty. Append to response_list


# #### Create df_countries

# In[6]:


df_countries = pd.DataFrame.from_dict(response_list)
st.markdown('**After the response_list is created, a dataframe is created with the response list as a Dataframe**')

st.text('df_countries = pd.DataFrame.from_dict(response_list)')


# #### Create countries with only the usefull data we will use

# In[7]:


countries = df_countries[['name','capital','population',]]
print(countries)
st.markdown('**Next, the name, the capital and the population is selected**')

st.text('countries = df_countries[["name","capital", "population",]]')


# #### Join the countries dataframe on df

# In[8]:


df = pd.merge(df, countries, left_on="Team", right_on="name")
st.markdown('**The final step: merging the countries**')

st.text('df = pd.merge(df, countries, left_on="Team", right_on="name")')

st.markdown('**The final merged dataframe:**')
df


# In[9]:


df.to_csv('DATAFRAMEAPP.csv')


# In[10]:


st.title("Data analysis")
st.markdown('**On this page, the data from the dataset will be explored. The dataset contains data about the olympic games of the past 120 years.**')
st.sidebar.title('Navigation')


# #### Check the keys of df

# In[11]:


print(df.keys())


# #### Check the shape of df

# In[12]:


df.shape


# #### Check the Non-Null values and datatype of each column

# In[13]:


df.info()


# #### View statistical details of df

# In[14]:


df.describe()


# #### View number of unique values

# In[15]:


df.nunique()


# In[16]:


uploaded_file = st.file_uploader('Upload file here')

if uploaded_file:
    st.header('Data Statistics')
    df = pd.read_csv(uploaded_file)
    st.write(df.describe())

    
    st.header('Data Header')
    st.write(df.head())
    

st.header("Data manipulation")
st.markdown('**In this part, the certain values are being dropped. These are the missing values for the columns MEDAL, HEIGHT, WEIGHT and all rows from before 1945. Meanwhile, the variable BMI is being added. This variables calculates the BMI for every athlete**')


df.drop(df[df['Season'] == 'Winter'].index, inplace = True)
df.dropna(subset = ['Medal'], inplace = True)
df.dropna(subset = ['Height'], inplace = True)
df.dropna(subset = ['Weight'], inplace = True)
df.drop(df[df['Year'] <= 1945].index, inplace = True)
df["BMI"] = df["Weight"] / (df["Height"]/100)**2

st.write("df.drop(df[df['Season'] == 'Winter'].index, inplace = True)")
st.write("df.dropna(subset = ['Medal'], inplace = True)")    
st.write("df.dropna(subset = ['Height'], inplace = True)")
st.write("df.dropna(subset = ['Weight'], inplace = True)")
st.write("df.drop(df[df['Year'] <= 1945].index, inplace = True)")
st.write("(df['BMI'] = df['Weight'] / (df['Height']/100)**2)")


# In[17]:


df.sort_values(by=["Year"])
df


# In[ ]:





# In[30]:


st.header("Scatterplot with dropdown menu")
st.sidebar.header('Select values for scatterplot')
x_selectbox = st.sidebar.selectbox('Select X Value', options = df.columns)
y_selectbox = st.sidebar.selectbox('Select Y Value', options = df.columns)


# In[19]:


plot = px.scatter(df, x=x_selectbox, y =y_selectbox, title="BMI spread for every Olympic Game")
st.plotly_chart(plot)


# In[20]:


st.header("Plot with slider")


# In[21]:


st.sidebar.header('Slider for plot top countries')
add_slider = st.sidebar.slider(
    'Select a number of countries', 0, 30, (0))

    
   


# In[22]:


df.drop(df[df['Year'] <= 2012].index, inplace = True)
df_medals = df.groupby(["Team", "Year"])["Medal"].count()
df_medals1 = df_medals.sort_values(ascending=False)
df_Medals = df_medals1[0:add_slider]
df_dropdown = pd.DataFrame(df_Medals)

df_dropdown = df_dropdown.reset_index()
st.text('Top Countries')
df_dropdown


# In[23]:


plot1 = px.bar(df_dropdown, x="Team", y = "Medal", title="Medals for top countries in 2016")
st.plotly_chart(plot1)


# In[24]:


df_Medalstwo = df_medals1[5:10]
df_dropdowntwo = pd.DataFrame(df_Medalstwo)

df_dropdowntwo = df_dropdowntwo.reset_index()
st.text('Places 5 to 10')
df_dropdowntwo


# In[ ]:





# In[ ]:





# In[25]:


if st.checkbox('Show places 5 to 10'):
  plot2 = px.bar(df_dropdowntwo, x="Team", y = "Medal", title="Medals for top 5 to 10 countries 2016")
  st.plotly_chart(plot2)


# In[31]:


st.header('Boxplot with age versus medals')
df.drop(df[df['Year'] <= 2014].index, inplace = True)

x_selectbox1 = st.sidebar.selectbox('Select Sport', options = df.groupby("Event")["Event"].unique())



# In[ ]:





# In[32]:


df.drop(df[df['Event'] != "Cycling Men's Sprint"].index, inplace = True)


# In[33]:


fig = px.box(df, x='Event', y = "BMI")
st.plotly_chart(fig)


# In[34]:


fig1 = px.box(df, x='Event', y = "BMI")
st.plotly_chart(fig1)


# In[ ]:





# In[ ]:





# In[ ]:




