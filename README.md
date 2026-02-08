# Algorithm Complexity Analyzer API

A Flask-based REST API that analyzes and visualizes the time complexity of various algorithms. Performs real-time algorithm analysis, generates performance graphs, and stores results in a MySQL database.

## Features

- Real-time algorithm performance analysis
- Automatic generation of time complexity graphs
- Database storage for analysis results
- RESTful API with three main endpoints
- Base64 encoded graph output

## Technologies

- Flask
- SQLAlchemy
- MySQL
- Matplotlib
- NumPy

## Installation

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip

### Setup

1. Clone the repository


bash
git clone https://github.com/yourusername/algo-complexity-analyzer.git
cd algo-complexity-analyzer

2. Create and activate virtual environment


bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies


bash
pip install -r requirements.txt

4. Configure database connection in `analysis_api.py`


python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user:password@localhost:3306/database'

5. Run the application


bash
python analysis_api.py

Server runs at http://localhost:8080

## API Endpoints

### 1. Analyze Algorithm


GET /analyze?algo=bubble&n=1000&steps=10
```

Parameters:

	* algo: Algorithm name (bubble, linear, binary, nested, exponential)
	* n: Number of elements
	* steps: Analysis steps

Response:

{
  "algo": "bubble",
  "items": 1000,
  "steps": 10,
  "start_time": 1707000000000,
  "end_time": 1707000003000,
  "total_time_ms": 3000.45,
  "time_complexity": "O(n²)",
  "path_to_graph": "base64_encoded_image"
}

2. Save Analysis
POST /save_analysis
Content-Type: application/json

Request body:

{
  "algo": "bubble sort",
  "items": 1000,
  "steps": 10,
  "start_time": 1707000000000,
  "end_time": 1707000003000,
  "total_time_ms": 3000,
  "time_complexity": "O(n²)",
  "path_to_graph": "base64_string"
}

Response:

{
  "status": "success",
  "message": "Analysis saved successfully",
  "id": 1
}

3. Retrieve Analysis
GET /retrieve_analysis?id=1

Response: Same format as analyze endpoint

Supported Algorithms
| Algorithm | Time Complexity |
|-----------|-----------------|
| Bubble Sort | O(n²) |
| Linear Search | O(n) |
| Binary Search | O(log n) |
| Nested Loops | O(n²) |
| Exponential | O(2^n) |

Testing
Run the test script:

chmod +x test_api.sh
./test_api.sh

Manual testing:

curl "http://localhost:8080/analyze?algo=bubble&n=500&steps=5"

Project Structure
algo-complexity-analyzer/
├── analysis_api.py          # Main Flask application
├── algorithm_analyzer.py    # Algorithm analysis logic
├── requirements.txt         # Dependencies
├── test_api.sh             # Testing script
├── config.py               # Configuration
└── README.md               # Documentation

Database Schema
Table: analysis_results

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| algorithm | String(50) | Algorithm name |
| items | Integer | Number of elements |
| steps | Integer | Analysis steps |
| start_time | Float | Start timestamp |
| end_time | Float | End timestamp |
| total_time | Float | Execution time |
| time_complexity | String(20) | Big O notation |
| graph_image_path | Text | Base64 graph |

Author
Alieu O. Jobe
