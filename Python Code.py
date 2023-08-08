import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

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

# loads the boundary of Rhodes island as the land extent and analysis area
outline = gpd.read_file(os.path.abspath('AssessmentData/RhodesBnd.shp'))
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='sienna', linewidth=1)

# create axis object in the figure using the UTM projection to plot data.
ax = plt.axes(projection=myCRS)

# creates a dictionary to assign fire dates to colors and sizes
fire_styles = {
    '24/07/2023': {'colour': 'yellow', 'size': 6},
    '25/07/2023': {'colour': 'darkorange', 'size': 6},
    '26/07/2023': {'colour': 'red', 'size': 6},
    '27/07/2023': {'colour': 'deeppink', 'size': 6},
    # More dates can be added

}

# creates a dictionary to assign BUA classes to colors, symbols and sizes
bua_styles = {
    'city': {'colour': 'purple', 'marker': '*', 'size': 17},
    'town': {'colour': 'purple', 'marker': 's', 'size': 7},
    'suburb': {'colour': 'purple', 'marker': 's', 'size': 5},
    'village': {'colour': 'k', 'marker': 's', 'size': 4},
    'hamlet': {'colour': 'k', 'marker': 's', 'size': 2.5},
    'locality': {'colour': 'k', 'marker': 's', 'size': 1},

}

# creates a dictionary to assign road types to colors and widths
road_type_styles = {
    'primary': {'colour': 'red', 'width': 3.0},
    'secondary': {'colour': 'green', 'width': 1.5},
    'tertiary': {'colour': 'lime', 'width': 1.0},

    }

# draws BUA features with hierarchical symbology
bua_legend_handles = []

for bua_class in bua_styles.keys():
    style = bua_styles[bua_class]
    bua_class_features = BUA[BUA['fclass'] == bua_class]

    # plots the BUA features with a white halo effect
    ax.plot(bua_class_features['geometry'].x, bua_class_features['geometry'].y, marker=style['marker'], color='white', linestyle='None', markersize=style['size'] + 1, zorder=5)

    # Plot the actual BUA features
    ax.plot(bua_class_features['geometry'].x, bua_class_features['geometry'].y, marker=style['marker'], color=style['colour'], linestyle='None', markersize=style['size'], label=bua_class, zorder=6)

    # Add legend handles
    bua_legend_handles.append(mlines.Line2D([], [], color=style['colour'], marker=style['marker'], markersize=style['size'], linestyle='None', label=bua_class))

# draws road features with a set hierarchy to draw in that order
road_legend_handles = []
for road_type_name in ['primary', 'primary_link', 'secondary', 'secondary_link', 'tertiary', 'track']:
    if road_type_name in road_type_styles:
        style = road_type_styles[road_type_name]
        road_type_features = Road[Road['fclass'] == road_type_name]
        for geom in road_type_features['geometry']:
            ax.add_line(mlines.Line2D(*geom.xy, color=style['colour'], linewidth=style['width'], zorder=4))
        road_legend_handles.append(mlines.Line2D([], [], color=style['colour'], linewidth=style['width'], label=road_type_name))

# draws fire points with symbology defined by acquisition date and apply transparency
fire_legend_handles = []
for acq_date in fire_styles.keys():
    style = fire_styles[acq_date]
    fire_date_features = Fire[Fire['ACQDATENEW'] == acq_date]
    if not fire_date_features.empty:
        for geom in fire_date_features['geometry']:
            ax.plot(geom.x, geom.y, marker='o', color=style['colour'], markersize=style['size'],
                    markeredgecolor=style['colour'], linestyle='None', label=acq_date, zorder=8, alpha=0.5)
        fire_legend_handles.append(mlines.Line2D([], [], color=style['colour'], marker='o', markersize=style['size'],
                                                 linestyle='None', label=acq_date, alpha=0.5))

# draws river lines
river_color = 'deepskyblue'
river_size = 0.5
river_legend_handles = [mlines.Line2D([], [], color=river_color, linewidth=river_size, label='River')]

