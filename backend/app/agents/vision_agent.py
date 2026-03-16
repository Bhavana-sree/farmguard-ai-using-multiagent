import io
import numpy as np
from PIL import Image

from sentinelhub import (
    SHConfig,
    SentinelHubRequest,
    DataCollection,
    MimeType,
    CRS,
    BBox,
)

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

from app.config import (
    SENTINELHUB_CLIENT_ID,
    SENTINELHUB_CLIENT_SECRET,
    AZURE_VISION_ENDPOINT,
    AZURE_VISION_KEY,
)


class VisionAgent:
    def __init__(self):
        sh_config = SHConfig()
        sh_config.sh_client_id = SENTINELHUB_CLIENT_ID
        sh_config.sh_client_secret = SENTINELHUB_CLIENT_SECRET
        self.sh_config = sh_config

        self.vision_client = ImageAnalysisClient(
            endpoint=AZURE_VISION_ENDPOINT,
            credential=AzureKeyCredential(AZURE_VISION_KEY),
        )

    def _get_bbox(self, latitude: float, longitude: float, delta: float = 0.002):
        return BBox(
            bbox=[
                longitude - delta,
                latitude - delta,
                longitude + delta,
                latitude + delta,
            ],
            crs=CRS.WGS84,
        )

    def _fetch_ndvi_array(self, bbox, start_date="2025-01-01", end_date="2026-12-31"):
        evalscript = """
        //VERSION=3
        function setup() {
          return {
            input: ["B04", "B08"],
            output: { bands: 1, sampleType: "FLOAT32" }
          };
        }

        function evaluatePixel(sample) {
          let denom = sample.B08 + sample.B04;
          if (denom === 0) return [0.0];
          let ndvi = (sample.B08 - sample.B04) / denom;
          return [ndvi];
        }
        """

        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=(start_date, end_date),
                    mosaicking_order="mostRecent",
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=bbox,
            size=(256, 256),
            config=self.sh_config,
        )

        data = request.get_data()[0]
        return np.squeeze(data)

    def _fetch_true_color_png(self, bbox):
        evalscript = """
        //VERSION=3
        function setup() {
          return {
            input: ["B04", "B03", "B02"],
            output: { bands: 3, sampleType: "AUTO" }
          };
        }

        function evaluatePixel(sample) {
          return [sample.B04 * 2.5, sample.B03 * 2.5, sample.B02 * 2.5];
        }
        """

        request = SentinelHubRequest(
            evalscript=evalscript,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L2A,
                    time_interval=("2025-01-01", "2026-12-31"),
                    mosaicking_order="mostRecent",
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.PNG)],
            bbox=bbox,
            size=(256, 256),
            config=self.sh_config,
        )

        img = request.get_data()[0]
        pil = Image.fromarray(img.astype(np.uint8))
        buf = io.BytesIO()
        pil.save(buf, format="PNG")
        buf.seek(0)
        return buf

    def _azure_vision_check(self, image_bytes: io.BytesIO):
        try:
            result = self.vision_client.analyze(
                image_data=image_bytes.read(),
                visual_features=[VisualFeatures.TAGS, VisualFeatures.CAPTION],
            )

            tags = []
            if result.tags and result.tags.list:
                tags = [t.name for t in result.tags.list[:5]]

            caption = ""
            if result.caption and result.caption.text:
                caption = result.caption.text

            return {
                "caption": caption,
                "tags": tags,
            }
        except Exception as e:
            return {
                "caption": "",
                "tags": [],
                "vision_warning": str(e),
            }

    def _generate_ndvi_history(self, bbox):
        monthly_ranges = [
            ("2025-01-01", "2025-01-31", "Jan-2025"),
            ("2025-02-01", "2025-02-28", "Feb-2025"),
            ("2025-03-01", "2025-03-31", "Mar-2025"),
            ("2025-04-01", "2025-04-30", "Apr-2025"),
            ("2025-05-01", "2025-05-31", "May-2025"),
            ("2025-06-01", "2025-06-30", "Jun-2025"),
        ]

        history = []

        for start_date, end_date, label in monthly_ranges:
            try:
                ndvi_array = self._fetch_ndvi_array(bbox, start_date, end_date)
                mean_ndvi = float(np.nanmean(ndvi_array))
                history.append({
                    "month": label,
                    "ndvi": round(mean_ndvi, 2)
                })
            except Exception:
                history.append({
                    "month": label,
                    "ndvi": None
                })

        valid_values = [item["ndvi"] for item in history if item["ndvi"] is not None]

        if valid_values:
            avg_ndvi = round(sum(valid_values) / len(valid_values), 2)
            min_ndvi = round(min(valid_values), 2)
            max_ndvi = round(max(valid_values), 2)

            if avg_ndvi > 0.6:
                vegetation_trend = "Healthy vegetation trend"
            elif avg_ndvi > 0.4:
                vegetation_trend = "Moderate vegetation trend"
            else:
                vegetation_trend = "Low vegetation trend"
        else:
            avg_ndvi = None
            min_ndvi = None
            max_ndvi = None
            vegetation_trend = "No historical NDVI data available"

        return {
            "history": history,
            "average_ndvi": avg_ndvi,
            "min_ndvi": min_ndvi,
            "max_ndvi": max_ndvi,
            "vegetation_trend": vegetation_trend
        }

    def analyze_farm(self, latitude: float, longitude: float):
        bbox = self._get_bbox(latitude, longitude)

        ndvi_array = self._fetch_ndvi_array(bbox)
        mean_ndvi = float(np.nanmean(ndvi_array))

        canopy_mask = ndvi_array > 0.5
        canopy_percent = float(np.mean(canopy_mask) * 100.0)

        if canopy_percent > 60:
            tree_density = "High vegetation"
            estimated_trees = 350
        elif canopy_percent > 30:
            tree_density = "Medium vegetation"
            estimated_trees = 180
        else:
            tree_density = "Low vegetation"
            estimated_trees = 60

        rgb_bytes = self._fetch_true_color_png(bbox)
        azure_check = self._azure_vision_check(rgb_bytes)

        ndvi_history = self._generate_ndvi_history(bbox)

        return {
            "latitude": latitude,
            "longitude": longitude,
            "ndvi": round(mean_ndvi, 2),
            "canopy_percent": round(canopy_percent, 2),
            "tree_density": tree_density,
            "estimated_trees": estimated_trees,
            "azure_scene_check": azure_check,
            "ndvi_history": ndvi_history
        }