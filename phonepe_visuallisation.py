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
def setting_bg():
    st.markdown(f""" <style>.stApp {{
                        background: url("https://img.freepik.com/free-photo/vivid-blurred-colorful-wallpaper-background_58702-3979.jpg?size=626&ext=jpg");
                        background-size: cover}}
                     </style>""", unsafe_allow_html=True)

setting_bg()
                                 
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

# Add your additional styles here
st.markdown(
    """
    <style>
        .iconify {
            color: black;
            font-size: 20px;
        }
        .selectbox-container {
            padding: 0!important;
            background-color: white;
            size: cover;
        }
        .selectbox option {
            font-size: 20px;
            text-align: center;
            margin: -2px;
        }
        .selectbox option:checked {
            background-color: #6F36AD;
            color: white;
        }
        .selectbox option:hover {
            background-color: #6F36AD;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


if SELECT == "Basic insights":
    tab1,tab2 = st.tabs(["Insights", "Details"])

    with tab1:
        
        st.title("Insights")
        st.write("----")
        st.subheader("Let's know some basic insights about the data")
        options = ["--select--", "1.Top 10 states based on year and amount of transaction",
                   "2.Least 10 states based on type and amount of transaction",
                   "3.Top 10 mobile brands based on percentage of transaction",
                   "4.Top 50 Registered-users based on States and District(pincode)",
                   "5.Top 10 Districts based on states and amount of transaction",
                   "6.Least 10 Districts based on states and amount of transaction",
                   "7.Least 10 registered-users based on District_Pincode and states",
                   "8.Top 10 transactions_type based on states and transaction_amount"]
        select = st.selectbox("Select the option", options)


        if select == "1.Top 10 states based on year and amount of transaction":

            cursor.execute("SELECT DISTINCT State, Transaction_amount, Year, Quarter FROM top_transaction ORDER BY transaction_amount DESC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])

    # Display data table
            st.write("### Top 10 States based on Year and Amount of Transaction:")
            st.table(df)

    # Create and display bar chart
            
            fig = px.bar(df, x="State", y="Transaction_amount", title="Top 10 States based on Transaction Amount", labels={'Transaction_amount': 'Amount'})
            st.plotly_chart(fig, use_container_width=True)   

    # Additional details or insights
            tap_1,tap_2=st.columns(2)
            with tap_1:
                
                st.write("- This chart represents the top 10 states based on transaction amount.")
                st.write("- Explore the data and gain insights into transaction patterns.")
                st.image("https://static.toiimg.com/thumb/imgsize-23456,msid-96002442,width-600,resizemode-4/96002442.jpg")
        
            with tap_2:
    # Additional Visualization - Pie Chart for Transaction Distribution
              
                fig_pie = px.pie(df, names='State', values='Transaction_amount', title='Transaction Distribution in Top 10 States')
                st.plotly_chart(fig_pie, use_container_width=True)
    # Additional Details for Pie Chart
               
                st.write("- Pie chart visualizing the distribution of transactions among the top 10 states.")
                st.write("- Gain insights into the contribution of each state to the total transaction amount.")
    #_______________________________________________________________________________________            
        elif select == "2.Least 10 states based on type and amount of transaction":
            cursor.execute(
                "SELECT DISTINCT State, Transaction_amount, Year, Quarter FROM top_transaction ORDER BY transaction_amount ASC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])
    
    # Visualization 1: Scatter Plot
            st.title("Least 10 states based on type and amount of transaction")
            col1, col2 = st.columns(2)
            with col1:

                st.subheader("Details:")
                st.write(df)

            with col2:

                st.subheader("Transaction_amount based on state")
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

        elif select == "3.Top 10 mobile brands based on percentage of transaction":
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
            col1,col2=st.columns(2)

            with col1:
                st.write("Data:")
                st.write(phonepe_df)

            with col2:
                fig3 = px.pie(df, names='Brands', values='Avg_Percentage', title='Distribution of Transactions Among Top Brands')
                st.plotly_chart(fig3, use_container_width=True)

            # Check if data is present
            if not phonepe_df.empty:
                st.title("PhonePe Growth Over Time")
                fig2 = px.line(phonepe_df, x="Year", y="Total_Percentage", title="PhonePe Growth Over Time")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No data available for PhonePe transactions grouped by year.")



    #_______________________________________________________________________________________

        elif select == "4.Top 50 Registered-users based on States and District(pincode)":
            cursor.execute("""SELECT State, District_Pincode, SUM(Registered_User) as Total_Registered_Users FROM top_user GROUP BY State, District_Pincode ORDER BY State, Total_Registered_Users DESC LIMIT 50;""")
    
    # Fetch data and create a DataFrame
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District_Pincode', 'Total_Registered_Users'])

            st.write(df)


            # Visualization title
            st.title("Top 10 Registered-users based on States and District (Pincode)")

# Stylish bar chart using Plotly Express
            fig = px.bar(df, x="State", y="Total_Registered_Users", color="District_Pincode",
                         labels={'Total_Registered_Users': 'Registered Users'},
                         title="Registered Users by State and District",
                         height=500,
                         width=800,
                         template="plotly_dark",
                         )

# Add some additional styling to the chart
            fig.update_layout(
                xaxis_title="State",
                yaxis_title="Registered Users",
                legend_title="District (Pincode)",
                font=dict(family="Arial", size=12, color="white"),
                )

# Display the chart with custom styling
            st.plotly_chart(fig, use_container_width=True)
    #_______________________________________________________________________________________
        elif select == "5.Top 10 Districts based on states and amount of transaction":
            cursor.execute("SELECT DISTINCT State, District, Transaction_Amount FROM map_transaction ORDER BY Transaction_Amount DESC LIMIT 10;")
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])
            st.table(df)
            st.title("Top 10 Districts based on states and amount of transaction")
        
            fig_px = px.bar(df, x='State', y='Transaction_amount', title="Top 10 Districts based on states and amount of transaction ",
                            labels={'Transaction_amount': 'Transaction Amount'})
            st.plotly_chart(fig_px, use_container_width=True)
    #_______________________________________________________________________________________
        elif select == "6.Least 10 Districts based on states and amount of transaction":
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
        elif select == "7.Least 10 registered-users based on District_Pincode and states":
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
        elif select == "8.Top 10 transactions_type based on states and transaction_amount":
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


        with tab2:
            Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2022)
            Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
            Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
            col1, col2 = st.columns(2)

            # EXPLORE DATA - TRANSACTIONS
            if Type == "Transactions":
                    # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
            
                    st.markdown("## :violet[Overall State Data - Transactions Amount]")
                    cursor.execute(f"select State, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transaction where Year = {Year} and Quarter = {Quarter} group by state order by State")
                    df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
                    df2 = pd.read_csv(r'D:\vk_project\phone_pe\Statenames.csv')
                    df1.State = df2
                    
                    fig = px.choropleth(df1,
                                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                        featureidkey='properties.ST_NM',
                                        locations='State',
                                        color='Total_amount',
                                        color_continuous_scale='sunset')

                    fig.update_geos(fitbounds="locations", visible=False)
                    st.plotly_chart(fig, use_container_width=True)


                # BAR CHART - TOP PAYMENT TYPE
                    st.markdown("## :violet[Top Payment Type]")
                    cursor.execute(f"select Transacion_type, sum(Transacion_count) as Total_Transactions, sum(Transacion_amount) as Total_amount from aggregated_transaction where Year= {Year} and Quater = {Quarter} group by Transacion_type order by Transacion_type")
                    df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])

                    fig = px.bar(df,
                                 title='Transaction Types vs Total_Transactions',
                                 x="Transaction_type",
                                 y="Total_Transactions",
                                 orientation='v',
                                 color='Total_amount',
                                 color_continuous_scale=px.colors.sequential.Agsunset)
                    st.plotly_chart(fig, use_container_width=False)

                # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
                    st.markdown("# ")
                    st.markdown("# ")
                    st.markdown("# ")
                    st.markdown("## :violet[Select any State to explore more]")
                    selected_state = st.selectbox("",
                                                  ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                                   'bihar',
                                                   'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                                   'goa', 'gujarat', 'haryana',
                                                   'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                                   'ladakh', 'lakshadweep',
                                                   'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                                   'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                                   'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                                   'west-bengal'), index=30)

                    cursor.execute(f"select State, District,Year,Quarter, sum(Transaction_Count) as Total_Transactions, sum(Transaction_Amount) as Total_amount from map_transaction where Year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")

                    df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                                 'Total_Transactions', 'Total_amount'])
                    fig = px.bar(df1,
                                 title=selected_state,
                                 x="District",
                                 y="Total_Transactions",
                                 orientation='v',
                                 color='Total_amount',
                                 color_continuous_scale=px.colors.sequential.Agsunset)
                    st.plotly_chart(fig, use_container_width=True)

            # EXPLORE DATA - USERS
            if Type == "Users":

                # BAR CHART TOTAL UERS - DISTRICT WISE DATA
                st.markdown("## :violet[Select any State to explore more]")
                selected_state = st.selectbox("",
                                              ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                               'bihar',
                                               'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                               'goa', 'gujarat', 'haryana',
                                               'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                               'ladakh', 'lakshadweep',
                                               'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                               'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                               'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                               'west-bengal'), index=30)

                cursor.execute(f"select State,Year,Quarter,District,sum(Registered_User) as Total_Users, sum(District) as Total_District from map_user where year = {Year} and Quarter = {Quarter} and State = '{selected_state}' group by State, District,Year,Quarter order by State,District")

                df = pd.DataFrame(cursor.fetchall(),
                                  columns=['State', 'year', 'quarter', 'District', 'Total_Users', 'Total_District'])
                df.Total_Users = df.Total_Users.astype(int)

                fig = px.bar(df,
                             title=selected_state,
                             x="District",
                             y="Total_Users",
                             orientation='v',
                             color='Total_Users',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig, use_container_width=True)



#_______________________________________________________________________________________
if SELECT == "Contact":
    name = "**VINOTH KUMAR**"
    d_link = "https://play.google.com/store/apps/details?id=com.phonepe.app&hl=en_IN&gl=US"
    mail = f'Mail: **vinoharish8799@gmail.com**'
    social_media = {"GITHUB": "https://github.com/vinothkumarpy",
                    'LINKED_IN': 'https://www.linkedin.com/in/vinoth-kumar-s-370724281/'}
    
    col1, col2 = st.columns(2)
    
    with col1:
        # URL of the image
        image_url = 'https://media.licdn.com/dms/image/D5603AQEdUYVxth10vA/profile-displayphoto-shrink_200_200/0/1696432308722?e=1712188800&v=beta&t=XVFpGzex8677InWdrqvpg9Oetr3lgD7d9te4yQ9VFKU'

# Set a larger size for the image
        st.image(image_url, width=400)


    with col2:
        st.markdown(f"# {name}")
        st.subheader("An Aspiring Data_Analyst")
        st.markdown(mail)
        st.markdown("## Social Media")
        for platform, link in social_media.items():
            st.markdown(f"[{platform}]({link})")

#_______________________________________________________________________________________
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
