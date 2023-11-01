
# ==================================================     /    IMPORT LIBRARY    /    ======================================================== #

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
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
import git

# [Dash board libraries]
import streamlit as st
import plotly.express as px



#  =============     CONNECT SQL SERVER  /   CREAT DATA BASE    /  CREAT TABLE    /    STORE DATA    ========  #


# CONNECTING WITH MYSQL DATABASE
# mydb = mysql.connector.connect(host="localhost",port = 3306, user="root",password="alohomora25", auth_plugin = 'mysql_native_password')

# ==============   /  CONNECT SQL SERVER  /   ACCESS DATA BASE    /   EXECUTE SQL QUERIES      /    ACCESS DATA   /   ========================= #
import pymysql

conn = pymysql.connectpymysql.connect(
    host='mydb.cxxgnqrk2rjc.us-east-1.rds.amazonaws.com',
    user= 'admin',
    password='Alohomora25',
    database = 'phonepe_db'
)
cursor = conn.cursor()

# # ============================================       /     STREAMLIT DASHBOARD      /       ================================================= #
#
# Comfiguring Streamlit GUI
st.set_page_config(layout='wide')

# Title
st.header('Phonepe Pulse')
st.write('All PhonePe transactions (UPI + Cards + Wallets) from **2018** to **2022** in **INDIA**')

# Selection option
option = st.radio('**Select your option**', ('All India', 'State wise', 'Top Ten categories', 'Time Series'), horizontal=True)

# ===================================================       /      All India      /     ===================================================== #

