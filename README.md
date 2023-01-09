data-mountains
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

``` python
# requirements

import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, Point, LineString, GeometryCollection
from shapely.ops import unary_union, transform
import altair as alt
import math
import matplotlib.pyplot as plt
```

## Install

``` sh
pip install data_mountains
```

## How to use

``` python
# import the library
import data_mountains.mountainise as dm

# some census output area population density data
popden_oa = pd.read_csv('https://gist.github.com/joel-lbth/b35c0ac7a3652c3f34441d25c45ea84a/raw/d69075dc707b5bdb06c9b640d43db1e5b2ffcb64/lbth_census_2021_pop_density_oa.csv')

# some census output area population weighted centroids
oa = gpd.read_file("https://gist.github.com/joel-lbth/00f24602797d51d02d2177ed82f9295d/raw/b6c26621504a0df20ef6db1c93e5f99bce911d0a/lbth_oa21_pop_centroids.geojson")

# add data attribute to each point by merging on common identifier
gdf = oa.merge(popden_oa, left_on='oa21cd', right_on='GEOGRAPHY_CODE')

# turn each point in a data sized mountain
gdf = dm.points_to_peaks(gdf=gdf, column='OBS_VALUE', range=[0, 0.01])
```

``` python
# use Altair to create the visual
output = dm.plot(gdf=gdf, fill='#eee', stroke='#333')
```

![](visualization.svg)
