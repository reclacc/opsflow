from fastapi import FastAPI

app = FastAPI(
    title="OpsFlow API",
    description="Service desk",
    version="0.1.0"
)

@app.get("/health/")
async def get_health():
    return {"status": "ok"}
