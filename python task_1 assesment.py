#!/usr/bin/env python
# coding: utf-8

# In[19]:


import pandas as pd
df = pd.read_csv(r"C:\Users\91910\Downloads\dataset-1.csv")
def generate_car_matrix(data):
    dh = data.pivot(index='id_1', columns='id_2', values='car')
    dh.fillna(0, inplace=True)
    return dh
new_df = generate_car_matrix(df)
print(new_df)


# In[20]:


import pandas as pd
df = pd.read_csv(r"C:\Users\91910\Downloads\dataset-1.csv")
def get_type_count(data):
    data['car_type'] = pd.cut(data['car'], bins=[float('-inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_count = data['car_type'].value_counts().to_dict()
    type_count = dict(sorted(type_count.items()))
    return type_count
result = get_type_count(df)
print(result)


# In[9]:


import pandas as pd
def get_bus_indexes(df):
    mean_bus = df['bus'].mean()
    indices = df[df['bus'] > 2 * mean_bus].index.tolist()
    return sorted(indices)
get_bus_indexes(df)


# In[21]:


import pandas as pd
def filter_routes(df):
    avg = df.groupby('route')['truck'].mean()
    greater = avg[avg > 7].index.tolist()
    return sorted(greater)
filter_routes(df)


# In[23]:


import pandas as pd

def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    # Define a function to apply custom conditions
    def custom_multiply(value):
        if value > 20:
            return round(value * 0.75, 1)
        else:
            return round(value * 1.25, 1)

    # Apply the custom conditions to each element in the matrix
    modified_matrix = matrix.applymap(custom_multiply)

    return modified_matrix

# Assuming 'matrix' is the DataFrame returned from the generate_car_matrix function
result_matrix = multiply_matrix(pd.read_csv('/Users/mansimishra/Documents/Mapup/MapUp-Data-Assessment-F/datasets/dataset-1.csv'))
print(result_matrix)


# In[26]:


import pandas as pd
df = pd.read_csv(r"C:\Users\91910\Downloads\dataset-2 (1).csv")
def check_time_completeness(df):
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    df['duration'] = df['end_timestamp'] - df['start_timestamp']
    grouped = df.groupby(['id', 'id_2'])
    completeness_check = grouped.apply(lambda x: ((x['duration'].min() >= pd.Timedelta(days=1)) and
                                                  (x['duration'].max() <= pd.Timedelta(days=1, seconds=1)) and
                                                  (x['start_timestamp'].dt.dayofweek.nunique() == 7)
                                                 ))
    return completeness_check
check_time_completeness(df)


# In[ ]:





# In[ ]:




