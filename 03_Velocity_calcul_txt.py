import os
import pandas as pd
import numpy as np


def merged_files(file1, file2, input_folder):
    df1 = pd.read_csv(os.path.join(input_folder, file1), sep='\t')
    df2 = pd.read_csv(os.path.join(input_folder, file2), sep='\t')
    df3 = df1.merge(df2, on='ID', suffixes=('_x', '_y'))
    return df3


def calculate_distance(df3, timeinterval, file1, file2, output_folder):
    # Calculate the Euclidean distance between corresponding points in df1 and df2
    distances = np.sqrt((df3['X_y'] - df3['X_x']) ** 2 +
                        (df3['Y_y'] - df3['Y_x']) ** 2 +
                        (df3['Z_y'] - df3['Z_x']) ** 2)
    velocity = distances / timeinterval
    df3['Distances'] = distances
    df3['Velocity'] = velocity

    # Create a more readable file name
    file_name = f"{os.path.splitext(file1)[0]}_{os.path.splitext(file2)[0]}.txt"
    df3.to_csv(os.path.join(output_folder, file_name), sep='\t', index=False)


def batch_files(input_folder, output_folder, timeinterval):
    files = sorted(os.listdir(input_folder), key=lambda x: int(x.split('_')[2].split('.')[0]))
    for i in range(len(files) - 1):
        file1 = files[i]
        file2 = files[i + 1]
        result = merged_files(file1, file2, input_folder)
        calculate_distance(result, timeinterval, file1, file2, output_folder)


# Usage
input_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_trackedcoordinates'
output_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_trackedcoordinates_with_distances'
timeinterval = 7  # Adjust the time interval as needed

os.makedirs(output_folder, exist_ok=True)
batch_files(input_folder, output_folder, timeinterval)
