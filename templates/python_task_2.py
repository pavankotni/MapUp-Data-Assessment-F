
import pandas as pd

# task 2 ques 1
def calculate_distance_matrix(df)->pd.DataFrame():
    # Read the dataset
    data = pd.read_csv(input_csv)

    # Create a DataFrame with unique IDs
    unique_ids = sorted(set(data['id_start'].unique()) | set(data['id_end'].unique()))
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids)

    # Set diagonal values to 0
    distance_matrix = distance_matrix.fillna(0)

    # Populate the distance matrix
    for _, row in data.iterrows():
        id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
        distance_matrix.at[id_start, id_end] = distance
        distance_matrix.at[id_end, id_start] = distance  # Symmetric

    # Cumulative distances along known routes
    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                if distance_matrix.at[i, j] == 0 and i != j:
                    if distance_matrix.at[i, k] != 0 and distance_matrix.at[k, j] != 0:
                        distance_matrix.at[i, j] = distance_matrix.at[i, k] + distance_matrix.at[k, j]

    return distance_matrix


resulting_matrix = calculate_distance_matrix('dataset-3.csv')
print(resulting_matrix)


# task 2 ques 2
def unroll_distance_matrix(df)->pd.DataFrame():
    unrolled_data = []

    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.at[id_start, id_end]
                unrolled_data.append({'id_start': id_start, 'id_end': id_end, 'distance': distance})

    return pd.DataFrame(unrolled_data)

# Example usage with the resulting_matrix from Question 1
unrolled_dataframe = unroll_distance_matrix(resulting_matrix)
print(unrolled_dataframe)


# task 2 ques 3
def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    # Filter rows where id_start is the reference_id
    reference_rows = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_avg_distance = reference_rows['distance'].mean()

    # Calculate the percentage threshold
    percentage_threshold = 0.1  # 10%

    # Filter rows where the average distance is within the percentage threshold
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[
        (result_df['distance'] >= (1 - percentage_threshold) * reference_avg_distance) &
        (result_df['distance'] <= (1 + percentage_threshold) * reference_avg_distance)
    ]

    return result_df

# Example usage with the unrolled_dataframe from Question 2 and a reference_id
reference_id = 1001400
result_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_dataframe, reference_id)
print(result_within_threshold)


# task 2 ques 4
def calculate_toll_rate(df)->pd.DataFrame():
    # Copy the input DataFrame to avoid modifying the original
    toll_dataframe = unrolled_dataframe.copy()

    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }

    # Add columns for each vehicle type with calculated toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        toll_dataframe[vehicle_type] = toll_dataframe['distance'] * rate_coefficient

    return toll_dataframe
