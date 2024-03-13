#!/usr/bin/env python
# coding: utf-8

# In[32]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from datetime import date,datetime


# In[56]:


sites = ['https://24petconnect.com/WACO',
         'https://24petconnect.com/WACO?index=30',
         'https://24petconnect.com/WACO?index=60',
         'https://24petconnect.com/WACO?index=90',
         'https://24petconnect.com/WACO?index=120',
         'https://24petconnect.com/WACO?index=150',
         'https://24petconnect.com/WACO?index=180',
         'https://24petconnect.com/WACO?index=210',
         'https://24petconnect.com/WACO?index=240',
         'https://24petconnect.com/WACO?index=270']


# In[60]:


def get_site(site):
    website = site
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'html.parser')

    dogs = soup.find_all('div', class_='gridResult')


# In[67]:


df = pd.DataFrame(columns=['ID', 'Name', 'Gender', 'Breed', 'Age', 'Arrival', 'Time'])


# In[64]:


def into_df(site):
    website = site
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content, 'html.parser')
    dogs = soup.find_all('div', class_='gridResult')
    
    for i in dogs:
        dog_name_and_id = i.find(class_='text_Name results').text.strip()
        name, dog_id= dog_name_and_id[:-1].split(" (")
        gender = i.find(class_='text_Gender results').text.strip()
        breed = i.find(class_='text_Breed results').text.strip()
        age = i.find(class_='text_Age results').text.strip()
        arrival_text = i.find(class_='text_Broughttotheshelter results').text.strip()
        arrival = datetime.strptime(arrival_text, '%Y.%m.%d').date()
        time = (date.today() - arrival).days

        row = {'ID': dog_id,
              'Name': name,
              'Gender': gender,
              'Breed': breed,
              'Age': age,
              'Arrival': arrival,
              'Time': time}
        df.loc[len(df.index)] = row


# In[68]:


for i in sites:
    into_df(i)


# In[69]:


display(df.sort_values('ID'))

