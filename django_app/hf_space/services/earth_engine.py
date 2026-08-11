import ee, geemap

class EarthEngineService:
    def __init__(self):
        pass

    def temp(self):
        # 1. Authenticate and Initialize GEE
        try:
            ee.Initialize()
        except Exception:
            ee.Authenticate()
            ee.Initialize(project='climate-change-0')  # Replace with your GCP project ID

        # 2. Define a Spatial Point of Interest (e.g., San Francisco)
        point = ee.Geometry.Point([-122.4194, 37.7749])

        # 3. Load and Filter a Satellite Image Collection (Sentinel-2 Surface Reflectance)
        s2_collection = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(point)
            .filterDate("2023-01-01", "2023-12-31")
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
        )

        # 4. Reduce Collection to a Single Median Image
        median_image = s2_collection.median()

        # 5. Compute Normalized Difference Vegetation Index (NDVI)
        # NDVI = (NIR - Red) / (NIR + Red) -> Bands B8 (NIR) and B4 (Red)
        ndvi = median_image.normalizedDifference(["B8", "B4"]).rename("NDVI")

        # 6. Print Metadata Information
        print("Image Collection Count:", s2_collection.size().getInfo())

        # 7. Interactive Visualization using Geemap
        Map = geemap.Map(center=[37.7749, -122.4194], zoom=10)

        # Add RGB True Color Layer
        vis_params_rgb = {
            "bands": ["B4", "B3", "B2"],
            "min": 0,
            "max": 3000,
        }
        Map.addLayer(median_image, vis_params_rgb, "Sentinel-2 True Color (RGB)")

        # Add NDVI Layer
        vis_params_ndvi = {
            "min": -0.1,
            "max": 0.8,
            "palette": ["blue", "white", "green"],
        }
        Map.addLayer(ndvi, vis_params_ndvi, "NDVI Layer")

        # Display the map (works directly inside Jupyter/PyCharm notebooks)
        Map