"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.solar import router as solar_router
from app.core.config import settings

app = FastAPI(
    title="solmap API",
    description="Solar potential mapping for Europe.",
    version="0.1.0",
    debug=settings.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(solar_router, prefix="/api/v1")


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok", "service": settings.app_name}
