from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .routers import auth, patients, intakes, safety, care_plans, documents, reviews, guidelines
import uvicorn

# Automatically initialize database schema for MVP local environment ease
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(patients.router, prefix=settings.API_V1_STR)
app.include_router(intakes.router, prefix=settings.API_V1_STR)
app.include_router(safety.router, prefix=settings.API_V1_STR)
app.include_router(care_plans.router, prefix=settings.API_V1_STR)
app.include_router(documents.router, prefix=settings.API_V1_STR)
app.include_router(reviews.router, prefix=settings.API_V1_STR)
app.include_router(guidelines.router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "message": "Welcome to Multilingual Clinical Intelligence Backend"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
