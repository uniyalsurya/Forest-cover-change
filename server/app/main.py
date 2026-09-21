from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path


app = FastAPI(
    title="Forest Cover Change Detection",
    description="Satellite-based forest cover change detection system",
    version="1.0.0",
)


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


@app.get("/")
def root():
    return {
        "message": "Forest Cover Change Detection API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/change-map")
def get_change_map():
    image_path = (
        DATA_DIR /
        "change_map_2021_2026_overlay.png"
    )

    if not image_path.exists():
        return {
            "error": "Change map has not been generated yet."
        }

    return FileResponse(
        image_path,
        media_type="image/png"
    )