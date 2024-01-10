import rasterio
import numpy as np
import sys, os
import fiona
from shapely.geometry import shape
import cv2
from shapely.geometry.polygon import Polygon


colors = {
    "B01a" : (255, 0 , 0),
    "B01b" : (0, 255 , 0),
    "B01c" : (0, 0 , 255),
    "B02a" : (255, 255 , 0),
    "B02b" : (255, 0 , 255),
    "B03a" : (0, 255 , 255),
    "B04a" : (0, 120 , 200)
}
geotiff_path = sys.argv[1]
shp_folder = sys.argv[2]

with rasterio.open(geotiff_path) as geotiff:

    # creare immagine con stessa size del geotiff
    mask = np.zeros((geotiff.height, geotiff.width, 3), np.uint8)    

    for folder in sorted(os.listdir(shp_folder)):

        color = colors[folder[0:4]]

        for shp_file in os.listdir(os.path.join(shp_folder, folder)):

            if not shp_file.endswith("shp"):
                continue

            with fiona.open(os.path.join(shp_folder, folder, shp_file), "r") as shapefile:
                
                print(shp_file)

                for feature in shapefile:
                    geometry = shape(feature["geometry"])                    

                    if len(geometry.coords) < 4:
                        continue
                    
                    contour = geometry.coords
                    
                    polygon = []

                    for i, coord in enumerate(contour):
                        row, col = geotiff.index(coord[0], coord[1])
                        polygon.append([col, row])

                    cv2.fillPoly(mask, pts=[np.array(polygon)], color=color)

    cv2.imwrite("mask.png", mask)
