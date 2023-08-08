# EGM722-Rhodes_FireSpreadAnalysis
EGM722 - Visualisation and analysis of wildfires in Rhodes

Introduction

The country of Greece and other areas around the world have recently experienced extreme temperatures and significant wildfires, which have put many people’s lives at risk. The National Aeronautics and Space Administration (NASA) Fire Information for Resource Management System (FIRMS) collects and distributes near real time active global fire events to open source. There are three satellite sensors (MODIS & VIIRS) which collect data available to download in different formats. All data has coordinate information, acquisition date, and time, allowing GIS to spatially and temporally analyse this data and visualise change over time. Within Greece, the island of Rhodes had particularly devastating fires in the month of July 2023 and analysis of NASA FIRMS data could be used to track, monitor and combat these events.

The Rhodes fire spread analysis script was developed to automate the workflow of plotting, symbolising and analysing active fires on Rhodes, clearly showing not only the spead of fire over time, but also assessed danger areas which could be used for evacuation warning and/or resource management. The script also automates geospatial product creation using the Cartopy libarary, producing a map with key land use data and the fire dataset overlaid.

Setup & Installation

The script that has been created is publicly hosted on GitHub. It is freely accessible from the EGM722-Rhodes_FireSpreadAnalysis repository here – https://github.com/Drusty42/EGM722-Rhodes_FireSpreadAnalysis
The script was created and developed within Jupiter Notebooks and PyCharm integrated development environment (IDE).

Python Dependencies

Various Python dependencies are required for the script to function, which can be seen in table 1 below. To replicate the environment and dependencies used for this script, the environment.yml file can be used from the linked GitHub repository. This requires Anaconda Navigator to be installed to import the created environment. Once the environment has been activated the script can be used.

Table 1. 
Python dependencies	Package	Version
geopandas		0.13.2
matplotlib		3.7.1
cartopy			0.21.1

Required input datasets

The prerequisite datasets that are required for the script need to be downloaded from various or similar sources. The sources where data has been downloaded from can be seen below in table 2. Additionally, the datasets used can be found in a folder called AssessmentData available for download in the linked GitHub repository.

Table 2. Input datasets
Dataset				File Type	Source
J1_VIIRS_C2_Europe_7d		.shp		https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-shapefile
SUOMI_VIIRS_C2_Europe_7d	.shp		https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-shapefile
BUA				.shp		https://download.geofabrik.de/europe/greece.html
RoadsRefine			.shp		https://download.geofabrik.de/europe/greece.html
River				.shp		https://download.geofabrik.de/europe/greece.html
RhodesBnd			.shp		https://download.geofabrik.de/europe/greece.html
Lake				.shp		https://download.geofabrik.de/europe/greece.html

Data preparation

Some data preparation is required to enable the input datasets to work within the design of the script; this was all done in ArcGIS PRO. The Rhode island boundary (RhodesBnd) was selected and exported from the Greek country boundary dataset, to be used as the AOI for the script. The roads dataset was refined to exclude some roads which would not be effective to display at larger scales. Two NASA VIIRS datasets were downloaded, merged together and clipped to the Rhodes island boundary, along with all other datasets. Lastly, a new field text field was required to be created to allow the active fire events to be split acquisition date by the script. Further work is require to allow the ACQ_DATE field to be used in its original format.

Methodology

The script was designed to automate a workflow of plotting NASA FIRMS fire point datasets to visualise the spread of active wildfires and identity danger areas in proximity. Using input datasets, this is currently only possible for the island of Rhodes however it would be relatively easy to adapt this for other areas with similar data. Eight functions were developed over time to perform data visualisation, analysis and product creation. The script was written to follow a logical workflow; the key workflow methodology was as follows:
1.	Import Python modules.
2.	Load geospatial datasets for fires, built-up-areas (BUA), roads, rivers and lakes.
3.	Create a map using the Universal Transverse Mercator (UTM) projection.
4.	Define symbology and styles for each feature category.
5.	Plot each feature category on the map using specified styles and symbology.
6.	Create buffer around fire feature.
7.	Set map extent and add a coloured background
8.	Create and add a legend for each feature category contained in the map.
9.	Add a title text box to the map


1 – Import Python modules
The python modules that are required for the script to function can be seen in figure 1 overleaf. All modules are available with the installation of python 3.x
 
Figure 1. Import Python modules

2 – Load geospatial datasets
Several downloaded geospatial datasets are required to be loaded by the script, with each corresponding to different features or elements to be displayed within the map. The geopandas library is used to read and load the input shapfiles (.shp), creating a variable for each. The section of code for this can be seen below in figure 2.
 
Figure 2. Load geospatial datasets

3 – Create a map using the UTM projection
The map and geospatial dataset are required to have a defined coordinate system and be plotted to a frame in that system. A figure object is created using myFig to a size of 10 by 10 inches; this will be the size of the map. The UTM coordinate system is defined by ‘myCRS’ using the ‘cartopy.crs’ module, in this case it is set to UTM zone 35, the correct zone for Rhodes. Finally an axis object is created using ‘ax’, to plot geospatial datasets in the defined myCRS projection. The section of code for this can be seen below in figure 3.
 
Figure 3. Create map in UTM

4 & 5 – Define symbology, styles and plot each feature category
To specify the desired symbology for some features, dictionaries were created to contain style information. This was to determine the appearance of features that were required to have a specific size, colour or marked based on an attribute field contained within the dataset.Next the specific symbology and style is set for each geospatial feature, some more complex than others: 

