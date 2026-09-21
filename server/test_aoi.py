from app.services.aoi import crop_to_aoi


image_path = "data/2021/B04-21.jp2"

image, profile = crop_to_aoi(image_path)

print("Original AOI crop shape:", image.shape)
print("CRS:", profile["crs"])
print("Transform:", profile["transform"])