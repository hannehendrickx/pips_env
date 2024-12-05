# Short Communication: AI-Based Tracking of Fast-Moving Alpine Landforms Using High Frequency Monoscopic Time-Lapse Imagery
Supplemantary code and data for the preprint submitted to Earth Surface Dynamics

Authors: Hanne Hendrickx*, Melanie Elias*, Xabier Blanch, Reynald Delaloye, Anette Eltner

*Joint first author

Correspondence to: Hanne Hendrickx (hanne.hendrickx@tu-dresden.de) and Melanie Elias (melanie.elias@tu-dresden.de)

Code developed in Python and C++ for extracting velocity information out of monoscopic time-lapse images from a landslide and a rock glacier. 

## General workflow
![General workflow](/Figures/Figure2.png)

### 1. Application of the Persistent Independent Particle tracker (PIPs++) 

For installing the PIPs++ model, we refer to their github page: https://github.com/aharley/pips2

The adapted codes in 1_pips++ folder can then be deployed witht the Data_Sample (image data)
The output of the PIPs++ model can be found in the Data_Sample folder as well (outputpips++)

![Example PIPs++ output](/Figures/Figure3.png)

### 2. From 2D to 3D: image-to-geometry registration using GIRAFFE

This part of the code is hosted an on a different repository. Please visit https://github.com/mel-ias/GIRAFFE

The LightGlue model is deployed for this part of the code to match a camera image to a synthetic image rendered from a coloured 3D point. 
We refer to their github page to install and run LightGlue: https://github.com/cvg/LightGlue

![I2G workflow](/Figures/Figure4.png) 

### 3. Basic velocity calculations and visualisation

The scaled data can than be used to calculate distance between two tracked points for each time epoch, and subsequently velocity data can be calculated based on the temporal interval of the images.
The source data and code are all available to recreate following paper figures:

![Figure5](/Figures/Figure5.png)
![Figure6](/Figures/Figure6.png)

