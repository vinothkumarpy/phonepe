import pandas as pd
import json
import os as os
import mysql.connector
import os
import json
from streamlit_option_menu import option_menu


data=open(r'D:\vs_code\pulse-master\data\aggregated\transaction\country\india\state\andaman-&-nicobar-islands\2018\1.json','r')
js=json.load(data)
print(js)

#CREATE DF df_Agg_Trans

path=r"D:\vs_code\pulse-master\data\aggregated\transaction\country\india\state"
Agg_state_list=os.listdir(path)
Agg_state_list


clm={'State':[], 'Year':[],'Quater':[],'Transacion_type':[], 'Transacion_count':[], 'Transacion_amount':[]}


for i in Agg_state_list:
    p_i=path+"/"+i
    Agg_yr=os.listdir(p_i)
    
    for j in Agg_yr:
        p_j=p_i+"/"+j
        Agg_yr_list=os.listdir(p_j)
        
        for k in Agg_yr_list:
            p_k=p_j+'/'+k
            Data=open(p_k,'r')
            D=json.load(Data)
            
            for z in D['data']['transactionData']:
              Name=z['name']
              count=z['paymentInstruments'][0]['count']
              amount=z['paymentInstruments'][0]['amount']
              clm['Transacion_type'].append(Name)
              clm['Transacion_count'].append(count)
              clm['Transacion_amount'].append(amount)
              clm['State'].append(i)
              clm['Year'].append(j)
              clm['Quater'].append(int(k.strip('.json')))
#Succesfully created a dataframe
df_Agg_Trans=pd.DataFrame(clm)
print(df_Agg_Trans)


#Agg_User

path_2=r"D:\vs_code\pulse-master\data\aggregated\user\country\india\state"
Agg_userstate_list=os.listdir(path_2)
Agg_userstate_list

clm_2={'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'User_Count': [], 'User_Percentage': []}

for i in Agg_userstate_list:
    p_i = path_2 + "/" + i 
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + "/" +  j 
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + "/" + k
            Data = open(p_k, 'r')
            B = json.load(Data)
            
            try:
                for l in B["data"]["usersByDevice"]:
                    brand_name = l["brand"]
                    count_ = l["count"]
                    ALL_percentage = l["percentage"]
                    clm_2["State"].append(i)
                    clm_2["Year"].append(j)
                    clm_2["Quarter"].append(int(k.strip('.json')))
                    clm_2["Brands"].append(brand_name)
                    clm_2["User_Count"].append(count_)
                    clm_2["User_Percentage"].append(ALL_percentage*100)
            except:
                pass

df_Agg_user = pd.DataFrame(clm_2)
print(df_Agg_user)

# map trans

path_3=r"D:\vs_code\pulse-master\data\map\transaction\hover\country\india\state"
map_trans_state_list=os.listdir(path_2)
map_trans_state_list


clm_3 = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Transaction_Count': [], 'Transaction_Amount': []}

for i in map_trans_state_list:
    p_i = path_3 + "/" + i  
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + "/" + j 
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + "/"+ k
            Data = open(p_k, 'r')
            C = json.load(Data)
            
            for l in C["data"]["hoverDataList"]:
                District = l["name"]
                count = l["metric"][0]["count"]
                amount = l["metric"][0]["amount"]
                clm_3['State'].append(i)
                clm_3['Year'].append(j)
                clm_3['Quarter'].append(int(k.strip('.json')))
                clm_3["District"].append(District)
                clm_3["Transaction_Count"].append(count)
                clm_3["Transaction_Amount"].append(amount)
                
df_map_trans = pd.DataFrame(clm_3)

print(df_map_trans)

#map_user

path_4=r"D:\vs_code\pulse-master\data\map\user\hover\country\india\state"
map_user_state_list=os.listdir(path_4)
map_user_state_list

clm_4= {"State": [], "Year": [], "Quarter": [], "District": [], "Registered_User": []}

for i in map_user_state_list:
    p_i = path_4 + "/" +i 
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + "/" + j
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + "/" + k
            Data = open(p_k, 'r')
            D = json.load(Data)

            for l in D["data"]["hoverData"].items():
                district = l[0]
                registereduser = l[1]["registeredUsers"]
                clm_4['State'].append(i)
                clm_4['Year'].append(j)
                clm_4['Quarter'].append(int(k.strip('.json')))
                clm_4["District"].append(district)
                clm_4["Registered_User"].append(registereduser)
                
df_map_user = pd.DataFrame(clm_4)

print(df_map_user)


#top trans

path_5=r"D:\vs_code\pulse-master\data\top\transaction\country\india\state"
top_trans_state_list=os.listdir(path_5)
top_trans_state_list

clm_5= {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'Transaction_count': [], 'Transaction_amount': []}

for i in top_trans_state_list:
    p_i = path_5 + "/" + i 
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + "/" +j
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + "/" + k
            Data = open(p_k, 'r')
            E = json.load(Data)
            
            for l in E['data']['pincodes']:
                Name = l['entityName']
                count = l['metric']['count']
                amount = l['metric']['amount']
                clm_5['State'].append(i)
                clm_5['Year'].append(j)
                clm_5['Quarter'].append(int(k.strip('.json')))
                clm_5['District_Pincode'].append(Name)
                clm_5['Transaction_count'].append(count)
                clm_5['Transaction_amount'].append(amount)

df_top_trans = pd.DataFrame(clm_5)

df_top_trans

#top user

path_6=r'D:\vs_code\pulse-master\data\top\user\country\india\state'
top_user_state_list=os.listdir(path_6)
top_user_state_list

clm_6 = {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'Registered_User': []}

for i in top_user_state_list:
    p_i = path_6 + "/" + i
    Agg_yr = os.listdir(p_i)

    for j in Agg_yr:
        p_j = p_i + "/" + j
        Agg_yr_list = os.listdir(p_j)

        for k in Agg_yr_list:
            p_k = p_j + "/" +  k
            Data = open(p_k, 'r')
            F = json.load(Data)
            
            for l in F['data']['pincodes']:
                Name = l['name']
                registeredUser = l['registeredUsers']
                clm_6['State'].append(i)
                clm_6['Year'].append(j)
                clm_6['Quarter'].append(int(k.strip('.json')))
                clm_6['District_Pincode'].append(Name)
                clm_6['Registered_User'].append(registeredUser)
                
df_top_user = pd.DataFrame(clm_6)
df_top_user

#--------------------------->>>>>>>>>>>>>>------------------------------->>>>>>>>>>>>>>

#drop dublicates
d1 = df_Agg_Trans.drop_duplicates()
d2 = df_Agg_user.drop_duplicates()
d3 = df_map_trans.drop_duplicates()
d4 = df_map_user.drop_duplicates()
d5 = df_top_trans.drop_duplicates()
d6 = df_top_user.drop_duplicates()
#______________________________________________________________________________________

#checking Null values

null_counts = d1.isnull().sum()
print(null_counts)

null_counts = d2.isnull().sum()
print(null_counts)

null_counts = d3.isnull().sum()
print(null_counts)

null_counts = d4.isnull().sum()
print(null_counts)

null_counts = d5.isnull().sum()
print(null_counts)

null_counts = d6.isnull().sum()
print(null_counts)
#______________________________________________________________________________________________

# connect sql server

import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine

# Connect to the MySQL server
mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "vino8799",
  database = "phonepe_pulsedb"
)

