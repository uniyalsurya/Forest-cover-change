import rasterio
import numpy as np

red_path = "data/2021/B04-21.jp2"
nir_path = "data/2021/B08-21.jp2"

with rasterio.open(red_path) as red_src:
    red = red_src.read(1).astype(np.float32)

with rasterio.open(nir_path) as nir_src:
    nir = nir_src.read(1).astype(np.float32)

print("Red shape:", red.shape)
print("NIR shape:", nir.shape)

print("Red range:", red.min(), red.max())
print("NIR range:", nir.min(), nir.max())

denominator = nir + red

ndvi = np.divide(
    nir - red,
    denominator,
    out=np.zeros_like(nir),
    where=denominator != 0
)

print("NDVI range:", ndvi.min(), ndvi.max())
print("Mean NDVI:", ndvi.mean())

forest_mask = ndvi >= 0.3

print("Vegetation pixels:", forest_mask.sum())
print("Total pixels:", forest_mask.size)

percentage = (forest_mask.sum() / forest_mask.size) * 100

print("Vegetation percentage:", percentage)