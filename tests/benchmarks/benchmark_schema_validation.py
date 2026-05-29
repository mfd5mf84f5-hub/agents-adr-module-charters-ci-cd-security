#!/usr/bin/env python3
"""Performance benchmark suite for schema architect.

Uses pytest-benchmark for regression detection.

Usage:
    pytest tests/benchmarks/ -v
    pytest tests/benchmarks/ --benchmark-compare=0001  # Compare with baseline
"""

import pytest
import json
from time import time
from jsonschema import validate, ValidationError


@pytest.fixture
def sample_schema():
    """Sample JSON schema for validation."""
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer", "minimum": 0},
            "email": {"type": "string", "format": "email"},
            "tags": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["name", "email"]
    }


@pytest.fixture
def sample_data():
    """Sample data for validation."""
    return {
        "name": "John Doe",
        "age": 30,
        "email": "john@example.com",
        "tags": ["python", "testing"]
    }


class TestSchemaValidationBenchmarks:
    """Benchmarks for schema validation performance."""
    
    def test_validate_simple_schema(self, benchmark, sample_schema, sample_data):
        """Benchmark: Validate simple schema (expected: < 10ms)."""
        def validate_func():
            validate(instance=sample_data, schema=sample_schema)
        
        result = benchmark(validate_func)
        # Assert passes < 10ms (SLA)
        assert benchmark.stats.mean < 0.010  # 10ms
    
    def test_validate_batch_1000(self, benchmark, sample_schema):
        """Benchmark: Validate 1000 records (expected: < 1s)."""
        data = [
            {
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "age": 20 + (i % 50),
                "tags": [f"tag{j}" for j in range(i % 5)]
            }
            for i in range(1000)
        ]
        
        def validate_batch():
            for record in data:
                validate(instance=record, schema=sample_schema)
        
        result = benchmark(validate_batch)
        # Batch should complete < 1 second
        assert benchmark.stats.mean < 1.0
    
    def test_invalid_data_validation(self, benchmark, sample_schema):
        """Benchmark: Validation failure path (expected: < 5ms)."""
        invalid_data = {"name": "John"}  # Missing required email
        
        def validate_invalid():
            try:
                validate(instance=invalid_data, schema=sample_schema)
            except ValidationError:
                pass  # Expected
        
        result = benchmark(validate_invalid)
        # Failure path should be fast
        assert benchmark.stats.mean < 0.005  # 5ms


class TestFeatureExtractionBenchmarks:
    """Benchmarks for feature extraction performance."""
    
    def test_extract_features_100_records(self, benchmark):
        """Benchmark: Extract features from 100 records (expected: < 500ms)."""
        # Placeholder - replace with actual feature extraction
        def extract_features():
            results = []
            for i in range(100):
                # Simulate feature extraction
                features = {
                    'id': i,
                    'feature1': i * 2,
                    'feature2': f"tag_{i}",
                }
                results.append(features)
            return results
        
        result = benchmark(extract_features)
        # Extraction should complete < 500ms
        assert benchmark.stats.mean < 0.5


class TestHTTPEndpointBenchmarks:
    """Benchmarks for HTTP endpoint latency."""
    
    def test_get_schemas_endpoint(self, benchmark, client):
        """Benchmark: GET /schemas (expected: < 50ms)."""
        def get_schemas():
            response = client.get('/schemas')
            return response
        
        result = benchmark(get_schemas)
        # Endpoint should respond < 50ms
        assert benchmark.stats.mean < 0.050
    
    def test_validate_endpoint(self, benchmark, client, sample_schema, sample_data):
        """Benchmark: POST /validate (expected: < 100ms)."""
        def validate_endpoint():
            response = client.post(
                '/validate',
                json={"schema": sample_schema, "data": sample_data}
            )
            return response
        
        result = benchmark(validate_endpoint)
        # Endpoint should respond < 100ms
        assert benchmark.stats.mean < 0.100
