import pandas as pd

# task 1 Ques 1
def generate_car_matrix(df)->pd.DataFrame:
    # Pivot the DataFrame to create the matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
    
    # Fill NaN values with 0 (diagonal values)
    car_matrix = car_matrix.fillna(0)
    return car_matrix

generate_car_matrix(pd.read_csv('dataset-1.csv'))
      

# task 1 Ques 2
def get_type_count(df: pd.DataFrame) -> dict:
    # Create a new categorical column 'car_type' based on 'car' values
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)
    
    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()
    
    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))
    
    return sorted_type_counts

# Assuming 'df' is the DataFrame read from dataset-1.csv
result_dict = get_type_count(pd.read_csv('dataset-1.csv'))
print(result_dict)


# task 1 Ques 3
def get_bus_indexes(df: pd.DataFrame) -> list:
    # Calculate the mean of the 'bus' column
    bus_mean = df['bus'].mean()
    
    # Filter the DataFrame based on the condition
    filtered_df = df[df['bus'] > 2 * bus_mean]
    
    # Retrieve the indices as a list (sorted in ascending order)
    bus_indexes = sorted(filtered_df.index.tolist())
    
    return bus_indexes

# Assuming 'df' is the DataFrame read from dataset-1.csv
result_list = get_bus_indexes(pd.read_csv('dataset-1.csv'))
print(result_list)


# task 1 Ques 4
def filter_routes(df: pd.DataFrame) -> list:
    # Group the DataFrame by 'route' and calculate the average 'truck' values
    route_avg_truck = df.groupby('route')['truck'].mean()
    
    # Filter routes based on the condition
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    
    # Sort the list of route names
    sorted_routes = sorted(filtered_routes)
    
    return sorted_routes

# Assuming 'df' is the DataFrame read from dataset-1.csv
result_list = filter_routes(pd.read_csv('dataset-1.csv'))
print(result_list)


# task 1 Ques 5
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
result_matrix = multiply_matrix(pd.read_csv('dataset-1.csv'))
print(result_matrix)


# task 1 Ques 5
def time_check(df):
    # Combine date and time columns into start and end timestamps
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

    # Remove rows with NaT (Not a Timestamp)
    df = df.dropna(subset=['start_timestamp', 'end_timestamp'])

    # Calculate the duration of each timestamp interval
    df['duration'] = df['end_timestamp'] - df['start_timestamp']

    # Extract day of the week and hour from start timestamp
    df['day_of_week'] = df['start_timestamp'].dt.dayofweek
    df['hour'] = df['start_timestamp'].dt.hour

    # Group by 'id', 'id_2' and check for incorrect timestamps
    grouped = df.groupby(['id', 'id_2'])
    incorrect_timestamps = grouped.apply(lambda x: (
        (x['duration'].sum() != pd.Timedelta(days=7)) or
        (x['day_of_week'].nunique() != 7) or
        (x['hour'].nunique() != 24)
    ))

    return incorrect_timestamps

# Read dataset-2.csv into a DataFrame
df = pd.read_csv('dataset-2.csv')

# Get the boolean series indicating incorrect timestamps for each (id, id_2) pair
result = time_check(df)
print(result)