for geom in River['geometry']:
    x, y = geom.xy
    ax.plot(x, y, color=river_color, linewidth=river_size, zorder=2)

# draws lake polygons
lake_color = 'darkblue'
lake_features = Lake
lake_shapes = [geom for geom in lake_features['geometry']]
lake_feature = ShapelyFeature(lake_shapes, myCRS, facecolor=lake_color, label='Lake', zorder=3)
ax.add_feature(lake_feature)
lake_legend_handles = [mpatches.Patch(facecolor=lake_color, label='Lake')]

# creates a buffer around the fire points and dissolves into a single polygon
fire_buffer = Fire.buffer(distance=0.015)  # Buffer distance of approximately 1500 meters
fire_buffer = fire_buffer.unary_union

# converts the dissolved buffer to a GeoDataFrame
fire_buffer_gdf = gpd.GeoDataFrame(geometry=[fire_buffer])

# plots the dissolved buffer with transparency
fire_buffer_feature = ShapelyFeature(fire_buffer_gdf['geometry'], myCRS, facecolor='maroon', edgecolor='none', alpha=0.5, zorder=7)
ax.add_feature(fire_buffer_feature)

# creates a legend handle for the fire buffer area
buffer_legend_handle = mpatches.Patch(facecolor='red', edgecolor='none', alpha=0.2, label='Danger Area')

# adds the created features to the map.
xmin, ymin, xmax, ymax = outline.total_bounds
ax.add_feature(outline_feature)

# generates matplotlib handles to create a legend of features to be used within the map

def generate_handles(labels, colors, halo_color='white', edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        # Create a rectangle with white halo and specified face color
        rect = mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha, linewidth=0.5, linestyle='dashed', hatch='////', joinstyle='round')
        handles.append(rect)
    return handles

legend_handles = []

# adds fire legend handles to the legend
legend_handles.extend(fire_legend_handles)

# adds BUA legend handles as per feature sizes and capitalize the first letter in the label
for bua_legend_handle in bua_legend_handles:
    label = bua_legend_handle.get_label()
    capitalized_label = label.title()
    legend_handles.append(mlines.Line2D([], [], color=bua_legend_handle.get_color(), marker=bua_legend_handle.get_marker(), markersize=bua_legend_handle.get_markersize(), linestyle='None', label=capitalized_label))

# adds road legend handles as per feature sizes and capitalize the first letter in the label
for road_legend_handle in road_legend_handles:
    label = road_legend_handle.get_label()
    capitalized_label = label.title()
    legend_handles.append(mlines.Line2D([], [], color=road_legend_handle.get_color(), linewidth=road_legend_handle.get_linewidth(), label=capitalized_label))

# adds river legend handles to the legend
legend_handles.extend(river_legend_handles)

# adds lake legend handles to the legend
legend_handles.extend(lake_legend_handles)

# adds buffer legend handle to the legend handles list
legend_handles.append(buffer_legend_handle)

# creates the legend
plt.legend(handles=legend_handles, title='Legend', loc='upper left')

# using the boundary of the shapefile features, zoom the map to the area of interest
ax.set_extent([xmin-0.15, xmax+0.01, ymin-0.01, ymax+0.01], crs=myCRS)

# adds a colored background
ax.add_patch(plt.Rectangle((xmin - 5000, ymin - 5000), xmax - xmin + 10000, ymax - ymin + 10000, facecolor='lightblue'))

# adds a title text box to the top center of the map
title_text = "Rhodes Wildfire Progression 24-27 Aug 2023"
bbox_props = dict(boxstyle="square,pad=0.3", facecolor='white', edgecolor='black', linewidth=1)
ax.text(0.5, 0.95, title_text, transform=ax.transAxes, fontsize=12, ha='center', va='center', bbox=bbox_props)

# saves the figure as map.png, cropped to the axis (bbox_inches='tight'), and a dpi of 300
myFig.savefig('RhodesFireMap.png', bbox_inches='tight', dpi=300)

