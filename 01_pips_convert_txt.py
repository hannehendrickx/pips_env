import os
import glob

# converts pips output to .txt file format that can be imported into VIG for scaling.

def reformat_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        for line in lines:
            numbers = line.split()
            if len(numbers) == 2:
                number1 = float(numbers[0])
                number2 = float(numbers[1])
                new_line = f"{number1:.4f},{number2:.4f},0.0000\n"
                f.write(new_line)


def reformat_file_with_id(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    with open(output_file, 'w') as f:
        # Write the header
        f.write("ID\tx_img\ty_img\tz_img\n")

        # Write each line with an ID
        for idx, line in enumerate(lines):
            numbers = line.split()
            if len(numbers) == 2:
                number1 = float(numbers[0])
                number2 = float(numbers[1])
                new_line = f"{idx}\t{number1:.4f}\t{number2:.4f}\t0.0000\n"
                f.write(new_line)


def process_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    txt_files = glob.glob(os.path.join(input_folder, '*.txt'))

    for txt_file in txt_files:
        filename = os.path.basename(txt_file)

        # Output file paths
        output_file = os.path.join(output_folder, filename)
        output_file_with_id = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_withID.txt")

        # Reformat the files
        reformat_file(txt_file, output_file)
        reformat_file_with_id(txt_file, output_file_with_id)


# Usage
input_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_weekly_summer2022_scaling'
output_folder = r'C:\Users\Hanne Hendrickx\Documents\04_Papers\2024_PIPS\Data\Cam5_weekly_summer2022_scaling_reformated'
process_folder(input_folder, output_folder)

