import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

img_path = '/home/pips/PIPS/pips2/gss_images/Datasets paper/pedro/images'
filenames = glob.glob(os.path.join(img_path, '*.png'))
filenames = sorted(filenames)

raw_path = '/home/pips/PIPS/pips2/outputs/Pedro_test_10_1000_de00_13:45:01'
filenames_raw = glob.glob(os.path.join(raw_path, '*.txt'))
filenames_raw = sorted(filenames_raw)

output_path = os.path.join(raw_path, 'pictures')
os.makedirs(output_path, exist_ok=True)

for y, image in enumerate(filenames):
    plt.ioff()
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    img = cv2.imread(image)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    points_0 = np.loadtxt(filenames_raw[y])
    points_1 = np.loadtxt(filenames_raw[y + 1])
    for i, point in enumerate(points_0):
        ax.arrow(point[0], point[1], points_1[i, 0] - point[0], points_1[i, 1] - point[1],
                 width=1)
    ax.axis('off')
    ax.imshow(img)

    # Save the figure with the correct output path
    output_filename = os.path.join(output_path, Path(image).name.replace('.PNG', '_output.png'))
    plt.savefig(output_filename, dpi=600)

    fig.clear()
    fig.clf()
    plt.close()
