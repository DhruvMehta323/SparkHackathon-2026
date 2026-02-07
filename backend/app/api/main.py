"""FastAPI application entry point."""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api.config import settings
from app.core.logger import get_logger

# Import all route modules
from app.api.routes import (
    health,
    admin,
    projects,
    creators,
    engagements,
    feed,
    collab,
    engines
)

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    description="FairStage API - Fair discovery and collaboration platform for creators"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc) if settings.LOG_LEVEL == "DEBUG" else "An error occurred"
        }
    )


# Register all routers
app.include_router(health.router)
app.include_router(admin.router)
app.include_router(projects.router)
app.include_router(creators.router)
app.include_router(engagements.router)
app.include_router(feed.router)
app.include_router(collab.router)
app.include_router(engines.router)


# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Database: {settings.FAIRRANK_DB}")
    logger.info(f"API docs: http://localhost:8000/docs")
    logger.info("All routes registered successfully")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API server")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FairStage API",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_base": settings.API_V1_STR,
        "status": "running"
    }