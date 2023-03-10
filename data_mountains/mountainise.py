# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_mountainise.ipynb.

# %% auto 0
__all__ = ['project_data_to_spatial_range', 'make_peak', 'points_to_peaks', 'plot']

# %% ../nbs/00_mountainise.ipynb 3
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString, GeometryCollection
from shapely.ops import unary_union, transform
import altair as alt
import math

# %% ../nbs/00_mountainise.ipynb 4
def project_data_to_spatial_range(n, range1, range2):
    """recalculate a number n from range1 (dataset) to range2 (latitude)

    Args:
        n (int): data value<br>
        range1 (list): dataset range<br>
        range2 (list): projected range

    Returns:
        float: reprojected value
    """
    delta1 = range1[1] - range1[0]
    delta2 = range2[1] - range2[0]
    return (delta2 * (n - range1[0]) / delta1) + range2[0]


# %% ../nbs/00_mountainise.ipynb 5
def make_peak(point, val, range1, range2):
    """turn a spatial point into a data peak

    Args:
        point (shapely.Point): i.e. a polygon centroid<br>
        val (int): i.e. a value to represent<br>
        range1 (list): min, max range of input data<br>
        range2 (list): min, max range of output data

    Returns:
        shapely.LineString: peak sized by input val
    """
    height = project_data_to_spatial_range(val, range1, range2)
    angle = math.pi / 3
    start = Point(point.x - 0.001, point.y)
    mid = Point(point.x, point.y + height * math.sin(angle))
    end = Point(point.x + 0.001, point.y)
    line = LineString([start, mid, end])
    return line


# %% ../nbs/00_mountainise.ipynb 6
def points_to_peaks(gdf, column, range):
    """turn point geometry into peak, sized by column and projected to range

    Args:
        gdf (geodataframe): contains points, ids, and a data column<br>
        column (string): name of data column<br>
        range (array:int): range to project data values into

    Returns:
        geodataframe: geospatial dataset of peaks
    """
    gdf["y"] = gdf.geometry.y
    gdf = gdf.sort_values(by=("y"), ascending=False)

    gdf["geometry"] = gdf.apply(
        lambda row: make_peak(
            row.geometry, row[column], [gdf[column].min(), gdf[column].max()], range
        ),
        axis=1,
    )
    return gdf


# %% ../nbs/00_mountainise.ipynb 7
def plot(gdf, fill, stroke):
    """create an altair map vis from a geodataframe

    Args:
        gdf (GeoDataframe): geospatial dataframe<br>
        fill (string): color string, e.g. black, #111<br>
        stroke (string): color string, e.g. black, #111

    Returns:
        altair.Chart: map vis
    """
    chart = (
        alt.Chart(gdf)
        .mark_geoshape(fill=fill, stroke=stroke)
        .project("mercator")
        .properties(width=500, height=500)
    )
    return chart

