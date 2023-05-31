import numpy as np
import pandas as pd




def payday(row):
    if row.DayOfMonth == 15 or row.Is_month_end == 1:
        return 1
    else:
        return 0
        

def date_extracts(data):
    data['Year'] = data.index.year
    data['Month'] = data.index.month
    data['DayOfMonth'] = data.index.day
    data['DaysInMonth'] = data.index.days_in_month
    data['DayOfYear'] = data.index.day_of_year
    data['DayOfWeek'] = data.index.dayofweek
    data['Week'] = data.index.isocalendar().week
    data['Is_weekend'] = np.where(data['DayOfWeek'] > 4, 1, 0)
    data['Is_month_start'] = data.index.is_month_start.astype(int)
    data['Is_month_end'] = data.index.is_month_end.astype(int)
    data['Quarter'] = data.index.quarter
    data['Is_quarter_start'] = data.index.is_quarter_start.astype(int)
    data['Is_quarter_end'] = data.index.is_quarter_end.astype(int)
    data['Is_year_start'] = data.index.is_year_start.astype(int)
    data['Is_year_end'] = data.index.is_year_end.astype(int)




# the function creates a dataframe from the inputs 
def create_dataframe(arr):
    X = np.array([arr])
    data = pd.DataFrame(X, columns=['date', 'Store_number', 'Family', 'Item_onpromo', 'Oil_prices', 
                                    'Holiday_level', 'Holiday_city','TypeOfDay', 'Store_city', 
                                    'Store_state', 'Store_type', 'Cluster'])
    data[['Store_number', 'Item_onpromo', 'Cluster']] = data [['Store_number', 'Item_onpromo', 'Cluster']].apply(lambda x: x.astype(int))
    data['date'] = pd.to_datetime(data['date'])
    
    return data

def process_data(data, categorical_pipeline, numerical_pipeliine, cat_cols, num_cols):
    processed_data = data.set_index('date')
    date_extracts(processed_data)
    processed_data['Is_payday']= processed_data[['DayOfMonth', 'Is_month_end']].apply(payday, axis=1)
    processed_data[cat_cols] = categorical_pipeline.transform(processed_data[cat_cols])
    processed_data[num_cols] = numerical_pipeliine.transform(processed_data[num_cols])    
    return  processed_data