if option == 'All India':

    # Select tab
    tab1, tab2 = st.tabs(['Transaction', 'User'])

    # -------------------------       /     All India Transaction        /        ------------------ #
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            in_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_yr')
        with col2:
            in_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_qtr')
        with col3:
            in_typ = st.selectbox('**Select Transaction type**',
                                        ('Recharge & bill payments', 'Peer-to-peer payments',
                                         'Merchant payments', 'Financial Services', 'Others'), key='in_typ')

        # SQL Query

        # Transaction Analysis bar chart query
        cursor.execute(
            f"SELECT State, Transaction_amount FROM aggregated_transaction WHERE Year = '{in_yr}' AND Quarter = '{in_qtr}' AND Transaction_type = '{in_typ}';")
        in_transaction = cursor.fetchall()
        df_transaction_result = pd.DataFrame(np.array(in_transaction), columns=['State', 'Transaction_amount'])
        df_transaction_result_qry = df_transaction_result.set_index(pd.Index(range(1, len(df_transaction_result) + 1)))

        # Transaction Analysis table query
        cursor.execute(
            f"SELECT State, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Year = '{in_yr}' AND Quarter = '{in_qtr}' AND Transaction_type = '{in_typ}';")
        in_table = cursor.fetchall()
        df_table = pd.DataFrame(np.array(in_table),
                                                  columns=['State', 'Transaction_count', 'Transaction_amount'])
        df_table_qry = df_table.set_index(
            pd.Index(range(1, len(df_table) + 1)))

        # Total Transaction Amount table query
        cursor.execute(
            f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE Year = '{in_yr}' AND Quarter = '{in_qtr}' AND Transaction_type = '{in_typ}';")
        in_amount = cursor.fetchall()
        df_amount = pd.DataFrame(np.array(in_amount), columns=['Total', 'Average'])
        df_amount_qry = df_amount.set_index(['Average'])

        # Total Transaction Count table query
        cursor.execute(
            f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Year = '{in_yr}' AND Quarter = '{in_qtr}' AND Transaction_type = '{in_typ}';")
        in_count = cursor.fetchall()
        df_count = pd.DataFrame(np.array(in_count), columns=['Total', 'Average'])
        df_count_qry = df_count.set_index(['Average'])

        # --------- / Output  /  -------- #

        # ------    /  Geo visualization dashboard for Transaction /   ---- #
        # Drop a State column
        df_transaction_result.drop(columns=['State'], inplace=True)
        # Clone the gio data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
        state_names_tra.sort()
        # Create a DataFrame with the state names column
        df_state_names_tra = pd.DataFrame({'State': state_names_tra})
        # Combine the Gio State name
        df_state_names_tra['Transaction_amount'] = df_transaction_result
        # convert dataframe to csv file
        df_state_names_tra.to_csv('State_trans.csv', index=False)
        # Read csv
        df_tra = pd.read_csv('State_trans.csv')

        # Geo plot

        fig_tra = px.choropleth(
            df_tra,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM', locations='State', color='Transaction_amount',
            color_continuous_scale='thermal', title='Transaction Analysis - Map')
        fig_tra.update_geos(fitbounds="locations", visible=False)
        fig_tra.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=800)
    
        st.plotly_chart(fig_tra, use_container_width=True)

        # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
        df_transaction_result_qry['State'] = df_transaction_result_qry['State'].astype(str)
        df_transaction_result_qry['Transaction_amount'] = df_transaction_result_qry['Transaction_amount'].astype(float)
        df_transaction_result_fig = px.bar(df_transaction_result_qry, x='State', y='Transaction_amount',
                                            color='Transaction_amount', color_continuous_scale='thermal',
                                            title='Transaction Analysis', height=700, )
        df_transaction_result_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_transaction_result_fig, use_container_width=True)

        # -------  /  All India Total Transaction calculation Table   /   ----  #
        st.header(':white[Summary Tables]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader('Transaction Summmary Table')
            st.dataframe(df_table_qry)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_amount_qry)
            st.subheader('Transaction Count')
            st.dataframe(df_count_qry)

    # ---------------------------------------       /     All India User        /        ------------------------------------ #
    with tab2:

        col1, col2 = st.columns(2)
        with col1:
            in_user_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='in_user_yr')
        with col2:
            in_user_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='in_user_qtr')

        # SQL Query

        # User Analysis Bar chart query
        cursor.execute(
            f"SELECT State, SUM(User_Count) FROM aggregated_user WHERE Year = '{in_user_yr}' AND Quarter = '{in_user_qtr}' GROUP BY State;")
        in_user = cursor.fetchall()
        df_user = pd.DataFrame(np.array(in_user), columns=['State', 'User Count'])
        df_user_qry = df_user.set_index(pd.Index(range(1, len(df_user) + 1)))

        # Total User Count table query
        cursor.execute(
            f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_user WHERE Year = '{in_user_yr}' AND Quarter = '{in_user_qtr}';")
        in_user_count = cursor.fetchall()
        df_user_count = pd.DataFrame(np.array(in_user_count), columns=['Total', 'Average'])
        df_user_count_qry = df_user_count.set_index(['Average'])

        # ---------  /  Output  /  -------- #

        # ------    /  Geo visualization dashboard for User  /   ---- #
        # Drop a State column
        df_user.drop(columns=['State'], inplace=True)
        # Clone the gio data
        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data2 = json.loads(response.content)
        # Extract state names and sort them in alphabetical order
        state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
        state_names_use.sort()
        # Create a DataFrame with the state names column
        df_state_names_use = pd.DataFrame({'State': state_names_use})
        # Combine the Gio State name
        df_state_names_use['User Count'] = df_user
        # convert dataframe to csv file
        df_state_names_use.to_csv('State_user.csv', index=False)
        # Read csv
        df_use = pd.read_csv('State_user.csv')
        # Geo plot
        fig_use = px.choropleth(
            df_use,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM', locations='State', color='User Count', color_continuous_scale='thermal',
            title='User Analysis')
        fig_use.update_geos(fitbounds="locations", visible=False)
        fig_use.update_layout(title_font=dict(size=33), title_font_color='#6739b7', height=800)
        st.plotly_chart(fig_use, use_container_width=True)

        # ----   /   All India User Analysis Bar chart   /     -------- #
        df_user_qry['State'] = df_user_qry['State'].astype(str)
        df_user_qry['User Count'] = df_user_qry['User Count'].astype(int)
        df_user_qry_fig = px.bar(df_user_qry, x='State', y='User Count', color='User Count',
                                            color_continuous_scale='thermal', title='User Analysis', height=700, )
        df_user_qry_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_user_qry_fig, use_container_width=True)

        # -----   /   All India Total User calculation Table   /   ----- #
        st.header(':white[Summary Table]')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('Summary of Summary Count')
            st.dataframe(df_user_qry)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_user_count_qry)



