# Importing Libraries
import pandas as pd
import mysql.connector as mysql
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from PIL import Image
import streamlit as st
from streamlit_player import st_player
from streamlit import components
import base64

icon = Image.open(r"D:\vk_project\phone_pe\phonepe-logo-icon.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Vinoth Kumar",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Vinoth Kumar*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})
mydb = mysql.connect(
  host = "localhost",
  user = "root",
  password = "vino8799",
  database = "phonepe_pulse"
)

# Create a new database and use
cursor = mydb.cursor()

SELECT = option_menu(
    menu_title=None,
    options=["About", "Basic insights", "Contact"],
    icons=["bar-chart", "toggles", "at"],
    default_index=2,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white", "size": "cover"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    }

)

if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--", "Top 10 states based on year and amount of transaction",
               "Least 10 states based on type and amount of transaction",
               "Top 10 mobile brands based on percentage of transaction",
               "Top 10 Registered-users based on States and District(pincode)",
               "Top 10 Districts based on states and amount of transaction",
               "Least 10 Districts based on states and amount of transaction",
               "Least 10 registered-users based on District_Pincode and states",
               "Top 10 transactions_type based on states and transaction_amount"]
    select = st.selectbox("Select the option", options)

    if select == "Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT State, Transaction_amount, Year, Quarter FROM top_transaction ORDER BY transaction_amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])

    # Display data table
        st.write("### Top 10 States based on Year and Amount of Transaction:")
        st.table(df)

    # Create and display bar chart
        st.write("### Visualization - Bar Chart:")
        fig = px.bar(df, x="State", y="Transaction_amount", title="Top 10 States based on Transaction Amount", labels={'Transaction_amount': 'Amount'})
        st.plotly_chart(fig, use_container_width=True)
        
    # Create and display line chart
        st.write("### Visualization - Line Chart:")
        fig_line = px.line(df, x="Year", y="Transaction_amount", color="State", title="Transaction Amount Over Years")
        st.plotly_chart(fig_line, use_container_width=True)    

    # Additional details or insights
        tap_1,tap_2=st.columns(2)
        with tap_1:
            st.write("### Additional Details:")
            st.write("- This chart represents the top 10 states based on transaction amount.")
            st.write("- Explore the data and gain insights into transaction patterns.")
            st.image("https://static.toiimg.com/thumb/imgsize-23456,msid-96002442,width-600,resizemode-4/96002442.jpg")
        
        with tap_2:
    # Additional Visualization - Pie Chart for Transaction Distribution
            st.write("### (Visualization) Pie Chart:")
            fig_pie = px.pie(df, names='State', values='Transaction_amount', title='Transaction Distribution in Top 10 States')
            st.plotly_chart(fig_pie, use_container_width=True)
    # Additional Details for Pie Chart
            st.write("### Pie Chart:")
            st.write("- Pie chart visualizing the distribution of transactions among the top 10 states.")
            st.write("- Gain insights into the contribution of each state to the total transaction amount.")
    #_______________________________________________________________________________________            
    elif select == "Least 10 states based on type and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State, Transaction_amount, Year, Quarter FROM top_transaction ORDER BY transaction_amount ASC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])
    
    # Visualization 1: Scatter Plot
        st.title("Least 10 states based on type and amount of transaction")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Data Frame:")
            st.write(df)

        with col2:
            st.subheader("Visualization 1: Scatter Plot")
            fig = px.scatter(df, x="State", y="Transaction_amount")
            st.plotly_chart(fig, use_container_width=True)
   
    # Visualization 2: Grouped Bar Chart
        st.title("Visualization 2: Grouped Bar Chart")
        groupby_column_options = [col for col in df.columns if col != 'Transaction_amount']
        groupby_column = st.selectbox("Select a column to group by:", groupby_column_options)
        grouped_df = df.groupby(groupby_column)['Transaction_amount'].sum().reset_index()
        fig_grouped = px.bar(grouped_df, x=groupby_column, y='Transaction_amount', title=f"Grouped by {groupby_column}")
        st.plotly_chart(fig_grouped, use_container_width=True)    

    #_______________________________________________________________________________________            

    elif select == "Top 10 mobile brands based on percentage of transaction":
        cursor.execute(
            "SELECT Brands, AVG(User_Percentage) as Avg_Percentage FROM aggregated_user GROUP BY Brands ORDER BY Avg_Percentage DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Avg_Percentage'])
    
# Visualization 1: Bar chart for average percentage by brand
        st.title("Top 10 mobile brands based on average percentage of transaction")
        fig1 = px.bar(df, x="Brands", y="Avg_Percentage", title="Average User Percentage by Brand")
        st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Line chart for PhonePe growth over time
        cursor.execute(
            "SELECT Year, SUM(User_Percentage) as Total_Percentage FROM aggregated_user GROUP BY Year;")
        phonepe_df = pd.DataFrame(cursor.fetchall(), columns=['Year', 'Total_Percentage'])

# Check the data retrieved
        st.write("PhonePe Data:")
        st.write(phonepe_df)

# Check if data is present
        if not phonepe_df.empty:
            st.title("PhonePe Growth Over Time")
            fig2 = px.line(phonepe_df, x="Year", y="Total_Percentage", title="PhonePe Growth Over Time")
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("No data available for PhonePe transactions grouped by year.")


# Visualization 3: Images or additional insights
        st.title("Additional Insights")
        
        tap1,tap2=st.columns(2)
        with tap1:
            st.image("https://img.freepik.com/free-vector/hand-drawn-installment-illustration_23-2149397096.jpg?size=626&ext=jpg", caption="Mobile Transactions")
        with tap2:
            # Additional Chart: Pie chart for distribution of transactions among top brands
            fig3 = px.pie(df, names='Brands', values='Avg_Percentage', title='Distribution of Transactions Among Top Brands')
            st.plotly_chart(fig3, use_container_width=True)
        
    #_______________________________________________________________________________________

    elif select == "Top 10 Registered-users based on States and District(pincode)":
        
        cursor.execute("""SELECT State, District_Pincode, SUM(Registered_User) as Total_Registered_Users FROM top_user GROUP BY State, District_Pincode ORDER BY State, Total_Registered_Users DESC LIMIT 10;""")
    
    # Fetch data and create a DataFrame
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District_Pincode', 'Total_Registered_Users'])

    # Visualization using groupby data
        st.title("Top 10 Registered-users based on States and District (Pincode)")
  
    # Bar chart for visualization
        fig = px.bar(df, x="State", y="Total_Registered_Users", color="District_Pincode",
                     
                     labels={'Total_Registered_Users': 'Registered Users'},
                     
                     title="Registered Users by State and District",
                     
                     height=500)

    # Display the chart
        st.plotly_chart(fig, use_container_width=True)

    # Display the DataFrame
        st.write(df)

    #_______________________________________________________________________________________
    elif select == "Top 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT State, District, Transaction_Amount FROM map_transaction ORDER BY Transaction_Amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])
        st.table(df)

    # Visualization with Plotly Express
        st.title("Top 10 Districts based on states and amount of transaction")
        
        fig_px = px.bar(df, x='State', y='Transaction_amount', title="Top 10 Districts based on states and amount of transaction ",
                        
                        labels={'Transaction_amount': 'Transaction Amount'})
        st.plotly_chart(fig_px, use_container_width=True)
    #_______________________________________________________________________________________
    elif select == "Least 10 Districts based on states and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State,District,Transaction_Amount FROM map_transaction ORDER BY Transaction_Amount ASC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on states and amount of transaction")
            fig = px.scatter(df, x="State", y="Transaction_amount")
            tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
            with tab1:
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab2:
                st.plotly_chart(fig, theme=None, use_container_width=True)
    #_______________________________________________________________________________________
    elif select == "Least 10 registered-users based on District_Pincode and states":
        cursor.execute(
            "SELECT DISTINCT State,District_Pincode,Registered_User FROM top_user ORDER BY Registered_User ASC LIMIT 10 ;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District_Pincode', 'Registered_User'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 registered-users based on Districts and states")
            fig = px.bar(df, x="State", y="Registered_User")
            tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
            with tab1:
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab2:
                st.plotly_chart(fig, theme=None, use_container_width=True)
    #_______________________________________________________________________________________
    elif select == "Top 10 transactions_type based on states and transaction_amount":
        cursor.execute(
            "SELECT DISTINCT State,Transacion_type,Transacion_amount FROM aggregated_transaction ORDER BY Transacion_amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transacion_type', 'Transacion_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 transactions_type based on states and transaction_amount")
            fig = px.bar(df, x="State", y="Transacion_amount")
            tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
            with tab1:
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab2:
                st.plotly_chart(fig, theme=None, use_container_width=True)
