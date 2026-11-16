from fastapi import FastAPI

from opsflow.api.v1.auth import router as auth_router
from opsflow.api.v1.tickets import router as tickets_router
from opsflow.core.config import settings

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)

app.include_router(tickets_router, prefix=settings.API_V1_PREFIX)
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)

@app.get("/health/")
async def get_health():
    return {"status": "ok"}
