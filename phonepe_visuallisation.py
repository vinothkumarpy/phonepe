# Importing Libraries
import pandas as pd
import mysql.connector as mysql
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
import streamlit as st
from streamlit_player import st_player
import json as js
from streamlit_lottie import st_lottie
import requests
#--------------------------------------------------------------------------------------------------------------------------------------------------------------            

pd.set_option('display.max_columns', None)


icon = Image.open(r"D:\vk_project\phone_pe\phonepe-logo-icon.png")


st.set_page_config(page_title= "Phonepe Pulse Data Visualization | By Vinoth Kumar",
                   page_icon= icon,
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Vinoth Kumar*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})

#--------------------------------------------------------------------------------------------------------------------------------------------------------------            


def lottie(filepath):

    with open(filepath, 'r') as file:

        return js.load(file)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------            
                                 
mydb = mysql.connect(
    host = "localhost",
    user = "root",
    password = "vino8799",
    database = "phonepe_pulse"
    )

cursor = mydb.cursor()

#--------------------------------------------------------------------------------------------------------------------------------------------------------------            

selected = option_menu(
    menu_title="Phone-pe",
    options=['Home', 'About', 'Basic insights'],
    icons=['mic-fill', 'cash-stack', 'phone-flip', "at"],
    menu_icon='alexa',
    default_index=0,
)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------            

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

#--------------------------------------------------------------------------------------------------------------------------------------------------------------            


if selected == "Basic insights":

    option = option_menu(menu_title='', options=['Insights', 'Details'],
                         icons=['database-fill', 'list-task', 'person-circle', 'sign-turn-right-fill'],
                         default_index=0, orientation="horizontal")
    

    if option == "Insights":

        col1,col2=st.columns(2)

        with col1:

            file=lottie(r"D:\vk_project\lottiite animation\d1.json")
            st_lottie(file,height=300,key=None)


        with col2:

            st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Insight </span><span style='color: white;'> Analysis </h1>",unsafe_allow_html=True)
        

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

            st.write("### Top 10 States based on Year and Amount of Transaction:")

            st.table(df) 

            fig = px.bar(df, x="State", y="Transaction_amount", title="Top 10 States based on Transaction Amount", labels={'Transaction_amount': 'Amount'})
            st.plotly_chart(fig, use_container_width=True)   

            tap_1,tap_2=st.columns(2)

            with tap_1:
                
                st.write("- This chart represents the top 10 states based on transaction amount.")
                st.write("- Explore the data and gain insights into transaction patterns.")
                st.image("https://static.toiimg.com/thumb/imgsize-23456,msid-96002442,width-600,resizemode-4/96002442.jpg")
        
            with tap_2:
              
                fig_pie = px.pie(df, names='State', values='Transaction_amount', title='Transaction Distribution in Top 10 States')
                st.plotly_chart(fig_pie, use_container_width=True)

               
                st.write("- Pie chart visualizing the distribution of transactions among the top 10 states.")
                st.write("- Gain insights into the contribution of each state to the total transaction amount.")
#--------------------------------------------------------------------------------------------------------------------------------------------------------------            
        elif select == "2.Least 10 states based on type and amount of transaction":

            cursor.execute(
                "SELECT DISTINCT State, Transaction_amount, Year, Quarter FROM top_transaction ORDER BY transaction_amount ASC LIMIT 10;")
            
            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])
    
            st.title("Least 10 states based on type and amount of transaction")
            
            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Details:")
                st.write(df)

            with col2:

                st.subheader("Transaction_amount based on state")
                fig = px.scatter(df, x="State", y="Transaction_amount")
                st.plotly_chart(fig, use_container_width=True)

            st.title("Visualization 2: Grouped Bar Chart")

            groupby_column_options = [col for col in df.columns if col != 'Transaction_amount']
            groupby_column = st.selectbox("Select a column to group by:", groupby_column_options)
            grouped_df = df.groupby(groupby_column)['Transaction_amount'].sum().reset_index()
            fig_grouped = px.bar(grouped_df, x=groupby_column, y='Transaction_amount', title=f"Grouped by {groupby_column}")
            st.plotly_chart(fig_grouped, use_container_width=True)    

#--------------------------------------------------------------------------------------------------------------------------------------------------------------         

        elif select == "3.Top 10 mobile brands based on percentage of transaction":

            cursor.execute(
                "SELECT Brands, AVG(User_Percentage) as Avg_Percentage FROM aggregated_user GROUP BY Brands ORDER BY Avg_Percentage DESC LIMIT 10;")
            
            df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Avg_Percentage'])
    
            st.title("Top 10 mobile brands based on average percentage of transaction")
            fig1 = px.bar(df, x="Brands", y="Avg_Percentage", title="Average User Percentage by Brand")
            st.plotly_chart(fig1, use_container_width=True)


            cursor.execute(
                "SELECT Year, SUM(User_Percentage) as Total_Percentage FROM aggregated_user GROUP BY Year;")
            phonepe_df = pd.DataFrame(cursor.fetchall(), columns=['Year', 'Total_Percentage'])


            col1,col2=st.columns(2)

            with col1:

                st.write("Data:")
                st.write(phonepe_df)

            with col2:

                fig3 = px.pie(df, names='Brands', values='Avg_Percentage', title='Distribution of Transactions Among Top Brands')
                st.plotly_chart(fig3, use_container_width=True)

            if not phonepe_df.empty:

                st.title("PhonePe Growth Over Time")
                fig2 = px.line(phonepe_df, x="Year", y="Total_Percentage", title="PhonePe Growth Over Time")
                st.plotly_chart(fig2, use_container_width=True)

            else:
                st.warning("No data available for PhonePe transactions grouped by year.")

#--------------------------------------------------------------------------------------------------------------------------------------------------------------         

        elif select == "4.Top 50 Registered-users based on States and District(pincode)":

            cursor.execute("""SELECT State, District_Pincode, SUM(Registered_User) as Total_Registered_Users FROM top_user GROUP BY State, District_Pincode ORDER BY State, Total_Registered_Users DESC LIMIT 50;""")
    

            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District_Pincode', 'Total_Registered_Users'])

            st.write(df)
            
            st.title("Top 10 Registered-users based on States and District (Pincode)")

            fig = px.bar(df, x="State", y="Total_Registered_Users", color="District_Pincode",
                         labels={'Total_Registered_Users': 'Registered Users'},
                         title="Registered Users by State and District",
                         height=500,
                         width=800,
                         template="plotly_dark",
                         )

            fig.update_layout(
                xaxis_title="State",
                yaxis_title="Registered Users",
                legend_title="District (Pincode)",
                font=dict(family="Arial", size=12, color="white"),
                )

            st.plotly_chart(fig, use_container_width=True)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------  
        elif select == "5.Top 10 Districts based on states and amount of transaction":

            cursor.execute("SELECT DISTINCT State, District, Transaction_Amount FROM map_transaction ORDER BY Transaction_Amount DESC LIMIT 10;")

            df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])

            st.table(df)
            
            st.title("Top 10 Districts based on states and amount of transaction")

            fig_px = px.bar(df, x='State', y='Transaction_amount', title="Top 10 Districts based on states and amount of transaction ",
                            labels={'Transaction_amount': 'Transaction Amount'})
            
            st.plotly_chart(fig_px, use_container_width=True)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------         
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
#--------------------------------------------------------------------------------------------------------------------------------------------------------------         
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
#--------------------------------------------------------------------------------------------------------------------------------------------------------------         
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

#--------------------------------------------------------------------------------------------------------------------------------------------------------------         

    if option == "Details":

        col1,col2=st.columns(2)

        with col1:

            file=lottie(r"D:\vk_project\lottiite animation\dash2.json")
            st_lottie(file,height=400,key=None)

        with col2:

            st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Detailed </span><span style='color: white;'> Analysis </h1>",unsafe_allow_html=True)
            st.markdown("<span style='font-size:30px; font-weight:bold;'>Transactions and users</span>", unsafe_allow_html=True)
        
        st.write("")

        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

        option = option_menu(menu_title='', options=['Transactions', 'Users'],
                             icons=['database-fill', 'list-task'],
                             default_index=0, orientation="horizontal")

        if option == "Transactions":
            
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

        if option == "Users":

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

