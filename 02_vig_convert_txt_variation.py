# converts VIG output to .txt file format for calculating velocities - for slightly different file names _scaled.txt and _pts_ID.txt

import os
import re

def reformat_with_ids(coordinates_file, ids_file, output_file):
    # Read IDs from the IDs file
    with open(ids_file, 'r') as f:
        ids = [line.strip() for line in f]

    # Read coordinates from the coordinates file
    with open(coordinates_file, 'r') as f:
        coordinates = [line.strip() for line in f]

    # Ensure the number of IDs matches the number of coordinate lines
    if len(ids) != len(coordinates):
        print(f"Error: The number of IDs does not match the number of coordinate lines in {coordinates_file}.")
        return

    # Write the reformatted output to the output file
    with open(output_file, 'w') as f:
        # Write the header
        f.write("ID\tX\tY\tZ\n")

        # Write each line with the corresponding ID and coordinates
        for id_value, coord_line in zip(ids, coordinates):
            x, y, z = coord_line.split(',')
            new_line = f"{id_value}\t{x}\t{y}\t{z}\n"
            f.write(new_line)

def process_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    files = os.listdir(input_folder)

    # Group files by their ID
    file_groups = {}
    for file in files:
        match = re.match(r'm220606150003016_raw_points(\d+)(_projected|_ID).txt', file)
        if match:
            file_id = match.group(1)
            if file_id not in file_groups:
                file_groups[file_id] = {}
            if '_projected' in file:
                file_groups[file_id]['coordinates'] = os.path.join(input_folder, file)
            elif '_ID' in file:
                file_groups[file_id]['ids'] = os.path.join(input_folder, file)

    # Process each group of files
    for file_id, paths in file_groups.items():
        if 'coordinates' in paths and 'ids' in paths:
            coordinates_file = paths['coordinates']
            ids_file = paths['ids']
            output_file = os.path.join(output_folder, f'tracked_coordinates_{file_id}.txt')

            reformat_with_ids(coordinates_file, ids_file, output_file)
        else:
            print(f"Missing required files for ID {file_id}")

# Usage
input_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\cam05_scaled'
output_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_trackedcoordinates'

process_files(input_folder, output_folder)


