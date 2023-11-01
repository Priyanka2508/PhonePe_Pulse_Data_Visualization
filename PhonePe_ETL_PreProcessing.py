#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[2]:


# [clone libraries]
import requests
import subprocess
# import git

# [pandas and file handling libraries]
import pandas as pd
import numpy as np
import os
import json

# [SQL libraries]
import pymysql
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine



# In[3]:


get_ipython().system('pip install mysql.connector')
get_ipython().system('pip install sqlalchemy')
get_ipython().system('pip install mysql.connector.python')


# In[ ]:


#Specify the GitHub repository URL and local directory path
github_url = "https://github.com/PhonePe/pulse.git"
# local_dir = "C:/Phonepe Pulse data"
#
# # Clone the repository to the specified local directory
# git.Repo.clone_from(github_url, local_dir)


# # DATA PROCESSING

# In[78]:


# Aggreagetd Transaction

path_1 = "C:/Phonepe Pulse data/data/aggregated/transaction/country/india/state/"
state_list = os.listdir(path_1)

Agg_tra = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
           'Transaction_amount': []}

for i in state_list:
    p_i = path_1 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            Data = open(p_k, 'r')
            A = json.load(Data)

            for l in A['data']['transactionData']:
                Name = l['name']
                count = l['paymentInstruments'][0]['count']
                amount = l['paymentInstruments'][0]['amount']
                Agg_tra['State'].append(i)
                Agg_tra['Year'].append(j)
                Agg_tra['Quarter'].append(int(k.strip('.json')))
                Agg_tra['Transaction_type'].append(Name)
                Agg_tra['Transaction_count'].append(count)
                Agg_tra['Transaction_amount'].append(amount)

df_aggregated_transaction = pd.DataFrame(Agg_tra)
df_aggregated_transaction.to_csv('Aggregated_Transaction_Table.csv',index=False)  


# In[79]:


df_aggregated_transaction.shape
df_aggregated_transaction.describe()
df_aggregated_transaction.head(20)
df_aggregated_transaction.isna().sum()


# In[15]:


# Aggreagted User

path_2 = "C:/Phonepe Pulse data/data/aggregated/user/country/india/state/"
Agg_user_state_list = os.listdir(path_2)

Agg_user = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'User_Count': [], 'User_Percentage': []}

for i in Agg_user_state_list:
    p_i = path_2 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            Data = open(p_k, 'r')
            B = json.load(Data)

            try:
                for l in B["data"]["usersByDevice"]:
                    brand_name = l["brand"]
                    count_ = l["count"]
                    ALL_percentage = l["percentage"]
                    Agg_user["State"].append(i)
                    Agg_user["Year"].append(j)
                    Agg_user["Quarter"].append(int(k.strip('.json')))
                    Agg_user["Brands"].append(brand_name)
                    Agg_user["User_Count"].append(count_)
                    Agg_user["User_Percentage"].append(ALL_percentage * 100)
            except:
                pass

df_aggregated_user = pd.DataFrame(Agg_user)

df_aggregated_user.to_csv('Aggregated_User_Table.csv',index=False) 


# In[16]:


df_aggregated_user.shape
df_aggregated_user.describe()
df_aggregated_user.head(20)
df_aggregated_user.isna().sum()


# In[17]:


# Map Transaction

path_3 = "C:/Phonepe Pulse data/data/map/transaction/hover/country/india/state/"
map_tra_state_list = os.listdir(path_3)

map_tra = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_Count': [], 'Transaction_Amount': []}

for i in map_tra_state_list:
    p_i = path_3 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            Data = open(p_k, 'r')
            C = json.load(Data)

            for l in C["data"]["hoverDataList"]:
                District = l["name"]
                count = l["metric"][0]["count"]
                amount = l["metric"][0]["amount"]
                map_tra['State'].append(i)
                map_tra['Year'].append(j)
                map_tra['Quarter'].append(int(k.strip('.json')))
                map_tra["District"].append(District)
                map_tra["Transaction_Count"].append(count)
                map_tra["Transaction_Amount"].append(amount)

df_map_transaction = pd.DataFrame(map_tra)

df_map_transaction.to_csv('Map_Transaction_Table.csv',index=False)



# In[18]:


df_map_transaction.shape
df_map_transaction.describe()
df_map_transaction.head(20)
df_map_transaction.isna().sum()


# In[20]:


# Map User

path_4 = "C:/Phonepe Pulse data/data/map/user/hover/country/india/state/"
map_user_state_list = os.listdir(path_4)

map_user = {"State": [], "Year": [], "Quarter": [], "District": [], "Registered_User": []}

for i in map_user_state_list:
    p_i = path_4 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            Data = open(p_k, 'r')
            D = json.load(Data)

            for l in D["data"]["hoverData"].items():
                district = l[0]
                registereduser = l[1]["registeredUsers"]
                map_user['State'].append(i)
                map_user['Year'].append(j)
                map_user['Quarter'].append(int(k.strip('.json')))
                map_user["District"].append(district)
                map_user["Registered_User"].append(registereduser)

df_map_user = pd.DataFrame(map_user)
df_map_user.to_csv('Map_User_Table.csv', index = False)


# In[21]:


df_map_user.shape
df_map_user.describe()
df_map_user.head(20)
df_map_user.isna().sum()


# In[22]:


# Top Transaction 

path_5 = "C:/Phonepe Pulse data/data/top/transaction/country/india/state/"
top_tra_state_list = os.listdir(path_5)

top_tra = {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'Transaction_count': [],
           'Transaction_amount': []}

for i in top_tra_state_list:
    p_i = path_5 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            Data = open(p_k, 'r')
            E = json.load(Data)

            for l in E['data']['pincodes']:
                Name = l['entityName']
                count = l['metric']['count']
                amount = l['metric']['amount']
                top_tra['State'].append(i)
                top_tra['Year'].append(j)
                top_tra['Quarter'].append(int(k.strip('.json')))
                top_tra['District_Pincode'].append(Name)
                top_tra['Transaction_count'].append(count)
                top_tra['Transaction_amount'].append(amount)

df_top_transaction = pd.DataFrame(top_tra)
df_top_transaction.to_csv('Top_Transaction_Table.csv', index = False)


# In[23]:


df_top_transaction.shape
df_top_transaction.describe()
df_top_transaction.head(20)
df_top_transaction.isna().sum()


# In[80]:


# Top User

path_6 = "C:/Phonepe Pulse data/data/top/user/country/india/state/"
top_user_state_list = os.listdir(path_6)

top_user = {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'Registered_User': []}

for i in top_user_state_list:
    p_i = path_6 + i + "/"
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + j + "/"
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + k
            Data = open(p_k, 'r')
            F = json.load(Data)

            for l in F['data']['pincodes']:
                Name = l['name']
                registeredUser = l['registeredUsers']
                top_user['State'].append(i)
                top_user['Year'].append(j)
                top_user['Quarter'].append(int(k.strip('.json')))
                top_user['District_Pincode'].append(Name)
                top_user['Registered_User'].append(registeredUser)

df_top_user = pd.DataFrame(top_user)
df_top_user.to_csv('Top_User_Table.csv', index = False)


# In[81]:


df_top_user.shape
df_top_user.describe()
df_top_user.head(20)
df_top_user.isna().sum()


# In[82]:


#  =============     CONNECT SQL SERVER  /   CREAT DATA BASE    /  CREAT TABLE    /    STORE DATA    ========  #

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "alohomora25",
  auth_plugin = "mysql_native_password",
)


# In[29]:


# Create a new database and use
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_db")

# Close the cursor and database connection
mycursor.close()
mydb.close()


