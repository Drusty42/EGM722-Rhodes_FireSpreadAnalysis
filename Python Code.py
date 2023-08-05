import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

# Create a dictionary to assign fire dates to colors and sizes
fire_styles = {
    '24/07/2023': {'colour': 'yellow', 'size': 6},
    '25/07/2023': {'colour': 'darkorange', 'size': 6},
    '26/07/2023': {'colour': 'red', 'size': 6},
    '27/07/2023': {'colour': 'deeppink', 'size': 6},
    # More dates can be added

}

# Create a dictionary to assign BUA classes to colors and symbols
bua_styles = {
    'city': {'colour': 'dimgrey', 'marker': '*', 'size': 17},
    'town': {'colour': 'dimgrey', 'marker': 's', 'size': 7},
    'suburb': {'colour': 'dimgrey', 'marker': 's', 'size': 5},
    'village': {'colour': 'k', 'marker': 's', 'size': 4},
    'hamlet': {'colour': 'k', 'marker': 's', 'size': 2.5},
    'locality': {'colour': 'k', 'marker': 's', 'size': 1},

}

# Create a dictionary to assign road types to colors and widths
road_type_styles = {
    'primary': {'colour': 'red', 'width': 3.0},
    'secondary': {'colour': 'orange', 'width': 1.5},
    'tertiary': {'colour': 'brown', 'width': 1.0},

    }

# generates matplotlib handles to create a legend of features to be used within the map
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# Create a scale bar of 25Km length with 5Km increments located bottom right of the map
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

# Draw BUA features with hierarchical symbology
bua_legend_handles = []
for bua_class in bua_styles.keys():
    style = bua_styles[bua_class]
    bua_class_features = BUA[BUA['fclass'] == bua_class]
    ax.plot(bua_class_features['geometry'].x, bua_class_features['geometry'].y, marker=style['marker'], color=style['colour'], linestyle='None', markersize=style['size'], label=bua_class, zorder=5)
    bua_legend_handles.append(mlines.Line2D([], [], color=style['colour'], marker=style['marker'], markersize=style['size'], linestyle='None', label=bua_class))


# Sort road features into a hierarchy and draw in that order
road_legend_handles = []
for road_type_name in ['primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'track']:
    if road_type_name in road_type_styles:
        style = road_type_styles[road_type_name]
        road_type_features = Road[Road['fclass'] == road_type_name]
        for geom in road_type_features['geometry']:
            ax.add_line(mlines.Line2D(*geom.xy, color=style['colour'], linewidth=style['width'], zorder=4))
        road_legend_handles.append(mlines.Line2D([], [], color=style['colour'], linewidth=style['width'], label=road_type_name))

# Draw fire points with symbology defined by acquisition date and apply transparency
fire_legend_handles = []
for acq_date in fire_styles.keys():
    style = fire_styles[acq_date]
    fire_date_features = Fire[Fire['ACQDATENEW'] == acq_date]
    if not fire_date_features.empty:
        for geom in fire_date_features['geometry']:
            ax.plot(geom.x, geom.y, marker='o', color=style['colour'], markersize=style['size'], markeredgecolor=style['colour'], linestyle='None', label=acq_date, zorder=6, alpha=0.4)
        fire_legend_handles.append(mlines.Line2D([], [], color=style['colour'], marker='o', markersize=style['size'], linestyle='None', label=acq_date, alpha=0.4))

# add the Rhodes boundary
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='khaki')

# Draw river lines
river_color = 'blue'
river_size = 1.5
river_legend_handles = [mlines.Line2D([], [], color=river_color, linewidth=river_size, label='River')]

for geom in River['geometry']:
    x, y = geom.xy
    ax.plot(x, y, color=river_color, linewidth=river_size, zorder=2)

# Draw lake polygons
lake_color = 'darkblue'
lake_features = Lake
lake_shapes = [geom for geom in lake_features['geometry']]
lake_feature = ShapelyFeature(lake_shapes, myCRS, facecolor=lake_color, label='Lake', zorder=3)
ax.add_feature(lake_feature)
lake_legend_handles = [mpatches.Patch(facecolor=lake_color, label='Lake')]

# adds the created features to the map
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)

# using the boundary of the shapefile features, zoom the map to the area of interest
ax.set_extent([xmin-0.1, xmax+0.1, ymin-0.1, ymax+0.1], crs=myCRS)

# Add a colored background
ax.add_patch(plt.Rectangle((xmin - 5000, ymin - 5000), xmax - xmin + 10000, ymax - ymin + 10000, facecolor='lightblue'))

legend_handles = []

# Add fire legend handles to the legend
legend_handles.extend(fire_legend_handles)

# Add BUA legend handles as per feature sizes and capitalize the first letter in the label
for bua_legend_handle in bua_legend_handles:
    label = bua_legend_handle.get_label()
    capitalized_label = label.title()
    legend_handles.append(mlines.Line2D([], [], color=bua_legend_handle.get_color(), marker=bua_legend_handle.get_marker(), markersize=bua_legend_handle.get_markersize(), linestyle='None', label=capitalized_label))

# Add road legend handles as per feature sizes and capitalize the first letter in the label
for road_legend_handle in road_legend_handles:
    label = road_legend_handle.get_label()
    capitalized_label = label.title()
    legend_handles.append(mlines.Line2D([], [], color=road_legend_handle.get_color(), linewidth=road_legend_handle.get_linewidth(), label=capitalized_label))

# Add river legend handles to the legend
legend_handles.extend(river_legend_handles)

# Add lake legend handles to the legend
legend_handles.extend(lake_legend_handles)

# Create the legend
plt.legend(handles=legend_handles, title='Legend', loc='upper left')

plt.show()