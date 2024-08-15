# Short Communication: AI-Based Tracking of Fast-Moving Alpine Landforms Using High Frequency Monoscopic Time-Lapse Imagery
Supplemantary code and data for the preprint submitted to Earth Surface Dynamics

Authors: Hanne Hendrickx, Xabier Blanch, Melanie Elias, Reynald Delaloye, Anette Eltner
Correspondence to: Hanne Hendrickx (hanne.hendrickx@tu-dresden.de)

Code developed in Python and C++ for extracting velocity information out of monoscopic time-lapse images from a landslide and a rock glacier. 

## General workflow
![General workflow](/assets/Figures/Figure2.png)

### 1. Application of the Persistent Independent Particle tracker (PIPs++) 

For installing the PIPs++ model, we refer to their github page: https://github.com/aharley/pips2

The adapted codes in 1_pips++ folder can then be deployed witht the Data_Sample (image data)
The output of the PIPs++ model can be found in the Data_Sample folder as well (outputpips++)

![Example PIPs++ output](assets/Figures/Figure3.png)

## 2. From 2D to 3D: image-to-geometry scaling

This part of the repository is still under construction. Please reach out to us if you would like to run the image-to-geometry scaling. 
Results for the Data_Sample can be found in the folder (outputI2G). 

The LightGlue model is deployed for this part of the code to match a camera image to a synthetic image rendered from a coloured 3D point. 
We refer to their github page to install and run LightGlue: https://github.com/cvg/LightGlue

![I2G workflow](assets/Figures/Figure4.png) 

## 3. Basic velocity calculations and visualisation

The scaled data can than be used to calculate distance between two tracked points for each time epoch, and subsequently velocity data can be calculated based on the temporal interval of the images.
The source data and code are all available to recreate following paper figures:

![Figure5](assets/Figures/Figure5.png)
![Figure6](assets/Figures/Figure6.png)

