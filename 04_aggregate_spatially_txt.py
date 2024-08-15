import pandas as pd
import os
import glob
from shapely.geometry import Point, Polygon


#seperates the txt files for stable points and points within the area of study (landslide or rock glacier area) using a simple bounding box or more ellaborate polygon
def filter_points_in_bounding_box(input_file, inside_box_output_file, outside_box_output_file, min_x, min_y, max_x,
                                  max_y):
    # Load the data
    df = pd.read_csv(input_file, sep='\t')

    # Filter the data within the bounding box
    inside_box_df = df[(df['X_x'] >= min_x) & (df['X_x'] <= max_x) &
                       (df['Y_x'] >= min_y) & (df['Y_x'] <= max_y)]

    # Filter the data outside the bounding box
    outside_box_df = df[~((df['X_x'] >= min_x) & (df['X_x'] <= max_x) &
                          (df['Y_x'] >= min_y) & (df['Y_x'] <= max_y))]

    # Save the filtered data to new files
    inside_box_df.to_csv(inside_box_output_file, sep='\t', index=False)
    outside_box_df.to_csv(outside_box_output_file, sep='\t', index=False)


def filter_points_in_polygon(input_file, inside_polygon_output_file, outside_polygon_output_file, polygon):
    # Load the data
    df = pd.read_csv(input_file, sep='\t')

    # Create a polygon from the given corner coordinates
    poly = Polygon(polygon)

    # Function to check if a point is inside the polygon
    def is_inside_polygon(row):
        point = Point(row['X_x'], row['Y_x'])
        return poly.contains(point)

    # Apply the function to filter the DataFrame
    inside_polygon_df = df[df.apply(is_inside_polygon, axis=1)]
    outside_polygon_df = df[~df.apply(is_inside_polygon, axis=1)]

    # Save the filtered data to new files
    inside_polygon_df.to_csv(inside_polygon_output_file, sep='\t', index=False)
    outside_polygon_df.to_csv(outside_polygon_output_file, sep='\t', index=False)


#def process_folder(input_folder, output_folder, min_x, min_y, max_x, max_y):
def process_folder(input_folder, output_folder, polygon):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all text files in the input folder
    txt_files = glob.glob(os.path.join(input_folder, '*.txt'))

    for txt_file in txt_files:
        # Get the base name of the file
        base_name = os.path.basename(txt_file)

        #for bounding box
        # # Create output file names
        # inside_box_output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}_inside.txt")
        # outside_box_output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}_outside.txt")
        #
        # # Process the file
        # filter_points_in_bounding_box(txt_file, inside_box_output_file, outside_box_output_file, min_x, min_y, max_x,
        #                              max_y)

        #for polygon
        # Create output file names
        inside_polygon_output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}_inside.txt")
        outside_polygon_output_file = os.path.join(output_folder, f"{os.path.splitext(base_name)[0]}_outside.txt")

        # Process the file
        filter_points_in_polygon(txt_file, inside_polygon_output_file, outside_polygon_output_file, polygon)


# Usage
input_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_trackedcoordinates_with_distances'
output_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_tracked_inside_outside'
# min_x = 2628800.0
# min_y = 1104480.0
# max_x = 2628830.0
# max_y = 1104500.0

# Example polygon with more than four points
polygon = [
    (2628452.697998, 1104859.281006),
    (2628384.936005, 1105062.012024),
    (2628450.563004, 1105101.377014),
    (2628573.893999, 1104943.829987),
    (2628562.990002, 1104877.431000),
    (2628472.181999, 1104831.756989),
    (2628452.697998, 1104859.281006) # Closing the polygon by repeating the first point is optional but recommended
]

#process_folder(input_folder, output_folder, min_x, min_y, max_x, max_y)
process_folder(input_folder, output_folder, polygon)