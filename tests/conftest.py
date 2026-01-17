"""
Pytest configuration and fixtures for FastMVC Middleware tests.
"""

import pytest
from fastapi import FastAPI, Request
from starlette.testclient import TestClient


@pytest.fixture
def app() -> FastAPI:
    """Create a test FastAPI application."""
    return FastAPI()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_routes(app: FastAPI):
    """Add sample routes to the test application."""
    
    @app.get("/")
    async def root():
        return {"message": "Hello, World!"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy"}
    
    @app.get("/protected")
    async def protected(request: Request):
        auth = getattr(request.state, "auth", None)
        return {"auth": auth}
    
    @app.get("/context")
    async def context(request: Request):
        return {
            "request_id": getattr(request.state, "request_id", None),
            "start_time": str(getattr(request.state, "start_time", None)),
        }
    
    @app.post("/data")
    async def post_data(request: Request):
        body = await request.json()
        return {"received": body}
    
    return app

