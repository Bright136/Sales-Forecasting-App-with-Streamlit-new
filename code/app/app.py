import streamlit as st
import pandas as pd
import numpy as np
import pickle
import datetime
from PIL import Image
import os
from utils import create_dataframe, process_data
st.set_page_config(
    page_title="CAPE TOWN ANALYTICS",
    page_icon="📉",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)


def load_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        return data 

def check_csv(csv_file, data):
    if os.path.isfile(csv_file):
        data.to_csv(csv_file, mode='a', header=False, encoding='utf-8', index=False)
    else:
        history = data.copy()
        history.to_csv(csv_file, encoding='utf-8', index=False) 

#load all pickle files
ml_compos_1 = load_pickle('ml_components_1.pkl')
ml_compos_2 = load_pickle('ml_components_2.pkl')

# components in ml_compos_2  
categorical_pipeline = ml_compos_2['categorical_pipeline']
numerical_pipeliine = ml_compos_2['numerical_pipeline']
model = ml_compos_2['model']

num_cols = ml_compos_1['num_cols']
cat_cols = ml_compos_1['cat_cols'] 
hol_level_list = ml_compos_1['Holiday_level'].tolist()
hol_city_list = ml_compos_1['Holiday_city'].tolist()

# et the title for the app
hol_city_list.remove('Not Holiday')
hol_level_list.remove('Not Holiday')

my_expander = st.container()

holiday_level = 'Not Holiday'
hol_city = 'Not Holiday'
# st.sidebar.selectbox('Menu', ['About', 'Model'])
with my_expander:
    image = Image.open('images/justin-lim-JKjBsuKpatU-unsplash.jpg')
    st.image(image, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    st.markdown("""
        <style>
        h1 {
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
    st.title('Demo Sales Forecasting :red[App]')
    st.sidebar.markdown("""
    ## Demo App

    This app predict sales from the parameters on the interface
    """)        # create a three column layout
    col1, col2, col3 = st.columns(3)

    # create a date input to receive date
    date = col1.date_input(
        "Enter the Date",
        datetime.date(2019, 7, 6))
    
    # create a select box to select a family
    item_family = col2.selectbox('What is the category of item?',
                                ml_compos_1['family'])

    # create a select box for store city
    store_city = col3.selectbox("Which city is the store located?",
                                ml_compos_1['Store_city'])

    store_state = col1.selectbox("What state is the store located?",
                                ml_compos_1['Store_state'])

    crude_price = col3.number_input('Price of Crude Oil', min_value=1.0, max_value=500.0, value=1.0)

    day_type = col2.selectbox("Type of Day?",
                            ml_compos_1['Type_of_day'], index=2)
    # holiday_level = col3.radio("level of Holiday?",
    #                            ml_compos_1['Holiday_level'])
    colZ, colY = st.columns(2)
    store_type = colZ.radio("Type of store?",
                            ml_compos_1['Store_type'][::-1])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    holi = colY.empty()
    with holi.expander(label='Holiday', expanded=False):
        if day_type == 'Additional Holiday' or day_type == 'Holiday' or day_type=='Transferred holiday':
            holiday_level = st.radio("level of Holiday?",
                                hol_level_list)#.tolist().remove('Not Holiday'))
            hol_city = st.selectbox("In which city is the holiday?",
                                hol_city_list)#.tolist().remove('Not Holiday'))
        else:
            st.markdown('Not Holiday')



    colA, colB, colC = st.columns(3)

    store_number = colA.slider("Select the Store number ",
                            min_value=1,
                            max_value=54,
                            value=1)
    store_cluster = colB.slider("Select the Store Cluster ",
                                min_value=1,
                                max_value=17,
                                value=1)
    item_onpromo = colC.slider("Number of items onpromo ",
                            min_value=0,
                            max_value=800,
                            value=1)
    button = st.button(label='Predict', use_container_width=True, type='primary')

    raw_data = [date, store_number, item_family, item_onpromo, crude_price, holiday_level, hol_city, day_type, store_city, store_state, store_type, store_cluster]

    data = create_dataframe(raw_data)
    processed_data = process_data(data, categorical_pipeline, numerical_pipeliine, cat_cols, num_cols)

if button:
    st.balloons()

    st.metric('Predicted Sale', value=model.predict(processed_data))
    # predictions = model.predict(process_data)
    csv_file = 'history_df.csv'
    check_csv(csv_file, data)
    history = pd.read_csv(csv_file)
    with st.expander('Download Input History'):
        # new_history = history.iloc[1:]
        st.dataframe(history)
    
    st.download_button('Download Data', 
                history.to_csv(index=False), 
                file_name='input_history.csv')