#_______________________________________________________________________________________
if SELECT == "Contact":
    name = " VINOTH KUMAR "
    mail = (f'{"Mail :"}  {"vinoharish8799@gmail.com"}')
    social_media = {"GITHUB": "https://github.com/vinothkumarpy",
                    'LINKED_IN' :'https://www.linkedin.com/in/vinoth-kumar-s-370724281/'}
    col1, col2 = st.columns(2)
    with col1:
        st.image('https://www.logo.wine/a/logo/PhonePe/PhonePe-Logo.wine.svg') 
        st.write(":red[download link:https://play.google.com/store/apps/details?id=com.phonepe.app&hl=en_IN&gl=US]")
    with col2:
        st.title(name)
        st.title(mail)
        st.subheader("An Aspiring DATA-ANALYST.... !")
    # st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")

if SELECT == "About":
    st.write("### :green[Welcome to the dashbord created by Vinoth kumar (Data Scientist)]")
    registered_users = 50_000_000
    monthly_transactions = 600_000_000
    daily_average_transactions = 20_000_000
    # Display Details
    st.title("Grow Your Business with PhonePe")
    st.subheader("We help you achieve your business goals.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Registered Users", f"{registered_users} Crore", ":busts_in_silhouette:")

    with col2:
        st.metric("Monthly Transactions", f"{monthly_transactions} Crore", ":credit_card:")

    with col3:
        st.metric("Daily Average Transactions", f"{daily_average_transactions} Crore", ":chart_with_upwards_trend:")
        
    
    col1,col2=st.columns(2)
    with col1:
        st.image("https://i.redd.it/f03x2x52dyo91.png", width=500)
    with col2:
        st_player(url = "https://www.youtube.com/watch?v=c_1H6vivsiA", height = 480)
        
             
    st.write(" ")
    st.write(" ")
    st.markdown("### :violet[PhonePe becomes the fastest to reach a million transactions a day:] ")
    st.write("##### Bengaluru, December 6th, 2017: PhonePe, Indias fastest growing digital payments platform, today announced two big milestones.The market leader in UPI-based merchant transactions processed over 1 million daily transactions, worth over 100 Crores every day in November.PhonePe has achieved a staggering Total Payments Volume (TPV) annual run rate of INR 40,000 Crore within 14 months of market launch. This is the fastest ramp up seen in Indias digital payments space to date. PhonePes monthly transactions have grown ""8200 %"" since November last year, fueled largely by exponential growth in its online merchant, bill payment and peer to peer transactions. The PhonePe mobile app has been downloaded by over 55 million Indians so far.")
    st.write("##### Sameer Nigam, Co-founder & CEO, PhonePe said, “We believe India is at the cusp of a major digital payments revolution, and PhonePe has been an important catalyst driving this change across the country. In line with the national agenda of Digital India, we are constantly innovating to bring more use cases to our platform and becoming the one-stop payments solution for all our customer needs. We are humbled to hit the million transactions a day milestone in such a short span of time. We are currently processing INR 40,000 Cr worth of digital payments annually, and are targeting to double this metric by March, 2018..")
    st.write("##### About PhonePe .PhonePe is a Flipkart company and the fastest growing digital payments platform in India. With over 55 million installs, the PhonePe App drives the maximum number of UPI transactions in India. Using PhonePe users can send and receive money, recharge mobile, DTH, datacards, make utility payments, pay their credit card bills and shop online and offline.for more details: media@phonepe.com")
