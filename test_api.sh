#!/bin/bash

echo "=========================================="
echo "Testing Algorithm Complexity Analyzer API"
echo "=========================================="

# Test 1: Analyze endpoint
echo -e "\n1. Testing /analyze endpoint..."
echo "Running bubble sort analysis..."
curl -X GET "http://localhost:8080/analyze?algo=bubble&n=1000&steps=10" | jq '.'

# Test 2: Save analysis endpoint
echo -e "\n\n2. Testing /save_analysis endpoint..."
echo "Saving analysis results..."
curl -X POST http://localhost:8080/save_analysis \
  -H "Content-Type: application/json" \
  -d '{
    "algo": "bubble sort",
    "items": 1000,
    "steps": 10,
    "start_time": 1707000000000,
    "end_time": 1707000003000,
    "total_time_ms": 3000,
    "time_complexity": "O(n²)",
    "path_to_graph": "base64_encoded_image_here"
  }' | jq '.'

# Test 3: Retrieve analysis endpoint
echo -e "\n\n3. Testing /retrieve_analysis endpoint..."
echo "Retrieving analysis with ID 1..."
curl -X GET "http://localhost:8080/retrieve_analysis?id=1" | jq '.'

echo -e "\n\n=========================================="
echo "Testing complete!"
echo "=========================================="