1.	For the drawing of BUAs, a graduated and hierarchical symbology was used, based on the ‘bua_styles’ to determine marker, size and colour. The ‘fclass’ attribute field is used to filter BUA by type then each location is plotted, firstly with a larger white area then the symbol on top; this created a halo effect.

2.	For the drawing of road features a hierarchical symbology was used, based on the ‘road_type_styles’ to determine colour and width. The ‘fclass’ attribute field is used again to filter roads by type then the ‘ax.add.line() function is used to add line geometries

3.	For the drawing of fires, the same symbol is used but coloured to represent acquisition date and show temporal change based on ‘fire_styles’. A transparency is applied using ‘alpha’ to allow feature beneath to be seen.

4.	For the drawing of rivers, line geometries are plotted as before with a singular colour and line width.

5.	For the drawing of lakes, a ShapelyFeature is created using the lake polgon geometry and a single face colour is specified.
The ax.plot (points), ax.add_line (lines) and ax.add_feature (polygon) are used to plot each feature. The ‘zorder’ parameter is used to determine the hierarchy of all plotted features; the higher the number assigned the higher the feature will sit in the map.

Within each feature that is drawn a legend handle is created, to be added to the legend later in the script. These are created using ‘mpatches.Patch’ (matplotlib.patches) and ‘mline.Line2d’ (matplotlib.lines) to generate lines and markers as per the same styles as the plotted features.

Symbology, styles and other settings are relatively easy to adjust without having to change the code. See figures 4 - 6 overleaf for the section of code
 
Figure 4. Symbology, styles, plotting and legend handles
 
Figure 5. Symbology, styles, plotting and legend handles
 
Figure 6. Symbology, styles, plotting and legend handles

6 – Create buffer around fire feature
Using ‘Fire.geometry.buffer(value) a buffer area was applied to the geometry of the fire points, the value field can be set to a value in metres. The created buffers were then dissolved using ‘unary.union’ into a single geometry area. The dissolved buffer was then plotted similar to above with a specified symbology and transparency. Display settings can be changed with relative ease however to run multiple or separate buffers for each acquisition the code would need to have changes made. See figure 7 overleaf for the section of the code.
 
Figure 7. Create buffer

7 – Create and add a legend for each feature category contained in the map
Generating legend handles creates created matplotlib patches to represent the features contained in the legend, corresponding to the features in the map. There are several arguments contained in ‘def generate.handles’ which define how the legend will look. Next, a legend handles list was created for each feature and finally the ‘plt.legend’ is used to ring all the features into the legend and display it on the map. The desired item, title and position are specified here. See figure 8 below for the section of the code.
 
Figure 8. Create & add legend

8 – Set map extent and add a coloured background
The ‘ax.set_extent’ determines the geographic extent of the created map, using the four X/Y min/max values it sets the visible area of the map. There is an error in the code which if using metres values produces a very large extent suggesting there is a coordinate system error. Alternative values had to be used to achieve the desired extent and this could be corrected in the future. The ‘ax.add_patch(plt.Rectangle’ function was used to add a blue coloured background to the map. See figure 9 below for the section of the code.
 
Figure 9. Set map extent & background

9 – Add a title text box to the map
Using the ‘ax.text’ function a text box for a title was added to the map with a specific style, text and size. Lastly, the ‘myFig.savefig was used to export the final product to a .png file with a dots per inch (dpi) of 300. See figure 10 below for the section of the code.
 
Figure 10. Title & export product
 
Results
The visualisation and analysis as a result of the created script provide insight into the development of wildfires on Rhodes island between the 24th and 27th of August 2023. The final output product highlights the spatial distribution and progression of active fire points, also in relation to key infrastructure and land use areas. Additionally, a comprehensive overview map is created showing basic small scale features on the island which are clearly explained in the legend. See figure 11 below showing the final product.
 
Figure 11. Final product

Wildfire analysis

For the active fire points between the 24th and 27th of August, a graduated transparent symbology was set from yellow to magenta. This clearly shows the spread of active fires day by day, relying on the symbology and visual scatter. It is evident in figure 11 that the larger active fire area is spreading generally west over the time period and northwest in the latter stages (likely due to prevailing winds). A larger or more current dataset could be acquired to further analyse data using the created script, used to give timescales for evacuation of BUA and positioning resources to combat the fires. The assessed danger area of 1500m was an approximation of how far the fire could travel, but further analysis could be conducted to determine a more appropriate value, which can be changed within the script. The main limitation of the script regarding the buffer (and other area reliant on metric measurement) was an error which would not allow projected coordinate system measurements in metres to be used correctly. This requires further investigation

Product creation

Most geospatial datasets were displayed and symbolised effectively within the map and legend. However, the script was unable to apply the correct and desired hierarchy to the roads i.e. primary roads on to of secondary and so forth.

Troubleshooting

If any errors occur within the use of the script there are possible causes and solutions listed below.

Importing modules

If an error message similar to ‘ModuleNoFoundError: No modules name xxxx’ is encountered the most likely cause is the correct module(s) have not been successfully installed. The solution is to check which module(s) are not installed in the error message and install using the environment.yml or as a workaround manually in conda.

Missing data or file paths

If an error message similar to ‘FileNotFoundError: No such file or directory xxx’ is encountered the most likely cause is the required input data is not loaded or there is a naming convention issue. The solution is to check the loading geospatial dataset section of the script to ensure all are loaded with the correct name and source. Other related issues may be due to incorrect data or attribute field preparation. In that event please double check raw input data and preparation phases.

Variable names or values

If any local variable errors are encountered this could be due to the sue of a variable which has not been defined. Ensure variable names are correct if any updates have been made to the script and change them accordingly.
