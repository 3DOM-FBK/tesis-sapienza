import numpy as np
import sys, os
import cv2
import fiona
from shapely.geometry import mapping, shape, LineString
import rasterio

def write_shapefile(output_folder, file_name, polygons, crs):
    
    schema = {"geometry": "LineString", "properties": {}}

    with fiona.open(os.path.join(output_folder, f"{file_name}.shp"), "w", driver="Shapefile", crs=crs, schema=schema) as dst:

        for polygon in polygons:
            feature = { 
                "geometry": polygon,
                "properties": {}
            }
                
            dst.write(feature)

colors = { # Put your desidered file names for the shapefiles here
    (255, 0 , 0) : "B01a", 
    (0, 255 , 0) : "B01b",
    (0, 0 , 255) : "B01c",
    (255, 255 , 0) : "B02a",
    (255, 0 , 255) : "B02b",
    (0, 255 , 255) : "B03a",
    (0, 120 , 200) : "B04a"
}

geotiff_path = sys.argv[1]
mask_path = sys.argv[2]
output_folder = sys.argv[3]

image = cv2.imread(mask_path)
out = np.zeros(image.shape)

with rasterio.open(geotiff_path) as geotiff:

    for i, color in enumerate(colors.keys()):

        mask = cv2.inRange(image, color, color)
        
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Trovo contorni    

        polygons = []

        for contour in contours:
            epsilon = 0.0001 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, closed=True)
            approx = np.squeeze(approx, axis=1)
            transformed = [geotiff.xy(coord[1], coord[0]) for coord in approx]
            geom = LineString(transformed)            
            polygons.append(mapping(geom))
            
            cv2.polylines(out, [approx], True, color, 7)
        
        write_shapefile(output_folder, colors[color], polygons, geotiff.crs)

cv2.imwrite(f"{output_folder}/contours.png", out)

# per ogni classe 
#     creo maschera b/w con con i pixel del colore classe

#     faccio find contours per separare i vari blob

#     per ogni contour faccio ApproxPolyDP