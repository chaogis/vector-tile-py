#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import gzip
from vector_tile import renderer

if __name__ == "__main__" :
    # create a single tile at 0/0/0.png like tile.osm.org/0/0/0.png
    zoom = 0
    x = 0
    y = 0
    # request object holds a Tile XYZ and internally holds mercator extent
    req = renderer.Request(x,y,zoom)
    # create a vector tile, given a tile request
    vtile = renderer.VectorTile(req)
    # create a layer in the tile
    layer = vtile.add_layer(name="points")
    # for a given point representing a spot in NYC
    lat = 40.70512
    lng = -74.01226
    # and some attributes
    attr = {"hello":"world"}
    # convert to mercator coords
    x,y = renderer.lonlat2merc(lng,lat)
    # add this point and attributes to the tile
    vtile.add_point(layer,x,y,attr)
    # print the protobuf as geojson just for debugging
    # NOTE: coordinate rounding is by design and
    print('GeoJSON representation of tile (purely for debugging):')
    print(json.dumps(vtile.to_geojson(), indent=4))
    print('-'*60)
    # print the protobuf message as a string
    print('Protobuf string representation of tile (purely for debugging):')
    print(vtile)
    print('-'*60)
    # print the protobuf message
    if sys.version_info.major == 3:
        print('Serialized, gzip-coded tile message as bytes:')
        print(vtile.to_message())
        print('Gzip-coded tile message:')
        print(gzip.compress(vtile.to_message()))
    else:
        print('Serialized, gzip-coded tile message as string:')
        print(vtile.to_message())
        print('Gzip-coded tile message:')
        import StringIO
        out = StringIO.StringIO()
        with gzip.GzipFile(fileobj=out, mode="w") as f:
          f.write(vtile.to_message())
        print(out.getvalue())
