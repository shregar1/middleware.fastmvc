"""
Tests for Timing middleware.
"""

import pytest
import re
from fastapi import FastAPI
from starlette.testclient import TestClient

from fastmvc_middleware import TimingMiddleware


@pytest.fixture
def timing_app(sample_routes) -> FastAPI:
    """Create app with timing middleware."""
    app = sample_routes
    app.add_middleware(TimingMiddleware)
    return app


@pytest.fixture
def timing_client(timing_app: FastAPI) -> TestClient:
    """Create test client for timing app."""
    return TestClient(timing_app)


class TestTimingMiddleware:
    """Tests for TimingMiddleware."""
    
    def test_timing_header_added(self, timing_client: TestClient):
        """Test that X-Process-Time header is added."""
        response = timing_client.get("/")
        
        assert response.status_code == 200
        assert "X-Process-Time" in response.headers
    
    def test_timing_header_format_with_unit(self, timing_client: TestClient):
        """Test timing header format includes unit."""
        response = timing_client.get("/")
        timing = response.headers["X-Process-Time"]
        
        # Should match pattern like "1.23ms"
        assert re.match(r"^\d+\.\d+ms$", timing)
    
    def test_timing_is_positive_number(self, timing_client: TestClient):
        """Test that timing value is a positive number."""
        response = timing_client.get("/")
        timing = response.headers["X-Process-Time"]
        
        # Extract the number part
        value = float(timing.replace("ms", ""))
        assert value >= 0


class TestTimingConfiguration:
    """Tests for timing configuration options."""
    
    @pytest.fixture
    def custom_header_app(self, sample_routes) -> FastAPI:
        """Create app with custom header name."""
        app = sample_routes
        app.add_middleware(
            TimingMiddleware,
            header_name="X-Response-Time",
        )
        return app
    
    @pytest.fixture
    def custom_header_client(self, custom_header_app: FastAPI) -> TestClient:
        """Create test client for custom header app."""
        return TestClient(custom_header_app)
    
    def test_custom_header_name(self, custom_header_client: TestClient):
        """Test custom header name is used."""
        response = custom_header_client.get("/")
        
        assert "X-Response-Time" in response.headers
        assert "X-Process-Time" not in response.headers
    
    @pytest.fixture
    def no_unit_app(self, sample_routes) -> FastAPI:
        """Create app without unit in timing."""
        app = sample_routes
        app.add_middleware(
            TimingMiddleware,
            include_unit=False,
        )
        return app
    
    @pytest.fixture
    def no_unit_client(self, no_unit_app: FastAPI) -> TestClient:
        """Create test client for no-unit app."""
        return TestClient(no_unit_app)
    
    def test_without_unit(self, no_unit_client: TestClient):
        """Test timing without unit suffix."""
        response = no_unit_client.get("/")
        timing = response.headers["X-Process-Time"]
        
        # Should be just a number
        assert re.match(r"^\d+\.\d+$", timing)
        assert "ms" not in timing
    
    @pytest.fixture
    def precision_app(self, sample_routes) -> FastAPI:
        """Create app with custom precision."""
        app = sample_routes
        app.add_middleware(
            TimingMiddleware,
            precision=4,
            include_unit=False,
        )
        return app
    
    @pytest.fixture
    def precision_client(self, precision_app: FastAPI) -> TestClient:
        """Create test client for precision app."""
        return TestClient(precision_app)
    
    def test_custom_precision(self, precision_client: TestClient):
        """Test custom precision."""
        response = precision_client.get("/")
        timing = response.headers["X-Process-Time"]
        
        # Should have 4 decimal places
        assert re.match(r"^\d+\.\d{4}$", timing)

