import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_velocity_data(input_folder, suffix):
    data = []
    files = [f for f in os.listdir(input_folder) if f.endswith('.txt') and suffix in f]
    for file in files:
        df = pd.read_csv(os.path.join(input_folder, file), sep='\t')
        df['Source'] = suffix  # Add a column to indicate the source
        data.append(df[['Velocity', 'Source']])
    combined_data = pd.concat(data, ignore_index=True)
    return combined_data

def remove_outliers(df):
    Q1 = df['Velocity'].quantile(0.10)      #0.25 for cam4
    Q3 = df['Velocity'].quantile(0.90)      #0.75 for cam4
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_df = df[(df['Velocity'] >= lower_bound) & (df['Velocity'] <= upper_bound)]
    return filtered_df

def plot_velocity_violin(input_folder):
    # Read data from files
    inside_data = read_velocity_data(input_folder, '_inside')
    outside_data = read_velocity_data(input_folder, '_outside')

    # Combine data for plotting
    combined_data = pd.concat([inside_data, outside_data], ignore_index=True)

    # # Remove outliers
    filtered_data = remove_outliers(combined_data)
    print(filtered_data)

    # Map sources to new labels
    source_map = {'_inside': 'Moving area', '_outside': 'Stable area'}
    filtered_data.loc[:, 'Source'] = filtered_data['Source'].map(source_map)

    # Create the violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Source', y='Velocity', data=filtered_data, palette={'Moving area': 'goldenrod', 'Stable area': 'cornflowerblue'})
    plt.ylabel('Velocity in m/day', size='xx-large')
    plt.xlabel('Source', size='xx-large')
    plt.xticks(size='xx-large')
    plt.yticks(size='x-large')

    # Add lines
    plt.axhline(y=0, color='gray', linestyle='-')
    plt.axhline(y=-0.02, color='black', linestyle='--')     #0.01 for cam4
    plt.axhline(y=0.02, color='black', linestyle='--')      #0.01 for cam4

    # Display the number of data points used for each plot
    for label in source_map.values():
        count = filtered_data[filtered_data['Source'] == label].shape[0]
        plt.text(x=0 if label == 'Moving area' else 1, y=filtered_data['Velocity'].max(), s=f'N={count}',
                 horizontalalignment='right', size='xx-large', color='black', weight='semibold')

    plt.tight_layout()

    plt.show()

# Usage
input_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_tracked_inside_outside'
plot_velocity_violin(input_folder)

