from fastapi import FastAPI
from app.api.compare import router as compare_router

app = FastAPI(
    title="Deficiency Detection Agent",
    version="1.0.0"
)

app.include_router(compare_router, prefix="/compare")

@app.get("/")
def health_check():
    return {"status": "Deficiency Detection Agent running"}