# ==============================================          /     State wise       /             ============================================== #
elif option == 'State wise':

    # Select tab
    tab3, tab4 = st.tabs(['Transaction', 'User'])

    # ---------------------------------       /     State wise Transaction        /        ------------------------------- #
    with tab3:

        col1, col2, col3 = st.columns(3)
        with col1:
            st_tr_st = st.selectbox('**Select State**', (
            'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
            'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
            'himachal-pradesh',
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
            'maharashtra', 'manipur',
            'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu',
            'telangana',
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), key='st_tr_st')
        with col2:
            st_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_tr_yr')
        with col3:
            st_tr_qtr = st.selectbox('**Select Quarter**', ('1', '2', '3', '4'), key='st_tr_qtr')

        # SQL Query

        # Transaction Analysis bar chart query
        cursor.execute(
            f"SELECT Transaction_type, Transaction_amount FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_transaction = cursor.fetchall()
        df_st_transaction = pd.DataFrame(np.array(st_transaction),
                                                 columns=['Transaction_type', 'Transaction_amount'])
        df_st_transaction_qry = df_st_transaction.set_index(
            pd.Index(range(1, len(st_transaction) + 1)))

        # Transaction Analysis table query
        cursor.execute(
            f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_analysis_table = cursor.fetchall()
        df_st_analysis_table = pd.DataFrame(np.array(st_analysis_table),
                                                  columns=['Transaction_type', 'Transaction_count',
                                                           'Transaction_amount'])
        df_st_analysis_table_qry = df_st_analysis_table.set_index(
            pd.Index(range(1, len(df_st_analysis_table) + 1)))

        # Total Transaction Amount table query
        cursor.execute(
            f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year = '{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_amount = cursor.fetchall()
        df_st_amount = pd.DataFrame(np.array(st_amount), columns=['Total', 'Average'])
        df_st_amount_qry = df_st_amount.set_index(['Average'])

        # Total Transaction Count table query
        cursor.execute(
            f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE State = '{st_tr_st}' AND Year ='{st_tr_yr}' AND Quarter = '{st_tr_qtr}';")
        st_count = cursor.fetchall()
        df_st_count = pd.DataFrame(np.array(st_count), columns=['Total', 'Average'])
        df_st_count_qry = df_st_count.set_index(['Average'])

        # ---------  /  Output  /  -------- #

        # -----    /   State wise Transaction Analysis bar chart   /   ------ #
        df_st_transaction_qry['Transaction_type'] = df_st_transaction_qry['Transaction_type'].astype(str)
        df_st_transaction_qry['Transaction_amount'] = df_st_transaction_qry['Transaction_amount'].astype(
            float)
        df_st_transaction_qry_fig = px.bar(df_st_transaction_qry, x='Transaction_type',
                                                y='Transaction_amount', color='Transaction_amount',
                                                color_continuous_scale='thermal', title='Transaction Analysis By State',
                                                height=500, )
        df_st_transaction_qry_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_st_transaction_qry_fig, use_container_width=True)

        # ------  /  State wise Total Transaction calculation Table  /  ---- #
        st.header(':white[Summary Tables]')

        col4, col5 = st.columns(2)
        with col4:
            st.subheader(' Summary of Transaction')
            st.dataframe(df_st_analysis_table_qry)
        with col5:
            st.subheader('Transaction Amount')
            st.dataframe(df_st_amount_qry)
            st.subheader('Transaction Count')
            st.dataframe(df_st_count_qry)

    # -----------------------------------------       /     State wise User        /        ---------------------------------- #
    with tab4:

        col5, col6 = st.columns(2)
        with col5:
            st_us_st = st.selectbox('**Select State**', (
            'andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
            'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana',
            'himachal-pradesh',
            'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
            'maharashtra', 'manipur',
            'meghalaya', 'mizoram', 'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu',
            'telangana',
            'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'), key='st_us_st')
        with col6:
            st_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='st_us_yr')

        # SQL Query

        # User Analysis Bar chart query
        cursor.execute(
            f"SELECT Quarter, SUM(User_Count) FROM aggregated_user WHERE State = '{st_us_st}' AND Year = '{st_us_yr}' GROUP BY Quarter;")
        st_us_tab = cursor.fetchall()
        df_st_us_tab = pd.DataFrame(np.array(st_us_tab), columns=['Quarter', 'User Count'])
        df_st_us_tab_qry = df_st_us_tab.set_index(pd.Index(range(1, len(df_st_us_tab) + 1)))

        # Total User Count table query
        cursor.execute(
            f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_user WHERE State = '{st_us_st}' AND Year = '{st_us_yr}';")
        st_us_count = cursor.fetchall()
        df_st_us_count = pd.DataFrame(np.array(st_us_count), columns=['Total', 'Average'])
        df_st_us_count_qry = df_st_us_count.set_index(['Average'])

        # ---------  /  Output  /  -------- #

        # -----   /   All India User Analysis Bar chart   /   ----- #
        df_st_us_tab_qry['Quarter'] = df_st_us_tab_qry['Quarter'].astype(int)
        df_st_us_tab_qry['User Count'] = df_st_us_tab_qry['User Count'].astype(int)
        df_st_us_tab_qry_fig = px.bar(df_st_us_tab_qry, x='Quarter', y='User Count', color='User Count',
                                            color_continuous_scale='thermal', title='User Analysis', height=500, )
        df_st_us_tab_qry_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_st_us_tab_qry_fig, use_container_width=True)

        # ------    /   State wise User Total User calculation Table   /   -----#
        st.header(':white[Summary Tables]')

        col3, col4 = st.columns(2)
        with col3:
            st.subheader('Summary of Users')
            st.dataframe(df_st_us_tab_qry)
        with col4:
            st.subheader('User Count')
            st.dataframe(df_st_us_count_qry)



# ==============================================          /     Top categories       /             =========================================== #
if option == 'Top Ten categories':

    # Select tab
    tab5, tab6 = st.tabs(['Transaction', 'User'])

    # ---------------------------------------       /     All India Top Transaction        /        ---------------------------- #
    with tab5:
        top_tr_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='top_tr_yr')

        # SQL Query

        # Top Transaction Analysis bar chart query
        cursor.execute(
            f"SELECT State, SUM(Transaction_amount) As Transaction_amount FROM top_transaction WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
        top_transaction = cursor.fetchall()
        df_top_tran = pd.DataFrame(np.array(top_transaction),
                                              columns=['State', 'Top Transaction amount'])
        df_top_tr_qry = df_top_tran.set_index(pd.Index(range(1, len(df_top_tran) + 1)))

        # Top Transaction Analysis table query
        cursor.execute(
            f"SELECT State, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transaction WHERE Year = '{top_tr_yr}' GROUP BY State ORDER BY Transaction_amount DESC LIMIT 10;")
        top_analysis = cursor.fetchall()
        df_top_anly = pd.DataFrame(np.array(top_analysis),
                                                   columns=['State', 'Top Transaction amount',
                                                            'Total Transaction count'])
        df_top_anly_qry = df_top_anly.set_index(
            pd.Index(range(1, len(df_top_anly) + 1)))

        # ---------  /  Output  /  -------- #

        # -----   /   All India Transaction Analysis Bar chart   /   ----- #
        df_top_tr_qry['State'] = df_top_tr_qry['State'].astype(str)
        df_top_tr_qry['Top Transaction amount'] = df_top_tr_qry['Top Transaction amount'].astype(
            float)
        df_top_tr_qry_fig = px.bar(df_top_tr_qry, x='State', y='Top Transaction amount',
                                             color='Top Transaction amount', color_continuous_scale='thermal',
                                             title='Top Transaction Analysis', height=600, )
        df_top_tr_qry_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_top_tr_qry_fig, use_container_width=True)

        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':white[Summary]')
        st.subheader('Top Transaction Analysis')
        st.dataframe(df_top_tr_qry)

    # -------------------------       /     All India Top User        /        ------------------ #
    with tab6:
        top_us_yr = st.selectbox('**Select Year**', ('2018', '2019', '2020', '2021', '2022'), key='top_us_yr')

        # SQL Query

        # Top User Analysis bar chart query
        cursor.execute(
            f"SELECT State, SUM(Registered_User) AS Top_user FROM top_user WHERE Year='{top_us_yr}' GROUP BY State ORDER BY Top_user DESC LIMIT 10;")
        top_user_tab = cursor.fetchall()
        df_top_user_tab = pd.DataFrame(np.array(top_user_tab), columns=['State', 'Total User count'])
        df_top_user_tab_qry = df_top_user_tab.set_index(pd.Index(range(1, len(df_top_user_tab) + 1)))

        # ---------  /  Output  /  -------- #

        # -----   /   All India User Analysis Bar chart   /   ----- #
        df_top_user_tab_qry['State'] = df_top_user_tab_qry['State'].astype(str)
        df_top_user_tab_qry['Total User count'] = df_top_user_tab_qry['Total User count'].astype(float)
        df_top_user_tab_qry_fig = px.bar(df_top_user_tab_qry, x='State', y='Total User count',
                                             color='Total User count', color_continuous_scale='thermal',
                                             title='Top User Analysis', height=600, )
        df_top_user_tab_qry_fig.update_layout(title_font=dict(size=33), title_font_color='#6739b7')
        st.plotly_chart(df_top_user_tab_qry_fig, use_container_width=True)

        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':white[Summary]')
        st.subheader('Summary of users')
        st.dataframe(df_top_user_tab_qry)


