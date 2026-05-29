from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.core.config import settings
from app.db.session import SessionLocal, engine
from app.graphql.schema import get_graphql_router
import app.models.vehicle 

app = FastAPI(title=settings.app_title, version=settings.app_version)

async def get_context():
    db = SessionLocal()
    try:
        yield {"db": db}
    finally:
        db.close()

app.include_router(get_graphql_router(get_context), prefix="/graphql")

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

@app.get("/status", tags=["Health"])
def status():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready"}
    except Exception as exc:
        return JSONResponse(status_code=503, content={"status": "unavailable", "detail": str(exc)})
