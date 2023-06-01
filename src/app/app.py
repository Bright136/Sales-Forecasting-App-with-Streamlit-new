import sys
import os
import streamlit as st
import pandas as pd
import pickle
import datetime
from PIL import Image

# Add the root folder to the Python module search path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utils import create_dataframe, process_data

# Set Streamlit page configuration
st.set_page_config(
    page_title="CAPE TOWN ANALYTICS",
    page_icon="📉",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# Define directory paths
DIRPATH = os.path.dirname(os.path.realpath(__file__))
ml_components_1 = os.path.join(DIRPATH, "..", "assets", "ml_components", "ml_components_1.pkl")
ml_components_2 = os.path.join(DIRPATH, "..", "assets", "ml_components", "ml_components_2.pkl")
hist_df = os.path.join(DIRPATH, "..", "assets", "history.csv")
image_path = os.path.join(DIRPATH, "..", "assets", "images", "justin-lim-JKjBsuKpatU-unsplash.jpg")



# check if csv file exits 
def check_csv(csv_file, data):
    if os.path.isfile(csv_file):
        data.to_csv(csv_file, mode='a', header=False, encoding='utf-8', index=False)
    else:
        history = data.copy()
        history.to_csv(csv_file, encoding='utf-8', index=False) 

# Load pickle files
def load_pickle(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
        return data

ml_compos_1 = load_pickle(ml_components_1)
ml_compos_2 = load_pickle(ml_components_2)

# Extract components from ml_compos_2
categorical_pipeline = ml_compos_2['categorical_pipeline']
numerical_pipeliine = ml_compos_2['numerical_pipeline']
model = ml_compos_2['model']

# Extract columns from ml_compos_1
num_cols = ml_compos_1['num_cols']
cat_cols = ml_compos_1['cat_cols']
hol_level_list = ml_compos_1['Holiday_level'].tolist()
hol_city_list = ml_compos_1['Holiday_city'].tolist()

# Remove 'Not Holiday' from lists
hol_city_list.remove('Not Holiday')
hol_level_list.remove('Not Holiday')

# Create a container for expanding content
my_expander = st.container()


holiday_level = 'Not Holiday'
hol_city = 'Not Holiday'
# st.sidebar.selectbox('Menu', ['About', 'Model'])

# Expandable container for displaying content
with my_expander:
    image = Image.open(image_path)
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
    """)
    
    # create a three column layout
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
    csv_file = hist_df
    check_csv(csv_file, data)
    history = pd.read_csv(csv_file)
    with st.expander('Download Input History'):
        # new_history = history.iloc[1:]
        st.dataframe(history)
    
    st.download_button('Download Data', 
                history.to_csv(index=False), 
                file_name='input_history.csv')

