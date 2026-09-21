from fastapi import FastAPI

app = FastAPI(
    title="Forest Cover Change Detection",
    description="Satellite-based forest cover change detection system",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Forest Cover Change Detection API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }