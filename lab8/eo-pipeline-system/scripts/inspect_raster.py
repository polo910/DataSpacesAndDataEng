import rasterio
path = "assets/bands/B04_10m.tif"
with rasterio.open(path) as src:
    print(
        "Width:",
        src.width
    )
    print(
        "Height:",
        src.height
    )
    print(
        "Bands:",
        src.count
    )
    print(
        "CRS:",
        src.crs
    )
    print(
        "Bounds:",
        src.bounds
    )
