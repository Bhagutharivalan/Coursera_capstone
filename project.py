#!/usr/bin/env python
# coding: utf-8

# ## Segregation and clustering neighbourhoods in toronto city

# In[1]:


#Libraries needed
import numpy as np 
import requests
import pandas as pd 
from bs4 import BeautifulSoup # To webscarp the data
import json # Library to handle JSON files
#!conda install -c conda-forge geopy --yes 
from geopy.geocoders import Nominatim # To transform an address into geographical Coordinates
from pandas.io.json import json_normalize #To tranform JSON file into a pandas dataframe

# Matplotlib for data visualization
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

print('Libraries downloaded.')


# In[2]:


url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'


# In[3]:


result = requests.get(url).text


# In[4]:


# webscarping data using beautifulsoup package
soup = BeautifulSoup(result, 'html.parser')


# In[5]:


#creating lists to store parsed data
postalCode = []
borough = []
neighborhood = []


# In[6]:


# parsing
for row in soup.find('table').find_all('tr'):
    cells = row.find_all('td')
    if(len(cells) > 0):
        postalCode.append(cells[0].text)
        borough.append(cells[1].text)
        neighborhood.append(cells[2].text.rstrip('\n'))


# In[7]:


# Creating a DataFrame from the three lists
toronto = pd.DataFrame({"PostalCode": postalCode,
                           "Borough": borough,
                           "Neighborhood": neighborhood})


# In[8]:


toronto


# In[9]:


# Removing the whitespacings and '\n' obtained from parsing
toronto['PostalCode'] = toronto['PostalCode'].apply(lambda x: x.strip())
toronto['Borough'] = toronto['Borough'].apply(lambda x: x.strip())


# In[10]:


# Dropping the Boroughs with 'Not assigned'
toronto = toronto[toronto.Borough != 'Not assigned'].reset_index(drop=True)


# In[11]:


toronto


# In[12]:


# Grouping PostalCode and Borough coloumns
toronto_grouped = toronto.groupby(["PostalCode", "Borough"], as_index=False).agg(lambda x: ", ".join(x))
toronto_grouped 


# In[18]:


# Assigning the name of borough for the neighborhood with "Not assigned"
for index, i in toronto_grouped.iterrows():
    if i["Neighborhood"] == "Not assigned":
        i["Neighborhood"] = row["Borough"]


# In[19]:


#Checking the shape
toronto_grouped.shape


# In[20]:


data = pd.read_csv('https://cocl.us/Geospatial_data')


# In[21]:


data.rename(columns={"Postal Code":"PostalCode"},inplace=True)


# In[24]:


#new dataframe containing final data in new_df
new_df=toronto_grouped.merge(data,on="PostalCode",how = "left")
new_df


# In[ ]:





# In[ ]:




