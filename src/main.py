# src/main.py

from fastapi import FastAPI
from src.query.query_service import query_router  # Importing routers from query module
from src.utils.db_utils import get_db_connection
from src.utils.log_utils import setup_logger
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI()

# Include routers for different endpoints
app.include_router(query_router, prefix="/query", tags=["Query Service"])

Instrumentator().instrument(app).expose(app, endpoint="/metrics")


@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Initialize logger
logger = setup_logger("main")

@app.on_event("startup")
async def startup_event():
    # Startup logic, such as initializing a database connection
    db = get_db_connection()
    logger.info("Database connection established.")

@app.on_event("shutdown")
async def shutdown_event():
    # Shutdown logic, if any
    logger.info("Shutting down application.")

# Additional configuration or routes if needed

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