#--------------------------------------------------------------------------------------------------------------------------------------------------------------         
if selected == 'Home':

    def load_lottieurl(url):

        r = requests.get(url)

        if r.status_code != 200:

            return None
        
        return r.json()

   
    def local_css(file_name):

        with open(file_name) as f:

            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css(r"D:\vk_project\phone_pe\style.css")

    lottie_coding = lottie(r"D:\vk_project\lottiite animation\intro vk.json")

    with st.container():

        col1,col2=st.columns(2)

        with col1:

            st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Hi,  </span><span style='color: white;'> I am vinoth kumar </h1>",unsafe_allow_html=True)
            
            st.markdown(
                f"<h1 style='font-size: 40px;'><span style='color: white;'>A Data Scientist,</span><span style='color: #00BFFF;'> From India</span></h1>",
                unsafe_allow_html=True
                )
            
            st.write(f'<h1 style="color:#B0C4DE; font-size: 20px;">A data scientist skilled in extracting actionable insights from complex datasets, adept at employing advanced analytics and machine learning techniques to solve real-world problems. Proficient in Python, statistical modeling, and data visualization, with a strong commitment to driving data-driven decision-making.</h1>', unsafe_allow_html=True)    
            
            c1,c2=st.columns(2)
            
            with c1:

                st.markdown("[view more projects >](https://github.com/vinothkumarpy?tab=repositories)")
                st.markdown('[mail](vinoharish8799@gmail.com)')
            
            with c2:

                st.markdown('[GITHUB](https://github.com/vinothkumarpy)')
                st.markdown('[LINKED_IN](https://www.linkedin.com/in/vinoth-kumar-s-370724281/)')
         
        with col2:

            st_lottie(lottie_coding, height=400, key="coding")    

    with st.container():

        st.write("---")

        st.write("---")

        col1,col2,col3=st.columns(3)

        with col1:

            file = lottie(r"D:\vk_project\lottiite animation\working with data set.json")
            st_lottie(file,height=500,key=None) 
        
        with col2:

            st.markdown( f"<h1 style='font-size: 70px;text-align: center;'><span style='color: #00BFFF;'> WHAT  </span><span style='color: white;'> I DO </h1>",unsafe_allow_html=True)
        
        with col3:

            file=lottie(r'D:\vk_project\phone_pe\payment.json')
            st_lottie(file,height=500,key=None)
            
        #1
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'>Data  </span><span style='color: white;'>Extract</h1>",unsafe_allow_html=True)
        st.markdown('<h1 style="color:#B0C4DE; font-size: 30px;">Initially, we clone the data from the Phonepe GitHub repository by using Python libraries. <a href="https://github.com/PhonePe/pulse.git" target="_blank">https://github.com/PhonePe/pulse.git</a></h1>', unsafe_allow_html=True)
        
        #2
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Process and  </span><span style='color: white;'>Transform the data</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Process the clone data by using Python algorithms and transform the processed data into DataFrame formate.</h1>', unsafe_allow_html=True) 
        
        #3
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Load  </span><span style='color: white;'>Data</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Finally, create a connection to the MySQL server and create a Database and stored the Transformed data in the MySQL server by using the given method.</h1>', unsafe_allow_html=True)
        
        #4
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> E D A   </span><span style='color: white;'>Preprocessing</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Create a connection to the MySQL server and access the specified MySQL DataBase by using (MYSQL Python Client) library.</h1>', unsafe_allow_html=True)
        
        #5
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Filter the Data  </span><span style='color: white;'> & Visualization</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Filter and process the collected data depending on the given requirements by using SQL queries and Finally, create a Dashboard by using Streamlit and applying selection and dropdown options on the Dashboard and show the output are Geo visualization, bar chart, and Dataframe Table.</h1>', unsafe_allow_html=True)   
        
        #6
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Interactive  </span><span style='color: white;'>Streamlit UI</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Crafted an engaging and user-friendly interface for seamless data exploration and presentation.</h1>', unsafe_allow_html=True)
        
        #7
        st.markdown("[🔗 GitHub Repo >](https://github.com/vinothkumarpy/phonepe.git)")    



    with st.container():

        st.write("---")

        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Used-Tech  </span><span style='color: white;'>& Skills</h1>",unsafe_allow_html=True)

        col1,col2,col3 =st.columns(3)

        with col1:

            file = lottie(r"D:\vk_project\lottiite animation\python.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>python</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"D:\vk_project\lottiite animation\Data cleaning.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data Cleaning</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)


            file = lottie(r"D:\vk_project\lottiite animation\database.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>DataBase</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

        with col2:

            file = lottie(r"D:\vk_project\phone_pe\git.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Git</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)


            file = lottie(r"D:\vk_project\lottiite animation\analyis.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data visualization</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"D:\vk_project\lottiite animation\frame work.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Web application development with Streamlit</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

        with col3:    

            file = lottie(r"D:\vk_project\lottiite animation\data collection.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data Collection</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)


            file = lottie(r"D:\vk_project\lottiite animation\data_exploaration.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data Exploaration</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)
       

    with st.container():

        st.write("---")

        st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> About  </span><span style='color: white;'> Projects </h1>",unsafe_allow_html=True)
        
        col1,col2=st.columns(2)
        
        with col1:

            file = lottie(r"D:\vk_project\phone_pe\payment sucess 2.json")
            st_lottie(file,height=300,key=None)

        with col2:

            st.write("##")
           
            st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">This project aims to create an interactive data visualization tool for the Phonepe Pulse data available on GitHub. The tool provides user-friendly access to various Datas and Details.</h1>', unsafe_allow_html=True)
        
        st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Re</span><span style='color: white;'>sults</h1>",unsafe_allow_html=True)
        
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">This project delivers a user-friendly geo-visualization dashboard for exploring Phonepe Pulse data. Users can access and interact with various data visualizations through a web browser, gaining valuable insights from the Phonepe Pulse GitHub repository.</h1>', unsafe_allow_html=True)    
        


    with st.container():

        st.write("---")
        
        st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Get In Touch  </span><span style='color: white;'> With Me </h1>",unsafe_allow_html=True)
       
        st.write("##")

        
        contact_form = """
        <form action="https://formsubmit.co/vinoharish8799@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit" style="background-color: #00BFFF; color: white;">Send</button>
        </form>
        """
        
        left_column, right_column = st.columns(2)
        
        with left_column:

            st.markdown(contact_form, unsafe_allow_html=True)
        
        with right_column:

            st.empty()    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------         

if selected == "About":

    registered_users = 50_000_000
    monthly_transactions = 600_000_000
    daily_average_transactions = 20_000_000

    st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'>Grow Your Business</span><span style='color: white;'> with PhonePe </h1>",unsafe_allow_html=True)

    st.markdown( f"<h1 style='font-size: 40px;'><span style='color: white ;'>We help you achieve</span><span style='color: #00BFFF;'> your business goals </h1>",unsafe_allow_html=True)

    with st.container():

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric("Registered Users", f"{registered_users} Crore", ":busts_in_silhouette")

        with col2:

            st.metric("Monthly Transactions", f"{monthly_transactions} Crore", ":credit_card")

        with col3:

            st.metric("Daily Average Transactions", f"{daily_average_transactions} Crore", ":chart_with_upwards_trend")
        
    with st.container():

        st.write('---')

        col1,col2=st.columns(2)

        with col1:
        
            st.image("https://i.redd.it/f03x2x52dyo91.png", width=700)
        
        with col2:

            st_player(url = "https://www.youtube.com/watch?v=c_1H6vivsiA", height = 480)
            
        with st.container(): 

            st.write("---")

            st.markdown("### :violet[PhonePe becomes the fastest to reach a million transactions a day:] ")

            st.write("##### Bengaluru, December 6th, 2017: PhonePe, Indias fastest growing digital payments platform, today announced two big milestones.The market leader in UPI-based merchant transactions processed over 1 million daily transactions, worth over 100 Crores every day in November.PhonePe has achieved a staggering Total Payments Volume (TPV) annual run rate of INR 40,000 Crore within 14 months of market launch. This is the fastest ramp up seen in Indias digital payments space to date. PhonePes monthly transactions have grown ""8200 %"" since November last year, fueled largely by exponential growth in its online merchant, bill payment and peer to peer transactions. The PhonePe mobile app has been downloaded by over 55 million Indians so far.")
            
            st.write("##### Sameer Nigam, Co-founder & CEO, PhonePe said, “We believe India is at the cusp of a major digital payments revolution, and PhonePe has been an important catalyst driving this change across the country. In line with the national agenda of Digital India, we are constantly innovating to bring more use cases to our platform and becoming the one-stop payments solution for all our customer needs. We are humbled to hit the million transactions a day milestone in such a short span of time. We are currently processing INR 40,000 Cr worth of digital payments annually, and are targeting to double this metric by March, 2018..")
            
            st.write("##### About PhonePe .PhonePe is a Flipkart company and the fastest growing digital payments platform in India. With over 55 million installs, the PhonePe App drives the maximum number of UPI transactions in India. Using PhonePe users can send and receive money, recharge mobile, DTH, datacards, make utility payments, pay their credit card bills and shop online and offline.for more details: media@phonepe.com")
