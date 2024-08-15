import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.ticker import MultipleLocator, FuncFormatter




def remove_outliers(df):
    Q1 = df['Velocity'].quantile(0.10)
    Q3 = df['Velocity'].quantile(0.90)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_df = df[(df['Velocity'] >= lower_bound) & (df['Velocity'] <= upper_bound)]
    return filtered_df


def read_and_average_values(input_folder):
    velocities = []
    avg_distances = []
    cumulative_distances = []
    dates = []

    files = sorted([f for f in os.listdir(input_folder) if f.endswith('_inside.txt')])

    cumulative_distance = 0.0

    for file in files:
        df = pd.read_csv(os.path.join(input_folder, file), sep='\t')

        # Remove outliers
        df = remove_outliers(df)

        # Extract date from the file name
        date_str = file.split('_')[0]
        date = datetime.datetime.strptime(date_str, '%y%m%d')
        dates.append(date)

        # Calculate average velocity
        avg_velocity = df['Velocity'].mean()
        velocities.append(avg_velocity)

        # Calculate average distance for the current file
        avg_distance = df['Distances'].mean()
        avg_distances.append(avg_distance)

        # Accumulate average distance to get cumulative distance
        cumulative_distance += avg_distance
        cumulative_distances.append(cumulative_distance)

    # Sort by date
    sorted_indices = sorted(range(len(dates)), key=lambda k: dates[k])
    velocities = [velocities[i] for i in sorted_indices]
    avg_distances = [avg_distances[i] for i in sorted_indices]
    cumulative_distances = [cumulative_distances[i] for i in sorted_indices]
    dates = [dates[i] for i in sorted_indices]

    return velocities, avg_distances, cumulative_distances, dates


def read_additional_dataset(file_path):
    df = pd.read_csv(file_path)

    # Print column names for debugging
    print("Column names in the additional dataset:", df.columns)

    # Strip any whitespace from column names
    df.columns = df.columns.str.strip()

    # Convert the 'DATE' column to datetime
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y')

    # Filter data within the date range
    start_date = datetime.datetime.strptime('01/06/2022', '%d/%m/%Y')
    end_date = datetime.datetime.strptime('01/11/2022', '%d/%m/%Y')
    df = df[(df['DATE'] >= start_date) & (df['DATE'] <= end_date)]

    # # Calculate cumulative distance
    # df['Cumulative_Distance'] = df['Distance'].cumsum()

    return df['DATE'], df['velocity_md']#, df['Cumulative_Distance']


def plot_average_values(input_folder, additional_file):
    velocities, avg_distances, cumulative_distances, dates = read_and_average_values(input_folder)

    additional_dates, additional_velocities = read_additional_dataset(additional_file)

    # Prepare x-axis values using dates
    x_values = dates

    # Create figure and axes
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Plot velocities on primary y-axis (left)
    ax1.scatter(x_values, velocities, marker='o', color='cornflowerblue', alpha=0.7, label='Average Velocity (m/day) of 41 points')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Average Velocity (m/day)', color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.grid(True)

    # Plot additional dataset velocities on the same y-axis (left)
    ax1.plot(additional_dates, additional_velocities, marker='x', linestyle='-', color='red', alpha=0.7,
             label='Validation: Theodolite measurements of 2 points (m/day)')

    # Create secondary y-axis (right) for cumulative distances
    ax2 = ax1.twinx()
    ax2.plot(x_values, cumulative_distances, marker='s', color='goldenrod', alpha=0.7, label='Average Cumulative Distance of 41 points (m)')
    # ax2.plot(additional_dates, additional_cumulative_distances, marker='^', color='green', alpha=0.7,
    #          label='Additional Cumulative Distance (m)')
    ax2.set_ylabel('Cumulative Distance (m)', color='black')
    ax2.tick_params(axis='y', labelcolor='black')

    # Set axis limits to desired range
    start_date = pd.to_datetime('2022-06-01')
    end_date = pd.to_datetime('2022-11-01')
    ax1.set_xlim([start_date, end_date])
    ax1.set_ylim(0, )
    ax2.set_ylim(0, )

    # Set major ticks at intervals of 2 units
    ax2.yaxis.set_major_locator(MultipleLocator(2))

    # Format the ticks to display no decimals
    ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

    # Add legend and title
    fig.tight_layout()
    fig.legend(loc='upper center')

    # Format x-axis with date labels
    fig.autofmt_xdate()

    # Show plot
    plt.show()


# Usage
input_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_weeklyvelocities_graph'
additional_file = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Theodolite_Rockglacier_65_73_summary.csv'
plot_average_values(input_folder, additional_file)