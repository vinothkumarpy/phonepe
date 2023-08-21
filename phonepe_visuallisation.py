import mysql.connector
import pandas as pd

import streamlit as st
import PIL
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import requests

#connect to the database

import mysql.connector

mydb = mysql.connector.connect(
  host = "localhost",
  user = "root",
  password = "vino8799",
  database = "phonepe_pulse__"
)

cursor=mydb.cursor()

SELECT = option_menu(
    menu_title=None,
    options=['About' , 'Home' , 'Basic insights' ],
    icons=['bar_chart' , 'house' , 'toggles' , 'at'],
    default_index=2,
    orientation='Horizontal',
    styles={'Container':{'padding': '0!important' , 'background-colour' : 'black' , 'size' : 'cover','width' : '100%' },
            'icon' : {'colour' : 'white' , 'font-size' : '20px'},
            'navi-link': {'font-size' : '20px', 'text-align' : 'center' , 'margin' : '-2px' , '--hover-color' : '#6F3AD'},
            'nav-link-selected':{'background-color':'#6F36AD'}})



#---------------------Basic Insights -----------------#


if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("-----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on type and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and Count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_Count based on Districts and states",
               "Top 10 RegisteredUsers based on states and District"]
    
               #1
               
    select = st.selectbox("Select the option",options)
    if select=="Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT State, Year, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY State, Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        
        df = pd.DataFrame(cursor.fetchall(), columns=['State','Year', 'Transaction_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 states and amount of transaction")
            st.bar_chart(data=df,x="Transaction_amount",y="State")
            
            #2
            
    elif select=="List 10 states based on type and amount of transaction":
        cursor.execute("SELECT DISTINCT State, SUM(Transaction_count) as Total FROM top_transaction GROUP BY State ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','Total_Transaction'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("List 10 states based on type and amount of transaction")
            st.bar_chart(data=df,x="Total_Transaction",y="State")
            
            #3
            
    elif select == "Top 5 Transaction_Type based on Transaction_Amount":
        cursor.execute("SELECT DISTINCT Transacion_type, SUM(Transacion_amount) AS Amount FROM aggregated_transaction GROUP BY Transacion_type ORDER BY Amount DESC LIMIT 5")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transacion_type', 'Transacion_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 5 Transaction_Type based on Transaction_Amount")
            st.bar_chart(data=df, y="Transacion_type", x="Transacion_amount")

            #4
            
    elif select=="Top 10 Registered-users based on States and District":
        cursor.execute("SELECT DISTINCT State, District_Pincode, SUM(Registered_User) AS Users FROM top_user GROUP BY State, District_Pincode ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District_Pincode','Registered_User'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Registered-users based on States and District")
            st.bar_chart(data=df,y="State",x="Registered_User")
            
            #5
            
    elif select=="Top 10 Districts based on states and Count of transaction":
        cursor.execute("SELECT DISTINCT State,District,SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY State,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on states and Count of transaction")
            st.bar_chart(data=df,y="State",x="Transaction_Count")
            
            #6
            
    elif select=="List 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT State,year,SUM(Transacion_amount) AS Amount FROM aggregated_transaction GROUP BY State, year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','year','Transacion_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df,y="State",x="Transacion_amount")
            
            #7
            
    elif select=="List 10 Transaction_Count based on Districts and states":
        cursor.execute("SELECT DISTINCT State, District, SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY State,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Transaction_Count'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("List 10 Transaction_Count based on Districts and states")
            st.bar_chart(data=df,y="State",x="Transaction_Count")
            
            #8
             
    elif select=="Top 10 RegisteredUsers based on states and District":
        cursor.execute("SELECT DISTINCT State,District, SUM(Registered_User) AS Users FROM map_user GROUP BY State,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['State','District','Registered_User'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 RegisteredUsers based on states and District")
            st.bar_chart(data=df,y="State",x="Registered_User")


#----------------Home----------------------#
cursor = mydb.cursor()

# execute a SELECT statement
cursor.execute("SELECT * FROM aggregated_transaction")

# fetch all rows
rows = cursor.fetchall()
from streamlit_extras.add_vertical_space import add_vertical_space

if SELECT == "Home":
    col1,col2, = st.columns(2)
    col1.image(Image.open(r"D:\vs_code\images.jpg"),width = 400)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video(r"D:\vs_code\A speedy selfie to the rescue_(720P_HD).mp4")
        

#----------------About-----------------------#

if SELECT == "About":
    col1,col2 = st.columns(2)
    with col1:
        st.video(r"D:\vs_code\A speedy selfie to the rescue_(720P_HD).mp4")
    with col2:
        st.image(Image.open(r"D:\vs_code\images.jpg"),width = 500)
        st.write("---")
        st.subheader("The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and states-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.")
    st.write("---")
    col1,col2 = st.columns(2)
    with col1:
        st.title("THE BEAT OF PHONEPE")
        st.write("---")
        st.subheader("Phonepe became a one of the trending digital payments company")
        st.image(Image.open(r'D:\vs_code\phone_pe.webp'),width = 400)
        with open(r"D:\vs_code\PhonePe_Pulse_BCG_report.pdf","rb") as f:
            data = f.read()
        st.download_button("DOWNLOAD REPORT",data,file_name="annual report.pdf")
    with col2:
        st.image(Image.open(r"D:\vs_code\phone_pe.webp"),width = 800)


#----------------------Contact---------------#







        # MENU 4 - ABOUT
if SELECT == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[My Project GitHub link]** ⬇️")
        st.write("https://github.com/vinothkumarpy/phonepe")
        st.write("**:violet[Image and content source]** ⬇️")
        st.write("https://www.businesstoday.in/latest/corporate/story/phonepe-launches-interactive-geospatial-site-pulse-305744-2021-09-02")

        


