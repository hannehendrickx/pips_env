import os

#prepares txt file from cloudcompare so it is in the right input for pwconverter

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            columns = line.split()
            # Keep only the first six columns
            new_line = ' '.join(columns[:6])
            outfile.write(new_line + '\n')

# Define the file paths
input_file = r'G:\TUDresden\UAV_Data\Grabengufer\Cam5_5cm.txt'
output_file = r'G:\TUDresden\UAV_Data\Grabengufer\Cam5_5cm_2.txt'
process_file(input_file, output_file)