# Create a new database and use
mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS phonepe_pulse_db")

# Close the cursor and database connection
mycursor.close()
mydb.close()

#create engine to connect and insert the df one by one
engine = create_engine('mysql+mysqlconnector://root:vino8799@localhost/phonepe_pulse_db', echo=False)

#insert all dataframes in to sql
df_Agg_Trans.to_sql('aggregated_transaction', engine, if_exists = 'replace', index=False,   
                                 dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
                                       'Year': sqlalchemy.types.Integer, 
                                       'Quater': sqlalchemy.types.Integer, 
                                       'Transaction_type': sqlalchemy.types.VARCHAR(length=50), 
                                       'Transaction_count': sqlalchemy.types.Integer,
                                       'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})



# 2
df_Agg_user.to_sql('aggregated_user', engine, if_exists = 'replace', index=False,
                          dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
                                 'Year': sqlalchemy.types.Integer, 
                                 'Quater': sqlalchemy.types.Integer,
                                 'Brands': sqlalchemy.types.VARCHAR(length=50), 
                                 'User_Count': sqlalchemy.types.Integer, 
                                 'User_Percentage': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})

# 3                       
df_map_trans.to_sql('map_transaction', engine, if_exists = 'replace', index=False,
                          dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
                                 'Year': sqlalchemy.types.Integer, 
                                 'Quater': sqlalchemy.types.Integer, 
                                 'District': sqlalchemy.types.VARCHAR(length=50), 
                                 'Transaction_Count': sqlalchemy.types.Integer, 
                                 'Transaction_Amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})

# 4
df_map_user.to_sql('map_user', engine, if_exists = 'replace', index=False,
                   dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
                          'Year': sqlalchemy.types.Integer, 
                          'Quater': sqlalchemy.types.Integer, 
                          'District': sqlalchemy.types.VARCHAR(length=50), 
                          'Registered_User': sqlalchemy.types.Integer, })

# 5                  
df_top_trans.to_sql('top_transaction', engine, if_exists = 'replace', index=False,
                         dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
                                'Year': sqlalchemy.types.Integer, 
                                'Quater': sqlalchemy.types.Integer,   
                                'District_Pincode': sqlalchemy.types.Integer,
                                'Transaction_count': sqlalchemy.types.Integer, 
                                'Transaction_amount': sqlalchemy.types.FLOAT(precision=5, asdecimal=True)})

# 6
df_top_user.to_sql('top_user', engine, if_exists = 'replace', index=False,
                   dtype={'State': sqlalchemy.types.VARCHAR(length=50), 
                          'Year': sqlalchemy.types.Integer, 
                          'Quater': sqlalchemy.types.Integer,                           
                          'District_Pincode': sqlalchemy.types.Integer, 
                          'Registered_User': sqlalchemy.types.Integer,})
