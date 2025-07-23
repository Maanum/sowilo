from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.opportunities import router as opportunities_router
from backend.db.base import Base
from backend.db.session import engine
from backend.config import settings
import backend.models.opportunity  # Ensure model is imported

app = FastAPI(title="Job Opportunities API")

# Configure CORS
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"message": "Job Opportunities API"}

app.include_router(opportunities_router, prefix="/opportunities", tags=["opportunities"])

# Create tables on startup
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)