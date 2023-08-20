import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title="Startup Analysis")
df = pd.read_csv('stratup_cleand.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')
    total = round(df['amount'].sum())
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]

    avg_fun = df.groupby('startup')['amount'].sum().mean()

    total_fun = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)

    with col1:
        st.metric('Total',total)

    with col2:
        st.metric('Max_funding',max_funding)

    with col3:
        st.metric('Average funding',avg_fun)

    with col4:
       st.metric('Number_of_startup',total_fun)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig4, ax4 = plt.subplots()
    ax4.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig4)
def load_invester_details(invester):
    st.title(invester)

    last5_df = df[df['investors'].str.contains(invester)].head(5)[['date','startup','city','vertical','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)
    col1,col2 = st.columns(2)
    with col1:

        big_series = df[df['investors'].str.contains(invester)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()

        st.subheader('Biggest Investment')
        fig ,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    with col2:
        vartical_series = df[df['investors'].str.contains(invester)].groupby('vertical')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader('Sectors invested in')
        fig1, ax1 = plt.subplots()
        ax1.pie(vartical_series,labels=vartical_series.index,autopct="%0.2f%%")
        st.pyplot(fig1)

    col1, col2 = st.columns(2)
    with col1:
        rond_series = df[df['investors'].str.contains(invester)].groupby('round')['amount'].sum().sort_values(ascending=False).head(5)
        st.subheader(' Stage wise invested in')
        fig2, ax2 = plt.subplots()
        ax2.pie(rond_series, labels=rond_series.index, autopct="%0.2f%%")
        st.pyplot(fig2)

    with col2:
        city_series = df[df['investors'].str.contains(invester)].groupby('city')['amount'].sum().sort_values(
            ascending=False).head(5)
        st.subheader(' City wise invested in')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct="%0.2f%%")
        st.pyplot(fig3)

    col1, col2 = st.columns(2)
    with col1:
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(invester)].groupby('year')['amount'].sum()
        st.subheader('Year wise invested in')
        fig3, ax3 = plt.subplots()
        ax3.plot(year_series.index,year_series.values)
        st.pyplot(fig3)







st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select one',['Overall Analysis','Startup','Investor'])
if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)

