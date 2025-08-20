import models.opportunity  # Ensure model is imported
import models.profile  # Ensure profile model is imported
from config import settings
from db.base import Base
from db.session import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.opportunities import router as opportunities_router
from routes.profile import router as profile_router

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


app.include_router(
    opportunities_router, prefix="/opportunities", tags=["opportunities"]
)
app.include_router(profile_router, prefix="/profile", tags=["profile"])

# Create tables on startup
Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
