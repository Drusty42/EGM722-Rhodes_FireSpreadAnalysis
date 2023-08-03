import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# generates matplotlib handles to create a legend of features to be contained in the map
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# Creates a scale bar of 25Km length with 5Km increments located bottom right of the map
def scale_bar(ax, location=(0.92, 0.05)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 25000], [sby, sby], color='k', linewidth=9, transform=ax.transData)
    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.transData)
    ax.plot([sbx, sbx - 15000], [sby, sby], color='k', linewidth=9, transform=ax.transData)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=9, transform=ax.transData)
    ax.plot([sbx, sbx - 5000], [sby, sby], color='k', linewidth=6, transform=ax.transData)
    ax.plot([sbx - 5000, sbx - 10000, sbx - 15000, sbx - 20000, sbx - 25000], [sby, sby], color='w', linewidth=6,
            transform=ax.transData)

    ax.text(sbx - 25000, sby - 4500, '25 km', transform=ax.transData, fontsize=8, ha='left')
    ax.text(sbx - 20000, sby - 4500, '20 km', transform=ax.transData, fontsize=8, ha='left')
    ax.text(sbx - 15000, sby - 4500, '15 km', transform=ax.transData, fontsize=8, ha='left')
    ax.text(sbx - 10000, sby - 4500, '10 km', transform=ax.transData, fontsize=8, ha='left')
    ax.text(sbx - 5000, sby - 4500, '5 km', transform=ax.transData, fontsize=8, ha='left')
    ax.text(sbx, sby - 4500, '0 km', transform=ax.transData, fontsize=8, ha='left')

# loads the boundary of Rhodes island as the land extent and analysis area
outline = gpd.read_file(os.path.abspath('AssessmentData/RhodesBnd.shp'))

# loads the datasets to be displayed on the map
BUA = gpd.read_file(os.path.abspath('AssessmentData/BUA.shp'))
Lake = gpd.read_file(os.path.abspath('AssessmentData/Lake.shp'))
River = gpd.read_file(os.path.abspath('AssessmentData/River.shp'))
Road = gpd.read_file(os.path.abspath('AssessmentData/RoadsRefine.shp'))
Fire = gpd.read_file(os.path.abspath('AssessmentData/VIIRS_points.shp'))

# creates a page size of 10x10 inches
myFig = plt.figure(figsize=(10, 10))

# creates a Universal Transverse Mercator (UTM) coordinate system to transform data
myCRS = ccrs.UTM(35)

# create axis object in the figure using the UTM projection to plot data.
ax = plt.axes(projection=myCRS)

# add the Rhodes boundary using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='khaki')

# adds the created features to the map.
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)

# using the boundary of the shapefile features, zoom the map to our area of interest
ax.set_extent([xmin-0.1, xmax+0.1, ymin-0.1, ymax+0.1], crs=myCRS)

# Add a colored background
ax.add_patch(plt.Rectangle((xmin - 5000, ymin - 5000), xmax - xmin + 10000, ymax - ymin + 10000, facecolor='lightblue'))

plt.show()