# ===================================================       /      Time Series      /     ===================================================== #

if option == 'Time Series':

    st.header(':white[Time Series Analysis of Transaction amount and Transaction count for each state from 2018 to 2022]')

    #SQL Query
    cursor.execute(
        f"SELECT * FROM aggregated_transaction;")
    ts = cursor.fetchall()
    df_ts = pd.DataFrame(np.array(ts), columns=['State', 'year', 'Quarter', 'Transaction_type', 'Transaction_count',
                                                'Transaction_amount'])
    df_ts_qry = df_ts.set_index(pd.Index(range(1, len(df_ts) + 1)))
    df_ts_qry['Transaction_amount'] = df_ts_qry['Transaction_amount'].astype(float)
    df_ts_qry['Transaction_count'] = df_ts_qry['Transaction_count'].astype(float)
    min_amount = df_ts_qry['Transaction_amount'].min()
    max_amount = df_ts_qry['Transaction_amount'].max()
    min_count = df_ts_qry['Transaction_count'].min()
    max_count = df_ts_qry['Transaction_count'].max()

    # timeseries plot

    df_ts_fig = px.scatter(df_ts_qry, x='Transaction_amount',
                           y='Transaction_count',
                           size_max=100,
                           size='Transaction_amount',
                           color='State',
                           color_discrete_sequence=px.colors.qualitative.Light24,
                           animation_frame="year",
                           animation_group='State',
                           title='From 2018 to 2020',
                           labels={
                               'total_amount': 'Transaction_amount',
                               'total_count': 'Transaction_count'
                           },
                           width=1000, height=800,
                           opacity = 0.80,
                           template = "simple_white"
                           )

    df_ts_fig.update_xaxes(
        range=[min_amount, 750000000000],  dtick = 10000000000)

    # Adjust y-axis range (minimum, maximum)
    df_ts_fig.update_yaxes(range=[min_count, max_count], dtick = 50000000)

    st.plotly_chart(df_ts_fig, use_container_width=True)
    st.write(" Hit >> Play button to view the movement of transaction amount and count from 2018 to 2022")


else:
    pass

# =========================================         /   /   /   COMPLETED   /   /       ===================================================== #
